from src.app.entities.species.common.Base import Group
from src.app.entities.Life import Life

class Groups(Group):
    def __init__(self, app, parent=None, sprites=None, data=None):
        super().__init__(app, parent, sprites, data)

    def generateChild(self, data=None):
        self.add(Life(self.app, self.kingdom, self, self, data))

class Plant(Groups):

    def __init__(self, app, parent=None, sprites=None, data=None):
        super().__init__(app, parent, sprites, data)


class Animal(Groups):
    def __init__(self, app, parent=None, sprites=None, data=None):
        super().__init__(app, parent, sprites, data)