from src.wrappers.datatypes import Dict
from src.app.world.seasons import Cycles

class Calendar:
    def __init__(self, data = None):
        self.data = Dict(data)
        self.data.cycles = Cycles(self)

        self.data.time = 0
        self.data.hour = 0
        self.data.hourLength = 6

    def tick(self):
        self.data.time += 1
        if self.data.time == self.data.hourLength:
            self.data.time = 0
            self.data.hour += 1
        
        if self.data.hour >= self.data.cycles.sky.shape[0]:
            self.data.hour = 0
            
        self.data.cycles.changeColors()
        