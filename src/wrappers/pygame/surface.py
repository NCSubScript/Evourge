from pygame import Surface as pygSurface
import src.wrappers.pygame.Draw as Draw
import src.wrappers.pygame.Transform as Transform
from src.wrappers.Datatypes import *

transform = Transform.pgTransform
draw = Draw.pgDraw

class Surface(pygSurface):
    def __init__(self, area, flags=0, surface=None, data=None):
        if surface is None:
            super().__init__(area)
        else:
            super().__init__(area, flags, surface)
        self.data = Dict(data)

    def __init__(self, area = (0, 0), flags=0, depth=24, masks=None, data=None):
        if masks is None:
            super().__init__(area, flags, depth)
        else:
            super().__init__(area, flags, depth, masks)
        self.data = Dict(data)
