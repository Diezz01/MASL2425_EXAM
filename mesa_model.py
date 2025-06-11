from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa_agents import ImmuneCell, TumorCell
from mesa.datacollection import DataCollector
from mesa_parameters import PatientParameters
import random


class TumorModel(Model):
    def __init__(self, patient_params: PatientParameters, width=20, height=20, initial_tumors=10,  activate_therapy=False):
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.current_id = 0
        self.patient_params = patient_params
        self.max_number_of_cells = 400
        self.patient_alive = True
        self.therapy_administrstered = 0
        self.activate_therapy = activate_therapy

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
        print("💊 Terapia somministrata: inizio effetto.")
        '''killed = 0
        for agent in list(self.schedule.agents):  # copia lista per evitare problemi
            if isinstance(agent, TumorCell):
                if random.random() < 0.5:  # 50% efficacia
                    self.grid.remove_agent(agent)
                    self.schedule.remove(agent)
                    killed += 1
        print(f"💊 Terapia somministrata: {killed} cellule tumorali rimosse.")
        self.therapy_administered = False  # Resetta il flag'''

    def check_number_of_cells(self):

        counts = self.get_cells_count()
        for cell_type, counter in counts.items():
            num = counter(self)
            print(f"{cell_type}: {num}")

            if num > self.max_number_of_cells:
                print("prova1")
                if cell_type == "Tumor Cells":
                    print("prova2")
                    return False, "Paziente deceduto: crescita tumorale incontrollata."
                return False, "Simulazione terminata: paziente guarito"
            
        return True, ""

    def step(self):
        if not self.patient_alive or self.schedule.time > 80 :
            self.running = False
            return  # Non continuare la simulazione

        self.schedule.step()
        self.datacollector.collect(self)

        # Controlla il numero di cellule         
        check_cells, message = self.check_number_of_cells()
        if check_cells == False:
            print(message)
            self.patient_alive = False

        if self.therapy_administrstered == 1:
            self.apply_therapy_effects()

        '''if self.activate_therapy:
            self.therapy_administered = True
            self.activate_therapy = False  # Resetta il bottone (è tipo trigger one-shot)'''
