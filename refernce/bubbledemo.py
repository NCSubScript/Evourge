import random
import pygame
import math

class Creature:
    def __init__(self, app) -> None:
        self.app = app
        self.location = None
        self.genLocation()
        self.color = [random.randint(20, 50), random.randint(100, 150), random.randint(150, 200)]
        self.size = random.randint(10, 45)

    def render(self, display):
        
        color = self.color.copy()
        size = self.size
        location = [size, size]

        rstep = (255 - color[0]) / math.floor(size / 2)
        gstep = (255 - color[1]) / math.floor(size / 2)
        bstep = (255 - color[2]) / math.floor(size / 2)

        # display = display.convert_alpha()
        surface = pygame.Surface((size*2, size*2), pygame.HIDDEN, 32)
        surface = surface.convert_alpha()
        surface.fill((0, 0, 0, 255))

        while size > 2:
            # print(f'{color=} {location=} {size=} {rstep=} {gstep=} {bstep=}')
            pygame.draw.circle(surface, tuple(color), location, size)
            size -= 2
            location[0] -= 1
            location[1] -= 1
            color[0] = min(255, int(color[0] + rstep))
            color[1] = min(255, int(color[1] + gstep))
            color[2] = min(255, int(color[2] + bstep))

        display.blit(surface, self.location, special_flags=pygame.BLEND_MAX)
    
    def genLocation(self):
        self.location = [random.randint(200, self.app.gui.window.children["field"].width-200), \
                         random.randint(200, self.app.gui.window.children["field"].height-200)]
    
    def move(self):
        self.location[0] += random.randint(-2, 2)
        self.location[0] = min(self.app.gui.window.children["field"].width, max(0, self.location[0]))
        self.location[1] += random.randint(-2, 2)
        self.location[1] = min(self.app.gui.window.children["field"].height, max(0, self.location[1]))
        