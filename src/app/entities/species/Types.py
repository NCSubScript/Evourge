from src.app.entities.species.common.Base import Entity, MicroEntity, GroupSingle

class Types(Entity):

    def __init__(self, app, group, parent=None, data=None):
        super().__init__(app, group, parent, data)

        self.minimap = GroupSingle(self.app, parent=self, sprite=None,  data=None)
        self.minimap.add(MicroEntity(self.minimap, self, self))

class Plant(Types):

    def __init__(self, app, group, parent=None, data=None):
        self.minimapSize = 2
        super().__init__(app, group, parent, data)
        


class Animal(Types):

    def __init__(self, app, group, parent=None, data=None):
        self.minimapSize = 8
        super().__init__(app, group, parent, data)
        