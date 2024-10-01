import pygame
import random
import math

class Background():
    def __init__(self, field):
        self.field = field
        self.bgTile = None
        self.image = None

    def intToRGB(self, color):
        Blue =  color & 255
        Green = (color >> 8) & 255
        Red =   (color >> 16) & 255        

        return [Red, Green, Blue]

    def render(self):
        bgTile = pygame.Surface((56,math.ceil(32*0.866)),pygame.HIDDEN,24)

        bgTileFill = pygame.Surface((math.ceil(bgTile.get_width()/2),math.ceil(bgTile.get_height() / 2)),pygame.HIDDEN,24)

        buffer = pygame.PixelArray(bgTileFill)

        for x in range(bgTileFill.get_height()):
            for y in range(bgTileFill.get_width()):
                colorRoot = random.randint(40, 60)
                color = (colorRoot + random.randint(-4,4), colorRoot + random.randint(-4,4), colorRoot + random.randint(-4,4))
                if x % 2 == 0 and y % 2 != 0 or x % 2 != 0 and y % 2 == 0:
                    buffer[y, x] = color

        for x in range(bgTileFill.get_width()):
            for y in range(bgTileFill.get_height()):
                color = 0
                pixels = 0
                if x % 2 == 0 and y % 2 == 0 or x % 2 != 0 and y % 2 != 0:
                    if x-1 >= 0:
                        pixels += 1
                        color += sum(self.intToRGB(buffer[x-1, y]))
                    if x+1 < bgTileFill.get_width():
                        pixels += 1
                        color += sum(self.intToRGB(buffer[x+1, y]))
                    if y-1 >= 0:
                        pixels += 1
                        color += sum(self.intToRGB(buffer[x, y-1]))
                    if y+1 < bgTileFill.get_height():
                        pixels += 1
                        color += sum(self.intToRGB(buffer[x, y+1]))


                    buffer[x, y] = int(color / (pixels + (pixels * 3)))

        buffer.close()

        bgTile.blit(bgTileFill, (0,0))
        pygame.transform.flip(bgTileFill, True, False)
        bgTile.blit(bgTileFill, (math.ceil(bgTile.get_width() / 2), 0))
        buffer = bgTile.copy()
        pygame.transform.flip(buffer, False, True)
        bgTile.blit(buffer, (0, math.ceil(bgTile.get_height() / 2)))
        
        color = (0,0,0)
        pygame.draw.line(bgTile, color, (0, math.ceil(bgTile.get_height() / 2)), (10, math.ceil(bgTile.get_height() / 2)), 1)
        # pygame.draw.line(bgTile, color, (0, math.floor(bgTile.get_height() / 2)+1), (10, math.floor(bgTile.get_height() / 2)+1), 1)
        pygame.draw.line(bgTile, color, (10, math.floor(bgTile.get_height() / 2)), (19, 0), 1)
        pygame.draw.line(bgTile, color, (10, math.floor(bgTile.get_height() / 2)), (19, bgTile.get_height()), 1)
        pygame.draw.line(bgTile, color, (19, 0), (38, 0), 1)
        pygame.draw.line(bgTile, color, (38, 0), (47, math.floor(bgTile.get_height() / 2)), 1)
        pygame.draw.line(bgTile, color, (38, bgTile.get_height()), (47, math.floor(bgTile.get_height() / 2)), 1)
        pygame.draw.line(bgTile, color, (47, math.ceil(bgTile.get_height() / 2)), (56, math.ceil(bgTile.get_height() / 2)), 1)


        self.bgTile = bgTile.copy()

        self.update()

    def update(self):
        self.image = pygame.Surface((self.field.width, self.field.height),pygame.HIDDEN,24)

        x = 0
        while x < self.field.width:
            y = 0
            while y < self.field.height:
                self.image.blit(self.bgTile, (x, y))
                y += self.bgTile.get_height()
            x += self.bgTile.get_width()

        self.image = self.image.convert_alpha()
        self.image.set_alpha(128)




class Field():
    def __init__(self) -> None:
        self.width = 1027
        self.height = 768
        self.red = 255
        self.green = 255
        self.blue = 255

    def updateBackgroundColor(self, color):
        self.red, self.green, self.blue = zip(list(color))

    def getBgColor(self):
        return (self.red, self.green, self.blue)
        
    def setSize(self, size):
        self.width = size[0]
        self.height = size[1]

class Window():
    def __init__(self) -> None:
        self.width = 1027
        self.height = 768
        self.children = {}

    def getSize(self):
        return (self.width, self.height)
    
    def setSize(self, width, height):
        self.width = width
        self.height = height

class GUI():
    def __init__(self, app) -> None:
        self.app = app
        self.window = Window()
        self.surfaceOptions = pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE
        self.colorDepth = 32
        self.screenId = 0
        self.vsync = 1
        self.muted = 1
        self.display = None
        self.fps = 30
        self.window.children["field"] = Field()
        self.background = Background(self.window.children["field"])
        

    def updateDisplay(self):
        self.display = pygame.display.set_mode(self.window.getSize(), self.surfaceOptions, self.colorDepth, self.screenId, self.vsync)
        self.window.children["field"].setSize(self.window.getSize())

    def initPygame(self):
        if not self.muted:
            pygame.mixer.init()
        
        pygame.display.init()
        pygame.font.init()
        self.updateDisplay()
        self.background.render()
        
    def setSurfaceOptions(self, options):
        if isinstance(options, str):
            self.surfaceOptions = eval(options)
        else:
            self.surfaceOptions = options

    def close(self):
        pygame.quit()

    def processEvents(self):
        for event in pygame.event.get():
            self.onEvent(event)

    def processInputs(self):
        key = pygame.key.get_pressed()

    def onEvent(self, event):
        if event.type == pygame.QUIT:
            self.app.sigKill()
        if event.type == pygame.VIDEORESIZE:
            self.window.setSize(event.w, event.h)
            self.updateDisplay()
            self.background.update()
            self.app.repositionCreatures()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.app.sigKill()
            

    def render(self):
        # print(f'{self.window.children["field"].getBgColor()=}')
        self.display.fill(self.window.children["field"].getBgColor())
        self.display.blit(self.background.image, (0,0))

        for creature in self.app.creatures:
            creature.render(self.display)

        pygame.display.flip()
        pygame.time.Clock().tick(self.fps)