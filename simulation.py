import agents.MacrophageM1
from agents.MacrophageM2 import MacrophageM2
from agents.NK import NK
from agents.TCellCD8 import TCellCD8
from agents.TCellTreg import TCellTreg

# Parametri globali iniziali
GENDER = "F"  # 'M' o 'F'
BMI = 32  # Usato per modulare immunosoppressione
TUMOR_GROWTH = 1.0  # Crescita tumorale base


# Funzione helper per stimare immunosoppressione
def immunosuppression_level():
    base = 0.3 if GENDER == "M" else 0.5
    if BMI > 30:
        base += 0.2
    return min(base, 1.0)


IMMUNOSUPPRESSION = immunosuppression_level()

# ======================
# Ambiente e Simulazione
# ======================

def create_environment():
    return {
        'tumor_cells': 10,
        'agents': [
            TCellCD8(), TCellCD8(),
            TCellTreg(),
            agents.Macrophage_M1.MacrophageM1(), MacrophageM2(),
            NK()
        ]
    }


def simulate(environment, steps=10):
    for step in range(steps):
        print(f"\nStep {step + 1}: Tumor Cells = {environment['tumor_cells']:.2f}")
        for agent in environment['agents']:
            if agent.active:
                agent.act(environment)
        # Crescita tumorale di base
        environment['tumor_cells'] += TUMOR_GROWTH

    print(f"\nFinal Tumor Cell Count: {environment['tumor_cells']:.2f}")
    for agent in environment['agents']:
        if isinstance(agent, TCellCD8):
            print(f"{agent.name} kills: {agent.kills}")


# ======================
# Esecuzione
# ======================

if __name__ == "__main__":
    env = create_environment()
    simulate(env, steps=15)
