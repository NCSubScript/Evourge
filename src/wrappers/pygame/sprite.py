from pygame.sprite import Sprite as pygSprite, Group as pygGroup
from pygame.sprite import *
from src.wrappers.datatypes import *

    
class Entity(pygSprite):
    def __init__(self, group, data = None):
        super().__init__(group)
        self.data = Dict(data)


class Group(pygGroup):
    def __init__(self, group = None, data = None):
        if group is not None:
            super().__init__(group)
        else:
            super().__init__()
        
        self.data = Dict(data)
