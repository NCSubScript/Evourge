import random
import pygame
import math

class Creatures:
    def __init__(self, app):
        self.app = app
        self.count = 50
        self.data = []

    def generate(self):
        while len(self.data) < self.count:
            self.data.append(Creature(self.app))

    def render(self, display):
        for creature in self.data:
            creature.render(display)

    def move(self):
        for creature in self.data:
            creature.move()

    def genLocation(self):
        for creature in self.data:
            creature.genLocation()
()
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

        while size > 2:
            # print(f'{color=} {location=} {size=} {rstep=} {gstep=} {bstep=}')
            pygame.draw.circle(surface, tuple(color), location, size)
            size -= 2
            location[0] -= 1
            location[1] -= 1
            color[0] = min(255, int(color[0] + rstep))
            color[1] = min(255, int(color[1] + gstep))
            color[2] = min(255, int(color[2] + bstep))

        display.blit(surface, self.location, special_flags=pygame.BLEND_RGBA_ADD)
    
    def genLocation(self):
        w = self.app.gui.window.children["field"].width
        h = self.app.gui.window.children["field"].height
        self.location = [random.randint(int(w*0.1), w-int(w*0.1)), \
                         random.randint(int(h*0.1), h-int(h*0.1))]
    
    def move(self):
        self.location[0] += random.randint(-2, 2)
        self.location[0] = min(self.app.gui.window.children["field"].width, max(0, self.location[0]))
        self.location[1] += random.randint(-2, 2)
        self.location[1] = min(self.app.gui.window.children["field"].height, max(0, self.location[1]))
        