from GenericCell import GenericCell
import random
from TCellCD8 import TCellCD8

class TCellTreg(GenericCell):
    def __init__(self):
        super().__init__("Treg")

    def act(self, environment):
        # Inibisce altri T cell
        for cell in environment['agents']:
            if isinstance(cell, TCellCD8) and random.random() < 0.3:
                cell.active = False