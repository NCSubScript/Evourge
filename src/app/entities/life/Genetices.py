from src.wrappers.Datatypes import Dict
from .neural.Brain import Brain
import copy
import random

class Genetics(Dict):
    geneSet = [9, 0, 98, 49, 48, 8, 108, 5, 2, 75, 50, 180, 64, 72, 100, 18, 4, 192, 25, 3, 12, 162, 147, 196, 125, 20, 121, 80, 1, 169, 36, 144]

    @staticmethod
    def generateStartingGnome(app, neurons):
        dna = []

        geneMap = Dict()

        if not hasattr(app.world, "geneMap"):
            geneMap.speciesColor = 0
        #species color
        dna.extend(Genetics.getRandomColor())

        if not hasattr(app.world, "geneMap"):
            geneMap.mainColor = len(dna)

        #placeholder for individual main color
        dna.extend(Genetics.getRandomColor())

        if not hasattr(app.world, "geneMap"):
            geneMap.altColor = len(dna)

        #placeholder for individual secondary color
        dna.extend(Genetics.getRandomColor())

        if not hasattr(app.world, "geneMap"):
            geneMap.sex = len(dna)

        #sex
        dna.append(Genetics.getRandomGene())



        if not hasattr(app.world, "geneMap"):
            geneMap.brain = len(dna)

        if not hasattr(app.world, "geneMap"):
            geneMap.brainLayers = []
        #placeholder for hidden layer neurons
        for _ in range(4):
            if not hasattr(app.world, "geneMap"):
                geneMap.brainLayers.append(len(dna))
            for i in range(Brain.MAX_NEURONS_PER_LAYER):
                dna.append(1) # Index of 0 in geneSet
                for j in range(Brain.MAX_CONNECTIONS_PER_NEURON):
                    dna.extend([1, 1, 1, 1]) #layer, neuron, wieght, bias

        if not hasattr(app.world, "geneMap"):
            geneMap.brainLayers.append(len(dna))
        #output neurons connections for input neurons
        for i in range(neurons[len(neurons) - 1]):
            for j in range(Brain.MAX_CONNECTIONS_PER_NEURON):
                if random.randint(0, 1):
                    dna.extend([1, Genetics.getRandomGene(), Genetics.getRandomGene(), Genetics.getRandomGene()])
                else:
                    dna.extend([1, 1, 1, 1]) #layer, neuron, wieght, bias

        if not hasattr(app.world, "geneMap"):
            app.world.geneMap = geneMap
        return dna


    @staticmethod
    def getRandomColor():
        return [Genetics.getRandomGene(), Genetics.getRandomGene(), Genetics.getRandomGene()]


    @staticmethod
    def getRandomGene():
        return random.randint(0, len(Genetics.geneSet))
    
    @staticmethod
    def getGeneExpression(i):
        if i < len(Genetics.geneSet):
            return Genetics.geneSet[i]
        
        return 0
    
    def __init__(self, parent, clone=None, data=None):
        self.parent = parent
        super().__init__(data)

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
            self.dna = Dict(data.dna)
            self.neurslShape = Dict(data.nerualShape)

        
        

    

    def singleGeneMutation(self):
        t = random.randint(0, len(self.dna)-1)
        self.dna[t] = random.randint(0, len(Genetics.geneSet)-1)
    
    def getRandomShade(self, min=0, max=255):
        return random.randint(0, 255)
    
    
    
    def generateGenes(self):
        brainHiddenLayers = random.randint(0, 4)
        if brainHiddenLayers > 0:
            for i in range(brainHiddenLayers):
                pass