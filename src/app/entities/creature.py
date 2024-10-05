import random
import pygame
import pygame.gfxdraw
import pygame.transform
import math
import time
import pygame.mask
import typing

import src.wrappers.pygame.Sprite as sprite
from src.wrappers.pygame.Sprite import Group, Entity, GroupSingle, MicroEntity



class Creatures(Group):
    def __init__(self, app):
        self.app = app
        super().__init__()
        self.count = 50
        self.data = []
        self.sizes = {}
        self.lastMove = 0
        self.mag = 0
        self.mps = 0.05
        self.sizeChanges = Group()
        self.radiusBounds = [15, 45]

    def generate(self):
        self.count = int(math.sqrt((self.app.world.width *self.app.world.width)) / 128)
        self.empty()
        self.sizes = {}
        self.sizeChanges.empty()
        self.indexID = 0
        self.lastMove = 0
        while len(self) < self.count:
            newCreature = Creature(self.app, self.indexID, self)
            self.add(newCreature)

            if newCreature.radius not in self.sizes:
                self.sizes[newCreature.radius] = Group(newCreature)
            else:
                self.sizes[newCreature.radius].add(newCreature)

            attempts = 0
            while len(pygame.sprite.spritecollide(newCreature, self.sizes[newCreature.radius], False, collided = sprite.collide_circle)) > 1:
                if newCreature in pygame.sprite.spritecollide(newCreature, self.sizes[newCreature.radius], False, collided = sprite.collide_circle):
                    newCreature.genLocation()
                    attempts += 1
                    if attempts >= 10:
                        newCreature.kill()
                        break

            
            self.indexID += 1

    def draw(self, display):
        for size in sorted(self.sizes.keys(), key=lambda d: d):
            for creature in self.sizes[size]:
                creature.render(display)
                

    def update(self, collective = True):
        for size in self.sizes:
            self.mag = math.floor(self.app.gui.fps / self.mps)
            moveX = random.randint(-1 * self.mag + 10000, self.mag+ 10000)
            moveY = random.randint(-1 * self.mag+ 10000, self.mag+ 10000)

            for creature in self.sizes[size]:
                if collective == True:
                    if self.app.now - self.lastMove > ((1 / 60) * (60 / (self.mps))):
                        creature.mag = self.mag
                        creature.moveTo[0] = math.floor(creature.location[0]) + moveX
                        creature.moveTo[1] = math.floor(creature.location[1]) + moveY
                        creature.moveTo[0] = min(self.app.world.width-(creature.radius), max(creature.radius, (creature.moveTo[0])))
                        creature.moveTo[1] = min(self.app.world.height-(creature.radius), max(creature.radius, (creature.moveTo[1])))

                        creature.moveToStep[0] = (creature.location[0] - creature.moveTo[0]) / (self.mag / 2)
                        creature.moveToStep[1] = (creature.location[1] - creature.moveTo[1]) / (self.mag / 2)
                        creature.lastMove = time.time()

                else:
                    creature.move()
                
        self.lastMove = time.time()

        if len(self.sizeChanges):
            for creature in self.sizeChanges:
                creature.kill()
                self.add(creature)
                if creature.radius not in self.sizes:
                       self.sizes[creature.radius] = Group(creature)
                else:
                    self.sizes[creature.radius].add(creature)
            
                


    def genLocation(self):
        self.generate()
        for creature in self.data:
            creature.genLocation()

class Creature(Entity):
    def __init__(self, app, id, group) -> None:
        self.app = app
        super(Creature, self).__init__(group)
        self.id = id
        self.group = group
        self.color = [random.randint(20, 50), random.randint(100, 150), random.randint(150, 200)]
        self.sizeLimits = self.group.radiusBounds
        self.radius = random.randint(self.sizeLimits[0], self.sizeLimits[1])
        self.image = None
        self.mask = None
        self.rect = None

        
        self.renderSprite()
        self.genLocation()

        self.minimap = GroupSingle()
        self.minimap.add(MicroEntity(self.minimap, self))

        self.lastMove = 0
        self.mps = 0.05
        self.location = list(self.rect.center).copy()
        self.moveTo = list(self.rect.center).copy()
        self.moveToStep = [0, 0]
        self.undulation = bool(random.randint(0, 1))
        self.undulationAmount = random.randint(92, 108) / 100

        self.app.gui.clickables.left.add(self)
        

    def deriv(self, a, b):
        return {'dx': a[0] - b[0], 'dy': a[1] - b[1]}

    def collusion(self, target):
        return True if self.calcDistance(target) <= self.radius + target.radius else False

    def calcDistance(self, target):
        der = self.deriv(target.location, self.location)
        return abs(math.sqrt((der['dx'] ** 2) + der['dy'] ** 2))

    def renderSprite(self):
        color = self.color.copy()
        color.append(32)
        size = self.radius
        location = [size+1, size+1]

        rstep = (240 - color[0]) / math.floor(size / 2)
        gstep = (240 - color[1]) / math.floor(size / 2)
        bstep = (240 - color[2]) / math.floor(size / 2)
        astep = (240 - color[3]) / math.floor(size / 2)

        # display = display.convert_alpha()
        self.image = pygame.Surface(((size*2) + 2, (size*2) + 2), pygame.HIDDEN|pygame.SRCALPHA , 32)

        while size > 2:
            # print(f'{color=} {location=} {size=} {rstep=} {gstep=} {bstep=}')
            pygame.draw.circle(self.image, tuple(color), location, size)
            size -= 2
            location[0] -= 1
            location[1] -= 1
            color[0] = min(255, int(color[0] + rstep))
            color[1] = min(255, int(color[1] + gstep))
            color[2] = min(255, int(color[2] + bstep))
            color[3] = min(255, int(color[3] + astep))
            
        color = self.color.copy()
        color.append(32)
        pygame.gfxdraw.aacircle(self.image, self.radius+1, self.radius+1, self.radius, color)
        pygame.gfxdraw.aacircle(self.image, self.radius+1, self.radius+1, self.radius-1, color)
        
        self.rect = self.image.get_rect()
        self.drawMask()
        
    def drawMask(self):
        mask = pygame.Surface(((self.radius*2) + 2, (self.radius*2) + 2), pygame.HIDDEN, 24)
        mask.fill((255, 0, 128))
        pygame.draw.circle(mask, (255,255,255), self.rect.center, self.radius)
        self.mask = pygame.mask.from_surface(mask)

    def collusionResponse(self):
        if self.radius in self.group.sizes.keys():
            collisions = pygame.sprite.spritecollide(self, self.group.sizes[self.radius], False, collided = pygame.sprite.collide_circle)
            if len(collisions):
                deflected = False
                for creature in collisions:
                    if creature.id != self.id:
                        if self.collusion(creature):
                            # if not moved:
                            if (self.moveToStep[0] < 0 and creature.moveToStep[0] > 0) or (self.moveToStep[0] > 0 and creature.moveToStep[0] < 0):
                                if deflected == False:
                                    self.moveToStep[0] *= -1
                                    self.moveToStep[0] *= 0.6
                                creature.moveToStep[0] *= -1
                                creature.moveToStep[0] *= 0.6
                            if (self.moveToStep[1] < 0 and creature.moveToStep[1] > 0) or (self.moveToStep[1] > 0 and creature.moveToStep[1] < 0):
                                if deflected == False:
                                    self.moveToStep[1] *= -1
                                    self.moveToStep[1] *= 0.6
                                creature.moveToStep[1] *= -1
                                creature.moveToStep[1] *= 0.6

                            if deflected == False:
                                if self.radius < self.group.radiusBounds[1]:
                                    alreadPoped = False
                                    if self in self.group.sizeChanges:
                                        alreadPoped = True
                                        break
                                    if not alreadPoped:
                                        self.app.world.data.creatures.sizeChanges.add(self)
                                        self.radius += 1
                                        self.renderSprite()
                            if creature.radius > self.group.radiusBounds[0]:
                                alreadPoped = False
                                if creature in self.app.world.data.creatures.sizeChanges:
                                    alreadPoped = True
                                    break
                                if not alreadPoped:
                                    self.app.world.data.creatures.sizeChanges.add(creature)
                                    creature.radius -= 1
                                    creature.renderSprite()
                                    
                        if creature.id == self.id:
                            deflected = True
                                
    def updateLocation(self):
        if (self.moveToStep[0] > 0 and self.location[0] + self.moveToStep[0] < self.app.world.width - self.radius) or (self.moveToStep[0] < 0 and self.location[0] + self.moveToStep[0] >= self.radius):
            self.location[0] += self.moveToStep[0]
        else:
            self.moveToStep[0] = -1 * self.moveToStep[0]
            self.location[0] += self.moveToStep[0]
        if (self.moveToStep[1] > 0 and self.location[1] + self.moveToStep[1] < self.app.world.height - self.radius) or (self.moveToStep[1] < 0 and self.location[1] + self.moveToStep[1] >= self.radius):
            self.location[1] += self.moveToStep[1]
        else:
            self.moveToStep[1] = -1 * self.moveToStep[1] 
            self.location[1] += self.moveToStep[1]
        self.location[0] = min(self.app.world.width-(self.radius * 1), max(self.radius, (self.location[0])))
        self.location[1] = min(self.app.world.height-(self.radius * 1), max(self.radius, (self.location[1])))


        
        self.rect.center = tuple(self.location.copy())
        self.minimap.sprite.rect.update(tuple(self.location.copy()), (1,1))


    def render(self, display):
        if not self.app.world.paused:
            self.collusionResponse()
            self.updateLocation()
                    
        size = display.get_size()
        cropped_background = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.circle(cropped_background, (255,255,255), (self.location[0] + 2, self.location[1] + 2), self.radius * 0.7)
        cropped_background.blit(display, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        scaled_background = pygame.Surface(((self.radius)*2, (self.radius)*2))
        pygame.draw.circle(scaled_background, (0,0,0), (self.location[0] + 2, self.location[1] + 2), self.radius*2)
        
        scaled_background.fill((255,0,128))
        scaled_background.blit(cropped_background, (0,0), (self.location[0]-self.radius, self.location[1]-self.radius, (self.radius)*2, (self.radius)*2))
        
        
        scaled_background = pygame.transform.scale_by(scaled_background, 1.35)
        scaled_background.set_colorkey((255,0,128))
        
        
        
        scaleBy = None
        if self.undulation == True:
            if self.undulationAmount > 1:
                scaleBy = self.undulationAmount, 2 - self.undulationAmount
            else:
                scaleBy = 2 - self.undulationAmount, self.undulationAmount
            if self.undulationAmount >= 1.12:
                self.undulation = False
        else:
            if self.undulationAmount < 1:
                scaleBy = 2 - self.undulationAmount, self.undulationAmount
            else:
                scaleBy = self.undulationAmount, 2 - self.undulationAmount
            if self.undulationAmount <= 0.88:
                self.undulation = True
                
        self.undulationAmount += 0.005 if self.undulation else -0.005
        
        scaled_background = pygame.transform.scale_by(scaled_background, list(scaleBy))
        
        scaled_image = self.image.copy()
        scaled_image = pygame.transform.scale_by(scaled_image,  list(scaleBy))
            
        
        
        display.blit(scaled_background, (((self.location[0]-self.radius*1.3)-3) - self.app.gui.window.children["field"].viewport.sprite.rect.left, ((self.location[1]-self.radius*1.3)-3) - self.app.gui.window.children["field"].viewport.sprite.rect.top))
      
        display.blit(scaled_image, ((math.floor(self.location[0]) - self.radius) - self.app.gui.window.children["field"].viewport.sprite.rect.left, (math.floor(self.location[1]) - self.radius) - self.app.gui.window.children["field"].viewport.sprite.rect.top))

    def genLocation(self):
        w = self.app.world.width
        h = self.app.world.height
        self.rect.center = (random.randint(int(self.radius), int(w-self.radius)), \
                         random.randint(int(self.radius), int(h-self.radius)))
    
    def move(self, define = False, moveStep = None):
        if define == False:
            if self.app.now - self.lastMove > ((1 / 60) * (60 / (self.mps))):
                self.mag = math.floor(self.app.gui.fps / self.mps)
                self.moveTo[0] = math.floor(self.location[0]) + random.randint(-1 * self.mag, self.mag)
                self.moveTo[1] = math.floor(self.location[1]) + random.randint(-1 * self.mag, self.mag)
                self.moveTo[0] = min(self.app.world.width-(self.radius * 1), max(self.radius, (self.moveTo[0])))
                self.moveTo[1] = min(self.app.world.height-(self.radius * 1), max(self.radius, (self.moveTo[1])))

                self.moveToStep[0] = (self.location[0] - self.moveTo[0]) / (self.mag / 2)
                self.moveToStep[1] = (self.location[1] - self.moveTo[1]) / (self.mag / 2)
                self.lastMove = time.time()

        else:
            self.moveToStep = moveStep

    def processLeftClick(self, pos):
        self.app.gui.window.children["field"].viewport.sprite.following = self
        self.app.gui.window.children["field"].viewport.sprite.rect.center = self.rect.center
        self.app.gui.window.children["field"].viewport.sprite.setSize()