from src.app.entities.species.common.Base import Group
from src.app.entities.Life import Life


class Groups(Group):
    def __init__(self, app, parent=None, sprites=None, data=None):
        super().__init__(app, parent, sprites, data)

    def generateChild(self, data=None):
        child = Life(self.app, self.kingdom, self, self, data)
        child.defineStartingTraits()
        child.initBrain()


        self.add(child)


class Plant(Groups):

    def __init__(self, app, parent=None, sprites=None, data=None):
        super().__init__(app, parent, sprites, data)

        self.zoneSize = 30000


class Animal(Groups):
    def __init__(self, app, parent=None, sprites=None, data=None):
        super().__init__(app, parent, sprites, data)

        self.zoneSize = 2000