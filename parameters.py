# Parametri globali iniziali
GENDER = "F"        # 'M' o 'F'
BMI = 32            # Usato per modulare immunosoppressione
TUMOR_GROWTH = 1.0  # Crescita tumorale base

# Funzione helper per stimare immunosoppressione
def immunosuppression_level():
    base = 0.3 if GENDER == "M" else 0.5
    if BMI > 30:
        base += 0.2
    return min(base, 1.0)

IMMUNOSUPPRESSION = immunosuppression_level()