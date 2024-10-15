from pygame.sprite import Sprite as pygSprite, Group as pygGroup, GroupSingle as pgGroupSingle
from pygame.sprite import *
from pygame.constants import HIDDEN, SRCALPHA
from src.wrappers.pygame.Rect import Rect
from src.wrappers.pygame.Surface import Surface
from src.wrappers.Datatypes import *

    
class Entity(pygSprite, DictAccess):
    def __init__(self, group, data = None):
        pygSprite.__init__(self, group)
        self.group = group
        self.minimapSize = 2

        DictAccess.__init__(self, data)

    def processLeftClick(self, pos):
        self.group.processLeftClick(pos)

    def processRightClick(self, pos):
        self.group.processRightClick(pos)


class MicroEntity(Entity):
    def __init__(self, group, entity, data = None):

        super().__init__(group, data)
        

        self.parent = entity
        self.rect = Rect(entity.rect.left, entity.rect.top, 1, 1)
        self.rect.center = entity.rect.center
        if group.color is not None:
            self.color = group.color
        else:
            self.color = entity.color
        self.surface = Surface((entity.minimapSize, entity.minimapSize), HIDDEN|SRCALPHA, 32)
        self.surface.fill(tuple(self.color))

    def render(self, surface, scale):
        if self.parent not in self.parent.app.world.visableObjects:
            self.parent.updateLocation()
        surface.blit(self.surface, (int(self.rect.left * scale), int(self.rect.top * scale)))

class Group(pygGroup, DictAccess):
    def __init__(self, sprites = None, data = None):

        if sprites is not None:
            pygGroup.__init__(self, sprites)
        else:
            pygGroup.__init__(self)
        
        DictAccess.__init__(self, data)
        

        
        # self.data = Dict(data)

    def drawMicro(self, surface, scale):
        for sprite in self:
            sprite.minimap.sprite.render(surface, scale)

    def draw(self, surface, bgSurface=None, flags=0, override=False):
        if override:
            super().draw(surface, bgSurface, flags)
        else:
            for sprite in self.sprites():
                sprite.render(surface)

class GroupSingle(pgGroupSingle, DictAccess):
    def __init__(self, sprite = None, data = None):
        pgGroupSingle.__init__(self, sprite)

        DictAccess.__init__(self, data)



        # self.data = Dict(data)


    