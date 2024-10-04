from pygame import Rect as pygRect
from src.wrappers.datatypes import *

class Rect(pygRect):
    
    def __init__(self, object, data=None):
        super().__init__(object)
        self.data = Dict(data)

    def __init__(self, left, top, width, height, data=None):
        super().__init__(left, top, width, height)
        self.data = Dict(data)

    

    
