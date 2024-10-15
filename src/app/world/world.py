from src.wrappers.Datatypes import Dict
from src.wrappers.pygame.Sprite import Group
from src.wrappers.pygame.Rect import Rect
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
        self.rect = Rect(0, 0, self.width, self.height)
        self.paused = False


    def initWorld(self):
        self.data.calendar = Calendar()
        self.data.creatures.generate()

        


        loadintUpdate = self.app.gui.renderLoading(f"Generateing Kingdom Plantae", 0, 0, (63, 122, 43))

        for s in range(10):
            loadintUpdate = 0
            species = Species(self.app, "Plantae", self)
            
            if species.kingdom not in self.data.objects.keys():
                self.data.objects[species.kingdom] = Dict()

            for i in range(species.startingPopulationSize):
                    loadintUpdate = self.app.gui.renderLoading(f"Generateing Species: {species.kingdom.capitalize()} {species.genus.capitalize()} {species.species.capitalize()}", i / (species.startingPopulationSize-1), loadintUpdate, species.color)
                    species.generateChild()
                    self.data.objects[species.kingdom].add(species.name, species)

        loadintUpdate = self.app.gui.renderLoading(f"Generateing Kingdom Animalia", 0, 0, (122, 63, 43))

        for s in range(10):
            loadintUpdate = 0
            species = Species(self.app, "Animalia", self)
            
            if species.kingdom not in self.data.objects.keys():
                self.data.objects[species.kingdom] = Dict()

            for i in range(species.startingPopulationSize):
                    loadintUpdate = self.app.gui.renderLoading(f"Generateing Species: {species.kingdom.capitalize()} {species.genus.capitalize()} {species.species.capitalize()}", i / (species.startingPopulationSize-1), loadintUpdate, species.color)
                    species.generateChild()
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

