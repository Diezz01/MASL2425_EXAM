from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa_agents import ImmuneCell, TumorCell
from mesa.datacollection import DataCollector
from mesa_parameters import PatientParameters
import random

class TumorModel(Model):
    def __init__(self,activate_therapy, patient_sex, bmi, cd8, treg, nk, m1, m2, immune_response_level, tumor_proliferation_rate, resistance_to_therapy, width=20, height=20, initial_tumors=10):
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.current_id = 0
        #self.patient_params = patient_params
        self.max_number_of_cells = 400
        self.patient_alive = True

        self.patient_sex = patient_sex
        self.bmi = bmi
        self.CD8 = cd8
        self.treg = treg
        self.nk = nk
        self.m1 = m1
        self.m2 = m2
        self.immune_response_level = immune_response_level
        self.tumor_proliferation_rate = tumor_proliferation_rate
        self.resistance_to_therapy = resistance_to_therapy

        self.activate_therapy = activate_therapy
        self.therapy_already_applied = False

        for _ in range(initial_tumors):
            x = self.random.randrange(width)
            y = self.random.randrange(height)
            self.spawn_tumor((x, y))

        # Crea cellule immunitarie
        immune_types = ["CD8", "Treg", "M1", "M2", "NK"]
        cells_per_type = 10  # 10 per tipo
        total_cells = cells_per_type * len(immune_types)  # 50

        # 1. Crea tutte le possibili coordinate
        all_positions = [(x, y) for x in range(width) for y in range(height)]

        # 2. Mescola le posizioni
        self.random.shuffle(all_positions)

        # 3. Prendi le prime 50 posizioni uniche
        unique_positions = all_positions[:total_cells]

        # 4. Assegna agenti a posizioni uniche
        pos_index = 0
        for cell_type in immune_types:
            #print("inserico cell: ",cell_type)
            for _ in range(cells_per_type):
                #print("inserico cell position: ",cell_type)
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


    def apply_therapy_effects(self):
        print("Terapia somministrata: inizio effetto.")

        print("irl before", self.immune_response_level)
        print("tpr before", self.tumor_proliferation_rate)
        self.immune_response_level *= 1.5
        self.tumor_proliferation_rate -= 0.01
        print("irl after", self.immune_response_level)
        print("tpr after", self.tumor_proliferation_rate)


    def check_number_of_cells(self):

        counts = self.get_cells_count()
        for cell_type, counter in counts.items():
            num = counter(self)

            if num >= 200 and cell_type == "Tumor Cells" and not self.therapy_already_applied and self.activate_therapy: #and controlla anche la checkbox
                self.therapy_already_applied = True
                self.apply_therapy_effects()

            if num > self.max_number_of_cells:
                if cell_type == "Tumor Cells":

                    return False, "Paziente deceduto: crescita tumorale incontrollata."
                return False, "Simulazione terminata: paziente guarito"
            
        return True, ""

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
        #printParameters()

        if not self.patient_alive or self.schedule.time > 80 :
            self.running = False
            return  # Non continuare la simulazione

        self.schedule.step()
        self.datacollector.collect(self)

        # Check the number of each type of cell        
        check_cells, message = self.check_number_of_cells()
        if check_cells == False:
            print(message)
            self.patient_alive = False

        '''# Dynamically fetch updated slider value
        try:
            updated_therapy_value = self.activate_therapy_param.value
        except AttributeError:
            updated_therapy_value = self.activate_therapy_param

        print("Activate therapy:", updated_therapy_value)
        '''

        if self.therapy_already_applied:
            print("irl ", self.immune_response_level)
            print("tpr ", self.tumor_proliferation_rate)
