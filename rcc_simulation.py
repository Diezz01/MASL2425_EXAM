from parameters import *
from CD8 import TCell_CD8
from M1 import Macrophage_M1
from M2 import Macrophage_M2
from NK import NK
from Treg import TCell_Treg




# ======================
# Ambiente e Simulazione
# ======================

def create_environment():
    return {
        'tumor_cells': 10,
        'agents': [
            TCell_CD8(), TCell_CD8(),
            TCell_Treg(),
            Macrophage_M1(), Macrophage_M2(),
            NK()
        ]
    }

def simulate(environment, steps):
    for step in range(steps):
        print(f"\nStep {step+1}: Tumor Cells = {environment['tumor_cells']:.2f}")
        for agent in environment['agents']:
            if agent.active:
                agent.act(environment)
        # Crescita tumorale di base
        environment['tumor_cells'] += TUMOR_GROWTH

    print(f"\nFinal Tumor GenericCell Count: {environment['tumor_cells']:.2f}")
    for agent in environment['agents']:
        if isinstance(agent, TCell_CD8):
            print(f"{agent.name} kills: {agent.kills}")

# ======================
# Esecuzione
# ======================

env = create_environment()
simulate(env, steps=10)