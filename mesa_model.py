from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa_agents import ImmuneCell, TumorCell
from mesa.datacollection import DataCollector
import csv
import pandas as pd
import random

class TumorModel(Model):
    def __init__(self, activate_therapy, 
                patient_sex, bmi, cd8, treg, nk, m1, m2, tumorCells, 
                immune_response_level, tumor_proliferation_rate, resistance_to_therapy,  
                width=20, height=20, ):
        
        #params that are not passed
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.current_id = 0
        self.max_number_of_cells = 400
        self.patient_alive = True
        self.message = ""
        self.running = True
        #params that are passed
        self.patient_sex = patient_sex
        self.bmi = bmi
        self.CD8 = cd8
        self.treg = treg
        self.nk = nk
        self.m1 = m1
        self.m2 = m2
        self.initial_tumors = tumorCells

        self.immune_response_level = immune_response_level
        self.tumor_proliferation_rate = tumor_proliferation_rate
        self.resistance_to_therapy = resistance_to_therapy

        self.activate_therapy = activate_therapy
        self.therapy_already_applied = False

        self.data_row = {}

        for _ in range(self.initial_tumors):
            x = self.random.randrange(width)
            y = self.random.randrange(height)
            self.spawn_tumor((x, y))

        modifiers = {
            "CD8": 1.0,
            "Treg": 0.9 if self.is_patient_obese() else 1.0,
            "M1": 1.1 if self.is_patient_obese() else 1.0,       
            "M2": 0.9 if self.is_patient_obese() else 1.0,       
            "NK": 0.9 if self.is_patient_obese() else 1.0,
            "immune_response_level": 0.95 if self.is_patient_obese() else 1.0,
            "tumor_proliferation_rate": 0.9 if self.is_patient_obese() else 1.0
        }

        modifiersSex = {
            "CD8": 1.05 if self.patient_sex == False else 1.0,
            "Treg": 1.05 if self.patient_sex == False else 1.0,
            "M1": 1.05 if self.patient_sex == False else 1.0,       
            "M2": 1.05 if self.patient_sex == False else 1.0,       
            "NK": 1.05 if self.patient_sex == False else 1.0,
            "immune_response_level": 1.05 if self.patient_sex == False else 1.0,
            "tumor_proliferation_rate": 1.1 if self.patient_sex == False else 1.0,
            "resistance_to_therapy": 1.05 if self.patient_sex == False else 1.0
        }

        # Applica i modificatori ai valori provenienti dalla GUI
        immune_types = {
            "CD8": int(self.CD8 * modifiers["CD8"] * modifiersSex["CD8"]),
            "Treg": int(self.treg * modifiers["Treg"] * modifiersSex["Treg"]),
            "M1": int(self.m1 * modifiers["M1"] * modifiersSex["M1"]),
            "M2": int(self.m2 * modifiers["M2"] * modifiersSex["M2"]),
            "NK": int(self.nk * modifiers["NK"] * modifiersSex["NK"])
        }
        
        total_cells = sum(immune_types.values())
        
        # 1. Crea tutte le possibili coordinate
        all_positions = [(x, y) for x in range(width) for y in range(height)]

        # 2. Mescola le posizioni
        self.random.shuffle(all_positions)

        # 3. Prendi le prime 50 posizioni uniche
        unique_positions = all_positions[:total_cells]

        # 4. Assegna agenti a posizioni uniche
        pos_index = 0

        for cell_type, n_cell in immune_types.items():
            for _ in range(n_cell):
                pos = unique_positions[pos_index]
                pos_index += 1
                agent = ImmuneCell(self.next_id(), self, cell_type)
                self.grid.place_agent(agent, pos)
                self.schedule.add(agent)

        
        #this part is to permit the visualization in the chart at each step
        self.datacollector = DataCollector(
            self.get_cells_count()
        )
        self.datacollector.collect(self)

    def spawn_tumor(self, pos):
        tumor = TumorCell(self.next_id(), self)
        self.grid.place_agent(tumor, pos)
        self.schedule.add(tumor)


    def get_cells_count(self):
        return {
                "Tumor Cells": lambda m: sum(isinstance(a, TumorCell) for a in m.schedule.agents),
                "CD8": lambda m: sum(isinstance(a, ImmuneCell) and a.cell_type == "CD8" for a in m.schedule.agents),
                "Treg": lambda m: sum(isinstance(a, ImmuneCell) and a.cell_type == "Treg" for a in m.schedule.agents),
                "NK": lambda m: sum(isinstance(a, ImmuneCell) and a.cell_type == "NK" for a in m.schedule.agents),
                "M1": lambda m: sum(isinstance(a, ImmuneCell) and a.cell_type == "M1" for a in m.schedule.agents),
                "M2": lambda m: sum(isinstance(a, ImmuneCell) and a.cell_type == "M2" for a in m.schedule.agents)
            }
    
    def spawn_immune(self, cell_type, pos):
        new_agent = ImmuneCell(self.next_id(), self, cell_type)
        self.grid.place_agent(new_agent, pos)
        self.schedule.add(new_agent)   

    def is_patient_obese(self):
        return self.bmi >= 30

    def apply_therapy_effects(self):
        print("Terapia somministrata: inizio effetto.")

        print("irl before", self.immune_response_level)
        print("tpr before", self.tumor_proliferation_rate)
        self.immune_response_level *= 1.5
        self.tumor_proliferation_rate -= 0.01
        print("irl after", self.immune_response_level)
        print("tpr after", self.tumor_proliferation_rate)



    #return isAlive, message
    #patient_state: the actual situation of the patient (0=died, 1=healed, 2=running)
    def check_number_of_cells(self):

        counts = self.get_cells_count()
        for cell_type, counter in counts.items():
            num = counter(self)

            #check if the therapy is needed
            if num >= 200 and cell_type == "Tumor Cells" and not self.therapy_already_applied and self.activate_therapy: 
                self.therapy_already_applied = True
                self.apply_therapy_effects()

            #check if the tumor is completely eliminated
            if num == 0 and cell_type == "Tumor Cells":
                self.message = "Simulazione terminata: paziente guarito dal tumore"
                return 1

            #check for each type of cells if its instances are too many
            if num > self.max_number_of_cells:
                if cell_type == "Tumor Cells":
                    self.message = "⚠️ Paziente deceduto: crescita tumorale incontrollata."
                    return 0
                
                self.message = "Simulazione terminata: paziente guarito dal tumore"
                return 1, 
            
        self.message = f"✅ Stato: Vivo — Cellule tumorali: {self.get_cells_count()["Tumor Cells"](self)}"
        return 2

    def printParameters(self):
        print("bmi", self.bmi) 
        print("cd8" ,self.CD8)
        print("treg",self.treg)
        print("nk",self.nk) 
        print("m1" ,self.m1)
        print("m2",self.m2)
        print("immune_response_level",self.immune_response_level)
        print("tumor_proliferation_rate",self.tumor_proliferation_rate)
        print("resistance_to_therapy",self.resistance_to_therapy)


    def step(self):

        if self.schedule.time == 0:
            self.data_row = {
                "activate_therapy": self.activate_therapy,
                "patient_sex": self.patient_sex,
                "bmi": self.bmi,
                "cd8": self.CD8,
                "treg": self.treg,
                "nk": self.nk,
                "m1": self.m1,
                "m2": self.m2,
                "tumorCells": self.initial_tumors,
                "immune_response_level": self.immune_response_level,
                "tumor_proliferation_rate": self.tumor_proliferation_rate,
                "resistance_to_therapy": self.resistance_to_therapy,
                "result":""
            }

        if not self.patient_alive or self.schedule.time > 80 :
            self.running = False
            self.data_row["result"] = self.patient_alive
            self.simulation_saver(self.data_row)
            return  #stop the simulation

        self.schedule.step()
        self.datacollector.collect(self)

        # Check the number of each type of cell        
        patient_state = self.check_number_of_cells()
        if patient_state == 0:
            self.patient_alive = False
        
        if patient_state == 1: 
            self.data_row["result"] = self.patient_alive
            self.simulation_saver(self.data_row)
            self.running = False
            return

        #print infos when activating the immune therapy
        if self.therapy_already_applied:
            print("irl ", self.immune_response_level)
            print("tpr ", self.tumor_proliferation_rate)

    def simulation_saver(self, data_row):
        filename = "rcc_simulation.csv"
        with open(filename, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=data_row.keys(), delimiter=';')
            writer.writerow(data_row)