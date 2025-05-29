from GenericCell import GenericCell


class MacrophageM1(GenericCell):
    def __init__(self):
        super().__init__("Macrophage M1")

    def act(self, environment):
        if environment['tumor_cells'] > 0:
            environment['tumor_cells'] -= 0.5  # Meno efficace dei CD8+
