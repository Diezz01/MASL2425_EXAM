from cell import GenericCell
from parameters import IMMUNOSUPPRESSION
import random


class NK(GenericCell):
    def __init__(self):
        super().__init__("NK cell")
    
    def act(self, environment):
        if random.random() > IMMUNOSUPPRESSION and environment['tumor_cells'] > 0:
            environment['tumor_cells'] -= 1