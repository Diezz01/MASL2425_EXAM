from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from mesa_model import TumorModel
from mesa_agents import ImmuneCell, TumorCell
from mesa_parameters import PatientParameters
from mesa.visualization.modules import TextElement
from mesa.visualization.UserParam import UserSettableParameter


class PatientStatusElement(TextElement):
    def render(self, model):
        if not model.patient_alive:
            return "⚠️ Stato: Paziente deceduto"
        else:
            return f"✅ Stato: Vivo — Cellule tumorali: {model.get_tumor_count()}"

def agent_portrayal(agent):
    portrayal = {}

    if isinstance(agent, TumorCell):
        portrayal = {
            "Shape": "circle",
            "Color": "red",
            "Filled": True,
            "r": 0.6,
            "Layer": 1
        }

    elif isinstance(agent, ImmuneCell):
        color_map = {
            "CD8": "blue",
            "Treg": "orange",
            "M1": "green",
            "M2": "purple",
            "NK": "black"
        }
        portrayal = {
            "Shape": "circle",
            "Color": color_map[agent.cell_type],
            "Filled": True,
            "r": 0.5,
            "Layer": 2
        }

    return portrayal

grid = CanvasGrid(agent_portrayal, 20, 20, 500, 500)

chart = ChartModule([
    {"Label": "Tumor Cells", "Color": "Red"},
])
#HIGH BMI means low tumor proliferation rate
#famale subject has higher tumor proliferation rate and immune response level than male
params = PatientParameters(
    sex="male",
    bmi=32.5,
    immune_response_level=0.5,
    tumor_proliferation_rate=0.08,
    resistance_to_therapy=0.04
)

params2 = PatientParameters(
    sex="female",
    bmi=25,
    immune_response_level=0.5,
    tumor_proliferation_rate=0.8,
    resistance_to_therapy=0.04
)

server = ModularServer(
    TumorModel,
    [grid, chart, PatientStatusElement()],
    "Tumor Simulation",
    {
        "width": 20,
        "height": 20,
        "initial_tumors": 10,
        "immune_cells": 30,
        "patient_params": params,
        "activate_therapy": UserSettableParameter("slider","Somministra terapia",  False, False, True, 1),
    }
)


