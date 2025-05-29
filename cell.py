#This is the abstract class that represent a generic agent in the simulation
from abc import ABC, abstractmethod

class GenericCell(ABC):
    def __init__(self, name):
        self.name = name
        self.active = True
    @abstractmethod
    def act(self, environment):
        pass