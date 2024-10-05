from src.app.entities.life.Genetices import Genetics
from src.app.entities.species.Types import *
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
        
        return object


class Plants(Plant):

    def __init__(self, app, group, parent=None, data=None):
        super().__init__(app, group, parent, data)
        
class Animals(Animal):

    def __init__(self, app, group, parent=None, data=None):
        super().__init__(app, group, parent, data)