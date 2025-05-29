from GenericCell import GenericCell

class MacrophageM2(GenericCell):
    def __init__(self):
        super().__init__("Macrophage M2")

    def act(self, environment):
        environment['tumor_cells'] += 0.5  # Favorisce crescita tumorale