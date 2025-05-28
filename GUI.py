import solara
import pandas as pd

# Starting parameters
state = solara.reactive({
    "sex": "FEMALE",
    "age_group": "50-69",
    "histology": "clear_cell",
    "immune_response_level": 0.6,
    "tumor_proliferation_rate": 0.4,
    "therapy_type": "IO+TKI",
    "therapy_response_probability": 0.3,
    "BMI": 28.5,
    "NLR": "< 4",
    "PD1_expression_level": 0.5,
    "immune_exhaustion_rate": 0.2,
    "hormonal_modulation_index": 0.4,
    "mutation_profile": "none",
    "initial_metastasis_count": 2,
    "organ_metastases": "lung",
    "treatment_duration_days": 300,
    "adverse_event_probability": 0.1,
})


def sidebar():
    solara.Title("Patient Parameters")

    solara.Select(label="Sex", values=["MALE", "FEMALE"], value=state.value["sex"], on_value=lambda v: state.value.update(sex=v))
    solara.Select(label="Age Group", values=["18-49", "50-69", "70+"], value=state.value["age_group"], on_value=lambda v: state.value.update(age_group=v))
    solara.Select(label="Histology", values=["clear_cell", "non_clear_cell", "sarcomatoid"], value=state.value["histology"], on_value=lambda v: state.value.update(histology=v))

    solara.SliderFloat(label="Immune Response Level", min=0, max=1, value=state.value["immune_response_level"], on_value=lambda v: state.value.update(immune_response_level=v))
    solara.SliderFloat(label="Tumor Proliferation Rate", min=0, max=1, value=state.value["tumor_proliferation_rate"], on_value=lambda v: state.value.update(tumor_proliferation_rate=v))
    solara.Select(label="Therapy Type", values=["IO+IO", "IO+TKI"], value=state.value["therapy_type"], on_value=lambda v: state.value.update(therapy_type=v))
    solara.SliderFloat(label="Therapy Response Probability", min=0, max=1, value=state.value["therapy_response_probability"], on_value=lambda v: state.value.update(therapy_response_probability=v))
    solara.SliderFloat(label="BMI", min=18, max=40, value=state.value["BMI"], on_value=lambda v: state.value.update(BMI=v))
    solara.Select(label="NLR", values=["< 4", "≥ 4"], value=state.value["NLR"], on_value=lambda v: state.value.update(NLR=v))
    solara.SliderFloat(label="PD1 Expression Level", min=0, max=1, value=state.value["PD1_expression_level"], on_value=lambda v: state.value.update(PD1_expression_level=v))
    solara.SliderFloat(label="Immune Exhaustion Rate", min=0, max=1, value=state.value["immune_exhaustion_rate"], on_value=lambda v: state.value.update(immune_exhaustion_rate=v))
    solara.SliderFloat(label="Hormonal Modulation Index", min=0, max=1, value=state.value["hormonal_modulation_index"], on_value=lambda v: state.value.update(hormonal_modulation_index=v))
    solara.Select(label="Mutation Profile", values=["BAP1", "KDM5C", "PBRM1", "none"], value=state.value["mutation_profile"], on_value=lambda v: state.value.update(mutation_profile=v))
    solara.SliderInt(label="Initial Metastasis Count", min=1, max=5, value=state.value["initial_metastasis_count"], on_value=lambda v: state.value.update(initial_metastasis_count=v))
    solara.SliderInt(label="Treatment Duration (days)", min=30, max=1000, value=state.value["treatment_duration_days"], on_value=lambda v: state.value.update(treatment_duration_days=v))
   
# Page content
@solara.component
def Page():
    with solara.Sidebar():
        sidebar()