from cell import GenericCell
from parameters import IMMUNOSUPPRESSION
import random

class TCell_CD8(GenericCell):
    def __init__(self):
        super().__init__("CD8+ Cytotoxic")
        self.kills = 0
    
    def act(self, environment):
        if random.random() > IMMUNOSUPPRESSION:
            if environment['tumor_cells'] > 0:
                environment['tumor_cells'] -= 1
                self.kills += 1