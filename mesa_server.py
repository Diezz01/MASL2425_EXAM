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
            return f"✅ Stato: Vivo — Cellule tumorali: {model.get_cells_count()["Tumor Cells"](model)}"

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

'''chart = ChartModule([
    {"Label": "Tumor Cells", "Color": "Red"},
])'''

chart = ChartModule([
    {"Label": "Tumor Cells", "Color": "Red"},
    {"Label": "CD8", "Color": "Blue"},
    {"Label": "Treg", "Color": "Orange"},
    {"Label": "M1", "Color": "Green"},
    {"Label": "M2", "Color": "Purple"},
    {"Label": "NK", "Color": "Black"},
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

'''params2 = PatientParameters(
    sex="female",
    bmi=25,
    immune_response_level=0.5,
    tumor_proliferation_rate=0.8,
    resistance_to_therapy=0.04
)'''


model_params = {
    "activate_therapy": UserSettableParameter("slider", "Somministrala capitano", 0, 0, 1, 1),
    "patient_sex": UserSettableParameter("checkbox", "Sex (True = Male, False = Female)", True),


    "bmi": UserSettableParameter("number", "BMI", 22.5, 10.0, 40.0, 0.1),
    "cd8": UserSettableParameter("number", "CD8", 0.04, 0.1, 1.0, 0.1), 
    "treg": UserSettableParameter("number", "Treg", 0.05, 0.1, 1.0, 0.1), 
    "nk": UserSettableParameter("number", "NK", 0.01, 0.1, 1.0, 0.1), 
    "m1": UserSettableParameter("number", "M1", 0.03, 0.1, 1.0, 0.1), 
    "m2": UserSettableParameter("number", "M2", 0.04, 0.1, 1.0, 0.1),

    "immune_response_level": UserSettableParameter("number", "Livello risposta immunitaria", 0.7),
    "tumor_proliferation_rate": UserSettableParameter("number", "Tasso proliferazione tumore", 0.1),
    "resistance_to_therapy": UserSettableParameter("number", "Resistenza alla terapia", 0.2),

    "width": 20, "height": 20,
    "initial_tumors": 10,
    "patient_params": params, 
}

grid = CanvasGrid(agent_portrayal, 20, 20, 500, 500)
server = ModularServer(TumorModel, [grid, chart, PatientStatusElement()], "RCC Model", model_params)


