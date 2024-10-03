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

        bgTileFill = pygame.Surface((math.ceil(bgTile.get_width()/2),math.ceil(bgTile.get_height() / 2)),pygame.HIDDEN|pygame.SRCALPHA,32)

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
    def __init__(self, app) -> None:
        self.app = app
        self.width = 1000
        self.height = 1000
        self.maxWidth = 1000
        self.maxHeight = 1000
        self.red = 255
        self.green = 255
        self.blue = 255

        self.background = Background(self)

        self.surface = pygame.Surface((self.width, self.height), pygame.HIDDEN, 32)
        

    def updateBackgroundColor(self, color):
        self.red, self.green, self.blue = zip(list(color))

    def getBgColor(self):
        return (self.red, self.green, self.blue)
        
    def setSize(self, size):
        self.width = min(size[0], self.maxWidth)
        self.height = min(size[1], self.maxHeight)

        self.surface = pygame.Surface((self.width, self.height), pygame.HIDDEN, 32)

    def render(self, display):
        self.surface = self.surface.convert_alpha()
        self.surface.fill(self.getBgColor())
        self.surface.blit(self.background.image, (0,0))
        self.app.creatures.draw(self.surface)
        display.blit(self.surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

class Window():
    def __init__(self, app) -> None:
        self.app = app
        self.surfaceOptions = pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE
        self.externalWidth = 640
        self.externalHeight = 480
        self.width = 640
        self.height = 480
        self.maxWidth = 640
        self.maxHeight = 480
        self.children = {}
        self.children["field"] = Field(self.app)
        self.caption = "Evourge"

    def getSize(self, scaled = True):
        if scaled and self.getSurfaceOptions() & pygame.SCALED:
            return (self.width, self.height)
        
        return (self.externalWidth, self.externalHeight)
    
    def setSize(self, width, height):
        self.externalWidth = width
        self.externalHeight = height

        if self.externalWidth > self.maxWidth:
            self.width = self.maxWidth
        else:
            self.width = self.externalWidth

        if self.externalHeight > self.maxHeight:
            self.height = self.maxHeight
        else:
            self.height = self.externalHeight
        

        for child in self.children.values():
            child.setSize((width, height))

    def render(self, display):
        for child in self.children.values():
            child.render(display)

    def getSurfaceOptions(self):
        if (self.externalWidth > self.maxWidth) or (self.externalHeight > self.maxHeight):
            return self.surfaceOptions # |pygame.SCALED
        return self.surfaceOptions # & ~pygame.SCALED
    
class GUI():
    def __init__(self, app) -> None:
        self.app = app
        self.window = Window(self.app)
        
        self.colorDepth = 32
        self.screenId = 0
        self.activeDisplay = 0
        self.vsync = 1
        self.muted = 1
        self.display = None
        self.fps = 60

        
        
        

    def updateDisplay(self):
        
        if self.display is not None and self.window.getSurfaceOptions() != self.display.get_flags():
            pygame.display.quit()
            pygame.display.init()
        self.display = pygame.display.set_mode(size=self.window.getSize(False), flags=self.window.getSurfaceOptions(), depth=self.colorDepth, display=self.screenId, vsync=self.vsync)
        self.window.surfaceOptions = self.display.get_flags()
        print(f'{self.window.getSize(False)=} {self.window.getSurfaceOptions()=} {self.window.surfaceOptions=} {self.display.get_flags()=} {self.window.getSurfaceOptions() & self.display.get_flags()} {self.display.get_flags()=}')
        self.window.children["field"].setSize(self.window.getSize())
        self.window.children["field"].background.render()
        self.activeDisplay = self.screenId
        
        pygame.display.set_caption(self.window.caption)

    def initPygame(self):
        if not self.muted:
            pygame.mixer.init()
        
        pygame.display.init()
        pygame.font.init()
        self.updateDisplay()
        
        
    def setSurfaceOptions(self, options):
        if isinstance(options, str):
            self.window.surfaceOptions = eval(options)
        else:
            self.window.surfaceOptions = options

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
        if event.type == pygame.WINDOWDISPLAYCHANGED:
            self.screenId = int(event.display_index)
            print(f'{self.screenId=}')
        if event.type == pygame.VIDEORESIZE:
            self.window.setSize(event.w, event.h)
            self.updateDisplay()
            self.app.repositionCreatures()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.app.sigKill()
            

    def render(self):
        # print(f'{self.window.children["field"].getBgColor()=}')
        self.display.fill((0, 0, 0, 0))
        self.app.cycles.changeColors()
        self.window.render(self.display)

        pygame.display.flip()
        # pygame.time.Clock().tick(self.fps)