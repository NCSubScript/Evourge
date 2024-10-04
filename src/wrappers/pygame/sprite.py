from pygame.sprite import Sprite as pygSprite, Group as pygGroup, GroupSingle as pgGroupSingle
from pygame.sprite import *
from pygame.constants import HIDDEN
from src.wrappers.pygame.rect import Rect
from src.wrappers.pygame.surface import Surface
from src.wrappers.datatypes import *

    
class Entity(pygSprite):
    def __init__(self, group, data = None):
        super().__init__(group)
        self.group = group
        self.data = Dict(data)

    def processLeftClick(self, pos):
        self.group.processLeftClick(pos)

    def processRightClick(self, pos):
        self.group.processRightClick(pos)

class MicroEntity(Entity):
    def __init__(self, group, entity, data = None):
        super().__init__(group)
        
        self.rect = Rect(entity.rect.left, entity.rect.top, 1, 1)
        self.rect.center = entity.rect.center
        self.color = entity.color
        self.surface = Surface((2, 2), HIDDEN, 24)
        self.surface.fill(self.color)

    def render(self, surface, scale):
        surface.blit(self.surface, (int(self.rect.left * scale), int(self.rect.top * scale)))

class Group(pygGroup):
    def __init__(self, group = None, data = None):
        if group is not None:
            super().__init__(group)
        else:
            super().__init__()
        
        self.data = Dict(data)

    def drawMicro(self, surface, scale):
        for sprite in self:
            sprite.minimap.sprite.render(surface, scale)

    def draw(self, surface, bgSurface=None, flags=0, override=False):
        if override:
            super().draw(surface, bgSurface, flags)
        else:
            for sprite in self.sprites():
                sprite.render(surface)

class GroupSingle(pgGroupSingle):
    def __init__(self, sprite = None, data = None):
        super().__init__(sprite)

        self.data = Dict(data)

    