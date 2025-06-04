class PatientParameters:
    def __init__(self, sex, bmi,
                 immune_response_level,
                 tumor_proliferation_rate,
                 resistance_to_therapy):
        self.sex = sex
        self.bmi = bmi
        self.immune_response_level = immune_response_level
        self.tumor_proliferation_rate = tumor_proliferation_rate
        self.resistance_to_therapy = resistance_to_therapy