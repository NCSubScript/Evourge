import uuid
import random

from src.wrappers.pygame.Sprite import Group as pygWrapperGroup, Entity as pygWrapperEntity, GroupSingle as pygWrapperGroupSingle, MicroEntity as pygWrapperMicroEntity
from src.wrappers.pygame.Rect import Rect
from src.wrappers.pygame.Surface import Surface
from src.wrappers.Vector import Motion, Vector2



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
            self.color = parent.color
           

            self.data.id = self.id

            self.data.rect = Rect((self.app.world.width / 2) - 25, (self.app.world.height / 2) - 25, 50,50)

            self.randomizeLocation()

            self.data.rect.center = (self.rect.left + (self.rect.width / 2), self.rect.top + (self.rect.height / 2))

            self.image = Surface(self.rect.size)
            self.image.fill(self.color)

        else:
            pygWrapperEntity.__init__(self, group, data)
            if "mobility" in self.data.keys():
                self.data.mobility = Motion(self.data.mobility)

    def randomizeLocation(self):
        zoneCenter = Vector2(self.parent.startingZone)
        self.rect.update(self.randomRotation(zoneCenter), self.rect.size)
        
    def randomRotation(self, point):
        center = Vector2((1,random.randint(int(-1 * self.parent.zoneSize), int(self.parent.zoneSize))))
        center += Vector2((random.randint(int(-1 * self.parent.zoneSize * 0.2), int(self.parent.zoneSize * 0.2)), random.randint(int(-1 * self.parent.zoneSize * 0.2), int(self.parent.zoneSize * 0.2))))
        center.rotate_ip(random.randint(0, 259))
        # center.x = center.y
        center += point

        return center
    def generateColorDNA(self):
        color = ''
        color += format(random.randint(0, 255), 'b')
        color += format(random.randint(0, 255), 'b')
        color += format(random.randint(0, 255), 'b')

        return color
    
    def render(self, display):
        display.blit(self.image, Vector2(self.rect.topleft) - Vector2(self.app.gui.window.children["field"].viewport.sprite.rect.topleft))

    def updateLocation(self):
        pass


class MicroEntity(pygWrapperMicroEntity, Helper):
    
    def __init__(self, app, group, parent, data=None):
        Helper.__init__(self, app, parent)
        pygWrapperMicroEntity.__init__(self, group, parent, data)

