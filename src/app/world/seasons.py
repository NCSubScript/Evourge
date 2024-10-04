from pathlib import Path
import math
import pygame

class Cycles:
    def __init__(self, calendar) -> None:
        self.seasons = Seasons()
        self.calendar = calendar

        self.path = 'assets/img/cycles/'
        self.sky = None

        self.rStep, self.bStep, self.gStep = [0, 0, 0]
        self.skyColorSteps = [0,0,0]
        self.skyColor = [0, 0, 0]

        self.loadSky()
        

    def loadSky(self):
        p = Path(self.path)
        f = p / 'default.bmp'

        if f.exists():
            self.sky = pygame.PixelArray(pygame.Surface.convert_alpha(pygame.image.load(f)))
            
            return True
        

        return False

    def changeColors(self, override = False):
        if not override:
            if self.calendar.data.time == 0:
                self.skyColor = self.intToRGB(self.sky[self.calendar.data.hour, 0])
                self.skyColorSteps = self.intToRGB(self.sky[self.calendar.data.hour, 0])
                r, g, b = self.intToRGB(self.sky[self.calendar.data.hour+1 if self.calendar.data.hour+1 < self.sky.shape[0] else 0 , 0])
                self.rStep = ((self.skyColor[0] - r) / self.calendar.data.hourLength) * -1
                self.gStep = ((self.skyColor[1] - g) / self.calendar.data.hourLength) * -1
                self.bStep = ((self.skyColor[2] - b) / self.calendar.data.hourLength) * -1

            self.skyColorSteps[0] += self.rStep
            self.skyColorSteps[1] += self.gStep
            self.skyColorSteps[2] += self.bStep
            self.skyColor = max(0, min(255, math.floor(self.skyColorSteps[0]))), max(0, min(255, math.floor(self.skyColorSteps[1]))), max(0, min(255, math.floor(self.skyColorSteps[2])))

        else:
            self.skyColor = [0, 0, 0]
        

    def intToRGB(self, color):
        Blue =  color & 255
        Green = (color >> 8) & 255
        Red =   (color >> 16) & 255        

        return [Red, Green, Blue]


class Seasons:
    def __init__(self):
        self.collection = [Spring(), Summer(), Fall(), Winter()]

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