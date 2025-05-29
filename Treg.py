from cell import GenericCell
from CD8 import TCell_CD8
import random

class TCell_Treg(GenericCell):
    def __init__(self):
        super().__init__("Treg")
    
    def act(self, environment):
        # Inibisce altri T cell
        for cell in environment['agents']:
            if isinstance(cell, TCell_CD8) and random.random() < 0.3:
                cell.active = False