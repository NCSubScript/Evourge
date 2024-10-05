import uuid
import random

from src.wrappers.pygame.Sprite import Group as pygWrapperGroup, Entity as pygWrapperEntity, GroupSingle as pygWrapperGroupSingle, MicroEntity as pygWrapperMicroEntity
from src.wrappers.pygame.Rect import Rect
from src.wrappers.Vector import Motion



class Helper():
    def __init__(self, app, parent=None):
        self.app = app
        self.parent = parent
        self.id = uuid.uuid4()

class Group(pygWrapperGroup, Helper):
    def __init__(self, app, parent=None, sprites=None, data=None):
        Helper.__init__(self, app, parent)
        pygWrapperGroup.__init__(self, sprites, data)

class GroupSingle(pygWrapperGroupSingle, Helper):

    def __init__(self, app, parent=None, sprite=None,  data=None):
        Helper.__init__(self, app, parent)
        pygWrapperGroupSingle.__init__(self, sprite, data)


class Entity(pygWrapperEntity, Helper):
    
    def __init__(self, app, group, parent=None, data=None):
        Helper.__init__(self, app, parent)
        

        
        if data == None:
            pygWrapperEntity.__init__(self, group, data)    
            self.data.baseDNALength = 0
            self.color = tuple((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

            while self.color in self.app.world.reservedColors.values():
                self.color = tuple((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

            

            self.data.id = self.id

            self.data.rect = Rect((self.app.world.width / 2) - 5, (self.app.world.height / 2) - 5, 10,10)
            self.data.rect.center = (self.app.world.width / 2, self.app.world.height / 2)

        else:
            pygWrapperEntity.__init__(self, group, data)
            if "mobility" in self.data.keys():
                self.data.mobility = Motion(self.data.mobility)

        

    def generateColorDNA(self):
        color = ''
        color += format(random.randint(0, 255), 'b')
        color += format(random.randint(0, 255), 'b')
        color += format(random.randint(0, 255), 'b')

        return color
    
    def render(self, display):
        self.draw(display)

    def updateLocation(self):
        pass


class MicroEntity(pygWrapperMicroEntity, Helper):
    
    def __init__(self, app, group, parent, data=None):
        Helper.__init__(self, app, parent)
        pygWrapperMicroEntity.__init__(self, group, parent, data)

