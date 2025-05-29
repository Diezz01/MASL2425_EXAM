from GenericCell import GenericCell
import random
from simulation import IMMUNOSUPPRESSION

class NK(GenericCell):
    def __init__(self):
        super().__init__("NK cell")

    def act(self, environment):
        if random.random() > IMMUNOSUPPRESSION and environment['tumor_cells'] > 0:
            environment['tumor_cells'] -= 1