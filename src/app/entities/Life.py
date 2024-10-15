from src.app.entities.life.Genetices import Genetics
from src.app.entities.species.Types import *
from src.wrappers.Datatypes import Dict

import random

class Life():
    
    def __new__(self, app, type, group, parent=None, data=None):
        if type == "Plantae":
            object = Plants(app, group, parent, data)
        elif type == "Animalia":
            object = Animals(app, group, parent, data)
        else:
            TypeError(f'Unknown type ({type})')

        object.parent = parent

        object.traits = Dict()
        
        
        return object


class Plants(Plant):

    def __init__(self, app, group, parent=None, data=None):
        super().__init__(app, group, parent, data)

    def defineStartingTraits(self):
        self.traits.colors = 8
        self.traits.sensors = 4 #Neural Inputs
        self.traits.actions = 4 #Neural Outputs
        
class Animals(Animal):

    def __init__(self, app, group, parent=None, data=None):
        super().__init__(app, group, parent, data)

    def defineStartingTraits(self):
        self.traits.colors = 8
        self.traits.sensors = 4 #Neural Inputs
        self.traits.actions = 4 #Neural Outputs