from pathlib import Path
import math
import pygame

class Cycles:
    def __init__(self, world) -> None:
        self.world = world
        self.seasons = Seasons()

        self.path = 'assets/img/cycles/'
        self.sky = None

        self.time = 0
        self.hour = 0
        self.rStep, self.bStep, self.gStep = [0, 0, 0]
        self.skyColor = [0, 0, 0]
        self.hourLength = 6

        self.loadSky()
        

    def loadSky(self):
        p = Path(self.path)
        f = p / 'default.bmp'

        if f.exists():
            self.sky = pygame.PixelArray(pygame.Surface.convert_alpha(pygame.image.load(f)))
            
            return True
        

        return False

    def changeColors(self, override = True):
        if not override:
            if self.time == 0:
                self.world.red, self.world.green, self.world.blue = self.intToRGB(self.sky[self.hour, 0])
                self.skyColor = [self.world.red, self.world.green, self.world.blue]
                r, g, b = self.intToRGB(self.sky[self.hour+1 if self.hour+1 < self.sky.shape[0] else 0 , 0])
                self.rStep = ((self.world.red - r) / self.hourLength) * -1
                self.gStep = ((self.world.green - g) / self.hourLength) * -1
                self.bStep = ((self.world.blue - b) / self.hourLength) * -1

            self.skyColor[0] += self.rStep
            self.skyColor[1] += self.gStep
            self.skyColor[2] += self.bStep
            self.world.red = max(0, min(255, math.floor(self.skyColor[0])))
            self.world.green = max(0, min(255, math.floor(self.skyColor[1])))
            self.world.blue = max(0, min(255, math.floor(self.skyColor[2])))

            self.time += 1
            if self.time == self.hourLength:
                self.time = 0
                self.hour += 1
            
            if self.hour >= self.sky.shape[0]:
                self.hour = 0
        else:
            self.world.red = 0
            self.world.green = 0
            self.world.blue = 0
        

    def intToRGB(self, color):
        Blue =  color & 255
        Green = (color >> 8) & 255
        Red =   (color >> 16) & 255        

        return [Red, Green, Blue]


class Seasons:
    def __init__(self):
        self.collection = [Spring(), Summer(), Winter(), Fall()]

class Season:
    def __init__(self):
        self.duration = 90
        self.name = type(self).__name__

class Winter(Season):
    def __init__(self):
        super(Winter, self).__init__()

class Summer(Season):
    def __init__(self):
        super(Summer, self).__init__()

class Fall(Season):
    def __init__(self):
        super(Fall, self).__init__()

class Spring(Season):
    def __init__(self):
        super(Spring, self).__init__()