from src.app.entities.species.Groups import *
from .life.Genetices import Genetics
from .life.neural.Brain import Brain


import random

class Species():

    def __new__(self, app, type, parent=None, group=None, data=None):
        if type == "Plantae":
            object = Plants(app, parent, group, data)
        elif type == "Animalia":
            object = Animals(app, parent, group, data)
        else:
            TypeError(f'Unknown type ({type})')

        object.sampleDNA = Genetics.generateStartingGnome(app, {0:Brain.INPUT_NEURONS, 1:Brain.OUTPUT_NEURONS})

        if data is None:
            object.data.color = [Genetics.getGeneExpression(object.sampleDNA[0]), Genetics.getGeneExpression(object.sampleDNA[1]), Genetics.getGeneExpression(object.sampleDNA[2])]
            if type == "Plantae":
                object.data.color.append(128)
            while object.data.color in app.world.reservedColors.values():
                object.data.color = [random.randint(128, 255), random.randint(128, 255), random.randint(128, 255)]

            self.generateName(object)
            self.selectStartingZone(object, app.world.rect.size)

            
        return object
    
    def generateName(object, source_file="assets/latin_words.txt"):
        f = open(source_file,  "r")
        latin_words = eval(f.read())
        f.close()
        genus = random.randint(0, len(latin_words))
        species = random.randint(0, len(latin_words))
        while species == genus:
            species = random.randint(0, len(latin_words))

        object.data.genus = str(latin_words[genus])
        object.data.species = str(latin_words[species])
        del latin_words

        object.data.name = object.data.genus + "_" + object.data.species

    def selectStartingZone(object, area):
        object.startingZone = (random.randint(int((object.zoneSize * 1.2) / 2), int(area[0] - ((object.zoneSize * 1.2) / 2))), \
                            random.randint(int((object.zoneSize * 1.2) / 2), int(area[1] - ((object.zoneSize * 1.2) / 2))))
    
    


class Plants(Plant):

    def __init__(self, app, parent=None, group=None, data=None):
        self.kingdom = "Plantae"
        self.startingPopulationSize = 200
        super().__init__(app, parent, group, data)
    
        
class Animals(Animal):

    def __init__(self, app, parent=None, group=None, data=None):
        self.kingdom = "Animalia"
        self.startingPopulationSize = 10
        self.mobility = True
        super().__init__(app, parent, group, data)

    

    