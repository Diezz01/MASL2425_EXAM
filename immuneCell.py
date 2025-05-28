#this class represent the tumor cell in rcc
from cell import GenericAgent

class ImmuneCell(GenericAgent):
    def __init__(self, sex, age_group, histology, immune_response_level, tumor_proliferation_rate, therapy_type, therapy_response_probability, BMI, NLR, PD1_expression_level, immune_exhaustion_rate, hormonal_modulation_index, mutation_profile, initial_metastasis_count, treatment_duration_days, x_coord, y_coord, z_coord):
        super().__init__(sex, age_group, histology, immune_response_level, tumor_proliferation_rate, therapy_type, therapy_response_probability, BMI, NLR, PD1_expression_level, immune_exhaustion_rate, hormonal_modulation_index, mutation_profile, initial_metastasis_count, treatment_duration_days, x_coord, y_coord, z_coord)
    
    def step():
        #TODO: develop the step function of the Immune cell
        pass