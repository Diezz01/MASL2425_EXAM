from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from mesa_model import TumorModel
from mesa_agents import ImmuneCell, TumorCell
from mesa_parameters import PatientParameters

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

params = PatientParameters(
    sex="female",
    bmi=32.5,
    immune_response_level=1.4,
    tumor_proliferation_rate=0.08,
    resistance_to_therapy=0.04
)

server = ModularServer(
    TumorModel,
    [grid, chart],
    "Tumor Simulation",
    {
        "width": 20,
        "height": 20,
        "initial_tumors": 10,
        "immune_cells": 30,
        "patient_params": params
    }
)