import random
import pygame
import pygame.gfxdraw
import pygame.transform
import math
import time

class Creatures:
    def __init__(self, app):
        self.app = app
        self.count = 50
        self.data = []
        self.sizes = {}
        self.lastMove = 0
        self.mag = 0
        self.mps = 0.05
        self.sizeChanges = []

    def generate(self):
        self.count = int(math.sqrt((self.app.gui.window.children["field"].width * self.app.gui.window.children["field"].width)) / 8)
        self.data = []
        self.sizes = {}
        self.sizeChanges = []
        self.indexID = 0
        self.lastMove = 0
        while len(self.data) < self.count:
            self.data.append(Creature(self.app, self.indexID))

            if self.data[-1].size not in self.sizes:
                self.sizes[self.data[-1].size] = {}
            else:
                moved = True
                while moved == True:
                    moved = False
                    for creature in self.sizes[self.data[-1].size].values():
                        while self.data[-1].collusion(creature):
                            self.data[-1].genLocation()
                            moved = True
            
            self.sizes[self.data[-1].size][self.indexID] = self.data[-1]
            self.indexID += 1
        if self.count and len(self.data) > self.count:
            del self.data[self.count:]

    def render(self, display):
        for size in sorted(self.sizes.keys(), key=lambda d: d):
            for creature in self.sizes[size].values():
                creature.render(display)

    def move(self, collective = True):
        for size in self.sizes:
            self.mag = math.floor(self.app.gui.fps / self.mps)
            moveX = random.randint(-1 * self.mag, self.mag)
            moveY = random.randint(-1 * self.mag, self.mag)

            for creature in self.sizes[size].values():
                if collective == True:
                    if self.app.now - self.lastMove > ((1 / 60) * (60 / (self.mps))):
                        creature.mag = self.mag
                        creature.moveTo[0] = math.floor(creature.location[0]) + moveX
                        creature.moveTo[1] = math.floor(creature.location[1]) + moveY
                        creature.moveTo[0] = min(self.app.gui.window.children["field"].width-(creature.size), max(creature.size, (creature.moveTo[0])))
                        creature.moveTo[1] = min(self.app.gui.window.children["field"].height-(creature.size), max(creature.size, (creature.moveTo[1])))

                        creature.moveToStep[0] = (creature.location[0] - creature.moveTo[0]) / (self.mag / 2)
                        creature.moveToStep[1] = (creature.location[1] - creature.moveTo[1]) / (self.mag / 2)
                        creature.lastMove = time.time()
                        
                        
                else:
                    creature.move()
        self.lastMove = time.time()

        if len(self.sizeChanges):
            while len(self.sizeChanges):
                item = self.sizeChanges.pop()
                # print(f'{item=} {self.sizes[item["from"]]=}')
                creature = self.sizes[item["from"]][item["id"]]
                self.sizes[item["from"]] = {key: val for key, val in self.sizes[item["from"]].items() if key != item["id"]}
                # print(f'{creature=}')
                if not len(self.sizes[item["from"]]):
                    del self.sizes[item["from"]]
                if creature.size not in self.app.creatures.sizes:
                    self.app.creatures.sizes[creature.size] = {}
                self.sizes[creature.size][creature.id] = creature
                


    def genLocation(self):
        self.generate()
        for creature in self.data:
            creature.genLocation()

class Creature:
    def __init__(self, app, id) -> None:
        self.id = id
        self.app = app
        self.location = None
        self.maxSize = (15, 45)
        self.size = random.randint(self.maxSize[0], self.maxSize[1])
        self.genLocation()
        self.moveTo = self.location.copy()
        self.color = [random.randint(20, 50), random.randint(100, 150), random.randint(150, 200)]
        self.rect = None
        self.lastMove = 0
        self.mps = 0.05
        self.draw()
        self.moveToStep = [0, 0]

    def deriv(self, a, b):
        return {'dx': a[0] - b[0], 'dy': a[1] - b[1]}

    def collusion(self, target):
        return True if self.calcDistance(target) <= self.size + target.size else False

    def calcDistance(self, target):
        der = self.deriv(target.location, self.location)
        return abs(math.sqrt((der['dx'] ** 2) + der['dy'] ** 2))

    def draw(self):
        color = self.color.copy()
        size = self.size
        location = [size+1, size+1]

        rstep = (240 - color[0]) / math.floor(size / 2)
        gstep = (240 - color[1]) / math.floor(size / 2)
        bstep = (240 - color[2]) / math.floor(size / 2)

        # display = display.convert_alpha()
        self.rect = pygame.Surface(((size*2) + 2, (size*2) + 2), pygame.HIDDEN, 32)

        while size > 2:
            # print(f'{color=} {location=} {size=} {rstep=} {gstep=} {bstep=}')
            pygame.draw.circle(self.rect, tuple(color), location, size)
            size -= 2
            location[0] -= 1
            location[1] -= 1
            color[0] = min(255, int(color[0] + rstep))
            color[1] = min(255, int(color[1] + gstep))
            color[2] = min(255, int(color[2] + bstep))
            
        pygame.gfxdraw.aacircle(self.rect, self.size+1, self.size+1, self.size, self.color)
        pygame.gfxdraw.aacircle(self.rect, self.size+1, self.size+1, self.size-1, self.color)

    def collusionResponse(self):
        if self.size in self.app.creatures.sizes and len(self.app.creatures.sizes[self.size]) > 1:
            for creature in self.app.creatures.sizes[self.size].values():
                if creature.id != self.id:
                    if self.collusion(creature):
                        # if not moved:
                        if (self.moveToStep[0] < 0 and creature.moveToStep[0] > 0) or (self.moveToStep[0] > 0 and creature.moveToStep[0] < 0):
                            self.moveToStep[0] *= -1
                            self.moveToStep[0] *= 0.6
                            creature.moveToStep[0] *= -1
                            creature.moveToStep[0] *= 0.6
                        if (self.moveToStep[1] < 0 and creature.moveToStep[1] > 0) or (self.moveToStep[1] > 0 and creature.moveToStep[1] < 0):
                            self.moveToStep[1] *= -1
                            self.moveToStep[1] *= 0.6
                            creature.moveToStep[1] *= -1
                            creature.moveToStep[1] *= 0.6

                        if self.size < self.maxSize[1]:
                            alreadPoped = False
                            if len(self.app.creatures.sizeChanges):
                                for entry in self.app.creatures.sizeChanges:
                                    if self.id == entry["id"]:
                                        alreadPoped = True
                                        break
                            if not alreadPoped:
                                self.app.creatures.sizeChanges.append({"from": self.size, "to": self.size+1, "id": self.id})
                                self.size += 1
                                self.draw()
                        if creature.size > self.maxSize[0]:
                            alreadPoped = False
                            if len(self.app.creatures.sizeChanges):
                                for entry in self.app.creatures.sizeChanges:
                                    if creature.id == entry["id"]:
                                        alreadPoped = True
                                        break
                            if not alreadPoped:
                                self.app.creatures.sizeChanges.append({"from": creature.size, "to": creature.size-1, "id": creature.id})
                                creature.size -= 1
                                creature.draw()
                                
    def updateLocation(self):
        if (self.moveToStep[0] > 0 and self.location[0] + self.moveToStep[0] < self.app.gui.window.children["field"].width - self.size) or (self.moveToStep[0] < 0 and self.location[0] + self.moveToStep[0] >= self.size):
            self.location[0] += self.moveToStep[0]
        else:
            self.moveToStep[0] = -1 * self.moveToStep[0]
            self.location[0] += self.moveToStep[0]
        if (self.moveToStep[1] > 0 and self.location[1] + self.moveToStep[1] < self.app.gui.window.children["field"].height - self.size) or (self.moveToStep[1] < 0 and self.location[1] + self.moveToStep[1] >= self.size):
            self.location[1] += self.moveToStep[1]
        else:
            self.moveToStep[1] = -1 * self.moveToStep[1] 
            self.location[1] += self.moveToStep[1]
        self.location[0] = min(self.app.gui.window.children["field"].width-(self.size * 1), max(self.size, (self.location[0])))
        self.location[1] = min(self.app.gui.window.children["field"].height-(self.size * 1), max(self.size, (self.location[1])))
    def render(self, display):
        self.collusionResponse()
        self.updateLocation()
                        
        size = display.get_size()
        cropped_background = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.circle(cropped_background, (255,255,255), (self.location[0] + 2, self.location[1] + 2), self.size * 0.7)
        cropped_background.blit(display, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        scaled_background = pygame.Surface(((self.size)*2, (self.size)*2))
        pygame.draw.circle(scaled_background, (0,0,0), (self.location[0] + 2, self.location[1] + 2), self.size*2)
        
        scaled_background.fill((255,0,128))
        scaled_background.blit(cropped_background, (0,0), (self.location[0]-self.size, self.location[1]-self.size, (self.size)*2, (self.size)*2))
        
        
        scaled_background = pygame.transform.scale_by(scaled_background, 1.35)
        scaled_background.set_colorkey((255,0,128))
        display.blit(scaled_background, ((self.location[0]-self.size*1.3)-3, (self.location[1]-self.size*1.3)-3))
        
        
        display.blit(self.rect, (math.floor(self.location[0]) - self.size, math.floor(self.location[1]) - self.size), special_flags=pygame.BLEND_RGBA_ADD)
    
    def genLocation(self):
        w = self.app.gui.window.children["field"].width
        h = self.app.gui.window.children["field"].height
        self.location = [random.randint(int(self.size), int(w-self.size)), \
                         random.randint(int(self.size), int(h-self.size))]
    
    def move(self, define = False, moveStep = None):
        if define == False:
            if self.app.now - self.lastMove > ((1 / 60) * (60 / (self.mps))):
                self.mag = math.floor(self.app.gui.fps / self.mps)
                self.moveTo[0] = math.floor(self.location[0]) + random.randint(-1 * self.mag, self.mag)
                self.moveTo[1] = math.floor(self.location[1]) + random.randint(-1 * self.mag, self.mag)
                self.moveTo[0] = min(self.app.gui.window.children["field"].width-(self.size * 1), max(self.size, (self.moveTo[0])))
                self.moveTo[1] = min(self.app.gui.window.children["field"].height-(self.size * 1), max(self.size, (self.moveTo[1])))

                self.moveToStep[0] = (self.location[0] - self.moveTo[0]) / (self.mag / 2)
                self.moveToStep[1] = (self.location[1] - self.moveTo[1]) / (self.mag / 2)
                self.lastMove = time.time()

        else:
            self.moveToStep = moveStep