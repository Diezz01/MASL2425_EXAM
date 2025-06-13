from mesa import Agent
import random

'''proliferation_rates = {
    "CD8": 0.02,
    "Treg": 0.05,
    "M1": 0.03,
    "M2": 0.04,
    "NK": 0.01
}'''

proliferation_rates = {
    "CD8": 0.04,
    "Treg": 0.05,
    "M1": 0.03,
    "M2": 0.04,
    "NK": 0.01
}

class ImmuneCell(Agent):
    def __init__(self, unique_id, model, cell_type):
        super().__init__(unique_id, model)
        self.cell_type = cell_type
        self.active = True

    def step(self):
        # Movimento casuale
        self.random_move()

        if self.cell_type == "CD8":
            self.kill_tumor()
        elif self.cell_type == "Treg":
            self.suppress_cd8()
        elif self.cell_type == "M1":
            self.kill_tumor(slow=True)
        elif self.cell_type == "M2":
            self.promote_tumor()
        elif self.cell_type == "NK":
            self.kill_tumor()

        # immune cells proliferation
        rate = proliferation_rates[self.cell_type]
        if self.random.random() < rate:
            self.model.spawn_immune(cell_type=self.cell_type, pos=self.pos)

    
    def random_move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
    
    def kill_tumor(self, slow=False):
        eff = self.model.immune_response_level

        #if cell is not active or the probability relater to the tumor resisance is higher than the immune_response_level,
        #the cell does not kill the tumor
        if not self.active or random.random() > eff: 
            return

        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for obj in cellmates:
            if isinstance(obj, TumorCell):
                self.model.grid.remove_agent(obj)
                self.model.schedule.remove(obj)
                if slow:
                    break

    def suppress_cd8(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for obj in cellmates:
            if isinstance(obj, ImmuneCell) and obj.cell_type == "CD8":
                obj.active = False

    def promote_tumor(self):
        randomvar = self.random.random()
        threshold = self.model.tumor_proliferation_rate
        #print("Promotion check:", randomvar)
        if randomvar < threshold:
            self.model.spawn_tumor(pos=self.pos)


class TumorCell(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
    
    def step(self):
        rate = self.model.tumor_proliferation_rate
        randomvar = self.random.random()
        #print("Proliferation check:", randomvar)
        if randomvar < rate:
            self.model.spawn_tumor(pos=self.pos)