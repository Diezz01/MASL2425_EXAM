import random
from tqdm import tqdm
from mesa_model import TumorModel

# Funzione per generare parametri casuali
def generate_random_params():
    return {
        "activate_therapy": random.randint(0, 1),
        "patient_sex": random.choice([True, False]),
        "bmi": round(random.uniform(10.0, 40.0), 1),
        "cd8": random.randint(1, 20),
        "treg": random.randint(1, 20),
        "nk": random.randint(1, 20),
        "m1": random.randint(1, 20),
        "m2": random.randint(1, 20),
        "tumorCells": random.randint(1, 20),
        "immune_response_level": round(random.uniform(0.0, 1.0), 2),
        "tumor_proliferation_rate": round(random.uniform(0.01, 0.2), 3),
        "resistance_to_therapy": round(random.uniform(0.0, 0.2), 3),
        "width": 20,
        "height": 20
    }

# Cancella il file esistente per evitare sovrascritture doppie

# Simulazioni
for _ in tqdm(range(200)):
    params = generate_random_params()
    model = TumorModel(**params)
    while model.running:
        model.step()
