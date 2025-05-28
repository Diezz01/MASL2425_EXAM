#This is the abstract class that represent a generic agent in the simulation
from abc import ABC, abstractmethod
from typing import Optional

class GenericAgent(ABC):
        def __init__(self,
                 sex: str,
                 age_group: str,
                 histology: str,
                 immune_response_level: float,
                 tumor_proliferation_rate: float,
                 therapy_type: str,
                 therapy_response_probability: float,
                 BMI: float,
                 NLR: float,
                 PD1_expression_level: float,
                 immune_exhaustion_rate: float,
                 hormonal_modulation_index: float,
                 mutation_profile: str,
                 initial_metastasis_count: int,
                 treatment_duration_days: int,
                 x_coord: int,
                 y_coord: int,
                 z_coord: int):
            self.sex = sex
            self.age_group = age_group
            self.histology = histology
            self.immune_response_level = immune_response_level
            self.tumor_proliferation_rate = tumor_proliferation_rate
            self.therapy_type = therapy_type
            self.therapy_response_probability = therapy_response_probability
            self.BMI = BMI
            self.NLR = NLR
            self.PD1_expression_level = PD1_expression_level
            self.immune_exhaustion_rate = immune_exhaustion_rate
            self.hormonal_modulation_index = hormonal_modulation_index
            self.mutation_profile = mutation_profile
            self.initial_metastasis_count = initial_metastasis_count
            self.treatment_duration_days = treatment_duration_days
            self.x_coord = x_coord
            self.y_coord = y_coord
            self.z_coord = z_coord

        @abstractmethod
        def step(self):
            """This method define the main activity of each agent"""
            pass