from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa_agents import ImmuneCell, TumorCell
from mesa.datacollection import DataCollector
from mesa_parameters import PatientParameters

class TumorModel(Model):
    def __init__(self, patient_params: PatientParameters, width=20, height=20, initial_tumors=10, immune_cells=30):
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.current_id = 0
        self.patient_params = patient_params      

        for _ in range(initial_tumors):
            x = self.random.randrange(width)
            y = self.random.randrange(height)
            self.spawn_tumor((x, y))

        # Crea cellule immunitarie
        for _ in range(immune_cells):
            x = self.random.randrange(width)
            y = self.random.randrange(height)
            cell_type = self.random.choice(["CD8", "Treg", "M1", "M2", "NK"])
            agent = ImmuneCell(self.next_id(), self, cell_type)
            self.grid.place_agent(agent, (x, y))
            self.schedule.add(agent)
        
        self.datacollector = DataCollector(
            model_reporters={
                "Tumor Cells": lambda m: sum(isinstance(a, TumorCell) for a in m.schedule.agents),
                "CD8": lambda m: sum(isinstance(a, ImmuneCell) and a.cell_type == "CD8" for a in m.schedule.agents),
                "Treg": lambda m: sum(isinstance(a, ImmuneCell) and a.cell_type == "Treg" for a in m.schedule.agents),
            }
        )
        self.datacollector.collect(self)

    def spawn_tumor(self, pos):
        tumor = TumorCell(self.next_id(), self)
        self.grid.place_agent(tumor, pos)
        self.schedule.add(tumor)

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
