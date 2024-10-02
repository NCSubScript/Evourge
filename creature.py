import random
import pygame
import math
import time

class Creatures:
    def __init__(self, app):
        self.app = app
        self.count = 50
        self.data = []

    def generate(self):
        self.count = int(math.sqrt((self.app.gui.window.children["field"].width * self.app.gui.window.children["field"].width)) / 8)
        while len(self.data) < self.count:
            self.data.append(Creature(self.app))
        
        if self.count and len(self.data) > self.count:
            del self.data[self.count:]

    def render(self, display):
        for creature in self.data:
            creature.render(display)

    def move(self):
        for creature in self.data:
            creature.move()

    def genLocation(self):
        self.generate()
        for creature in self.data:
            creature.genLocation()

class Creature:
    def __init__(self, app) -> None:
        self.app = app
        self.location = None
        self.size = random.randint(10, 45)
        self.genLocation()
        self.color = [random.randint(20, 50), random.randint(100, 150), random.randint(150, 200)]
        self.rect = None
        self.lastMove = 0
        self.mps = 10
        self.draw()

    def draw(self):
        color = self.color.copy()
        size = self.size
        location = [size, size]

        rstep = (255 - color[0]) / math.floor(size / 2)
        gstep = (255 - color[1]) / math.floor(size / 2)
        bstep = (255 - color[2]) / math.floor(size / 2)

        # display = display.convert_alpha()
        self.rect = pygame.Surface((size*2, size*2), pygame.HIDDEN, 32)

        while size > 2:
            # print(f'{color=} {location=} {size=} {rstep=} {gstep=} {bstep=}')
            pygame.draw.circle(self.rect, tuple(color), location, size)
            size -= 2
            location[0] -= 1
            location[1] -= 1
            color[0] = min(255, int(color[0] + rstep))
            color[1] = min(255, int(color[1] + gstep))
            color[2] = min(255, int(color[2] + bstep))

    def render(self, display):
         display.blit(self.rect, (self.location[0] - self.size, self.location[1] - self.size), special_flags=pygame.BLEND_RGBA_ADD)
    
    def genLocation(self):
        w = self.app.gui.window.children["field"].width
        h = self.app.gui.window.children["field"].height
        self.location = [random.randint(int(self.size), int(w-self.size)), \
                         random.randint(int(self.size), int(h-self.size))]
    
    def move(self):
        if self.app.now - self.lastMove > ((1 / 60) * (60 / self.mps)):
            self.location[0] += random.randint(-1, 1)
            self.location[0] = min(self.app.gui.window.children["field"].width-self.size, max(self.size, (self.location[0])))
            self.location[1] += random.randint(-1, 1)
            self.location[1] = min(self.app.gui.window.children["field"].height-self.size, max(self.size, (self.location[1])))
            self.lastMove = time.time()
        