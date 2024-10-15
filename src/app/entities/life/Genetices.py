from src.wrappers.Datatypes import Dict
import copy
import random

class Genetics(Dict):
    def __init__(self, parent, clone=None, data=None):
        self.parent = parent
        super().__init__(data)

        self.geneSet = [9, 0, 98, 49, 81, 16, 48, 8, 108, 5, 2, 32, 75, 50, 180, 64, 72, 100, 18, 4, 192, 25, 3, 12, 162, 147, 196, 125, 20, 121, 45, 128, 27, 80, 1, 169, 36, 144]

        if data is None:
            self.dna = Dict()
            self.nerualShape = parent.traits.neurons
            

            if clone is None:
                self.dna = Dict()
                self.structure = Dict()
            else:
                self.dna = copy.deepcopy(clone.dna)
                self.structure = copy.deepcopy(clone.structure)
                
        else:
            self.dna = Dict(self.dna)
            self.neurslShape = Dict(self.nerualShape)

    

    def getRandomColor(self, min=0, max=255):
        return tuple(self.getRandomShade(min, max), self.getRandomShade(min, max), self.getRandomShade(min, max))
    
    def getRandomShade(self, min=0, max=255):
        return random.randint(0, 255)