from src.app.entities.life.Genetices import Genetics
from src.app.entities.species.Types import *
import copy


import random

class Life():
    
    def __new__(self, app, type, group, parent=None, data=None):
        if type == "Plantae":
            object = Plants(app, group, parent, data)
        elif type == "Animalia":
            object = Animals(app, group, parent, data)
        else:
            TypeError(f'Unknown type ({type})')

        return object


class Plants(Plant):

    def __init__(self, app, group, parent=None, data=None):
        super().__init__(app, group, parent, data)

    def defineStartingTraits(self):
        self.traits.colors = 8
        self.traits.sensors = 4 #Neural Inputs
        self.traits.actions = 4 #Neural Outputs
        self.traits.neurons = {0: 4, 1: 0, 2: 0, 3: 0, 4: 0, 5: 4}
        self.genetics = Genetics(self)
        if not "genes" in dir(self):
            self.genetics.dna = self.genetics.generateGenes()

        self.genetics.dna = copy.deepcopy(self.parent.sampleDNA)

        for i in range(random.randint(0,3)):
            self.genetics.singleGeneMutation()


        self.genetics.dna[self.app.world.geneMap.mainColor] = Genetics.getRandomGene()
        self.genetics.dna[self.app.world.geneMap.mainColor+1] = Genetics.getRandomGene()
        self.genetics.dna[self.app.world.geneMap.mainColor+2] = Genetics.getRandomGene()
        self.genetics.dna[self.app.world.geneMap.altColor] = Genetics.getRandomGene()
        self.genetics.dna[self.app.world.geneMap.altColor+1] = Genetics.getRandomGene()
        self.genetics.dna[self.app.world.geneMap.altColor+2] = Genetics.getRandomGene()

        self.color2 = (Genetics.getGeneExpression(self.genetics.dna[self.app.world.geneMap.mainColor]), Genetics.getGeneExpression(self.genetics.dna[self.app.world.geneMap.mainColor+1]), Genetics.getGeneExpression(self.genetics.dna[self.app.world.geneMap.mainColor+2]))
        self.color3 = (Genetics.getGeneExpression(self.genetics.dna[self.app.world.geneMap.altColor]), Genetics.getGeneExpression(self.genetics.dna[self.app.world.geneMap.altColor+1]), Genetics.getGeneExpression(self.genetics.dna[self.app.world.geneMap.altColor+2]))

        self.addHighlightColors()

    
        
class Animals(Animal):

    def __init__(self, app, group, parent=None, data=None):
        super().__init__(app, group, parent, data)

    def defineStartingTraits(self):
        self.traits.colors = 8
        self.traits.sensors = 4 #Neural Inputs
        self.traits.actions = 4 #Neural Outputs
        self.traits.neurons = {0: 4, 1: 0, 2: 0, 3: 0, 4: 0, 5: 4}
        self.genetics = Genetics(self)
        if not hasattr(self, "genes"):
            self.genetics.dna = self.genetics.generateGenes()

        self.genetics.dna = copy.deepcopy(self.parent.sampleDNA)

        for i in range(random.randint(0,3)):
            self.genetics.singleGeneMutation()

        self.genetics.dna[self.app.world.geneMap.mainColor] = Genetics.getRandomGene()
        self.genetics.dna[self.app.world.geneMap.mainColor+1] = Genetics.getRandomGene()
        self.genetics.dna[self.app.world.geneMap.mainColor+2] = Genetics.getRandomGene()
        self.genetics.dna[self.app.world.geneMap.altColor] = Genetics.getRandomGene()
        self.genetics.dna[self.app.world.geneMap.altColor+1] = Genetics.getRandomGene()
        self.genetics.dna[self.app.world.geneMap.altColor+2] = Genetics.getRandomGene()

        self.color2 = (Genetics.getGeneExpression(self.genetics.dna[self.app.world.geneMap.mainColor]), Genetics.getGeneExpression(self.genetics.dna[self.app.world.geneMap.mainColor+1]), Genetics.getGeneExpression(self.genetics.dna[self.app.world.geneMap.mainColor+2]))
        self.color3 = (Genetics.getGeneExpression(self.genetics.dna[self.app.world.geneMap.altColor]), Genetics.getGeneExpression(self.genetics.dna[self.app.world.geneMap.altColor+1]), Genetics.getGeneExpression(self.genetics.dna[self.app.world.geneMap.altColor+2]))

        self.addHighlightColors()