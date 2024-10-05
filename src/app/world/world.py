from src.wrappers.Datatypes import Dict
from src.wrappers.pygame.Sprite import Group
from src.app.world.Calinder import Calendar
from src.app.entities.Creature import Creatures
from src.app.entities.Species import Species


class World():
    def __init__(self, app, data=None):
        self.app = app
        self.width = 128000
        self.height = 128000
        self.data = Dict(data)
        self.data.creatures = Creatures(self.app)
        self.data.objects = Dict()
        self.allObjects = Group()
        self.visableObjects = Group()
        self.reservedColors = {}

        self.paused = False


    def initWorld(self):
        self.data.calendar = Calendar()
        self.data.creatures.generate()

        
        
        species = Species(self.app, "Plantae", self)
        species.generateChild()
        if species.kindom not in self.data.objects.keys():
           self.data.objects[species.kingdom] = Dict()
        self.data.objects[species.kingdom].add(species.name, species)

        self.gatherAllSprites()

    def gatherAllSprites(self):
        if len(self.allObjects):
            self.allObjects.empty()
        for creature in self.data.creatures:
            self.allObjects.add(creature)

        for kingdomes in self.data.objects.keys():
            if kingdomes != "previous":
                for genus in self.data.objects[kingdomes].keys():
                    if genus != "previous":
                        for species in self.data.objects[kingdomes][genus]:
                            self.allObjects.add(species)


    def getSkyColor(self):
        return self.data.calendar.data.cycles.skyColor

    def update(self):
        if not self.paused:
            self.data.creatures.update()

    def tick(self):
        if not self.paused:
            self.data.calendar.tick()

