from cell import GenericCell

class Macrophage_M2(GenericCell):
    def __init__(self):
        super().__init__("Macrophage M2")
    
    def act(self, environment):
        environment['tumor_cells'] += 0.5  # Favorisce crescita tumorale