from src.wrappers.datatypes import Dict
from src.wrappers.pygame.sprite import Group
from src.app.world.calinder import Calendar
from src.app.entities.creature import Creatures


class World():
    def __init__(self, app, data=None):
        self.app = app
        self.width = 128000
        self.height = 128000
        self.data = Dict(data)
        self.data.creatures = Creatures(self.app)
        self.allObjects = Group()
        self.visableObjects = Group()



    def initWorld(self):
        self.data.calendar = Calendar()
        self.data.creatures.generate()

        self.gatherAllSprites()

    def gatherAllSprites(self):
        if len(self.allObjects):
            self.allObjects.empty()
        for creature in self.data.creatures:
            self.allObjects.add(creature)

    def getSkyColor(self):
        return self.data.calendar.data.cycles.skyColor

    def update(self):
        pass

    def tick(self):

        self.data.calendar.tick()