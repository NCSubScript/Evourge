
from pygame.constants import HWSURFACE, DOUBLEBUF, RESIZABLE, SCALED
from src.app.gui.window.Field import Field, Minimap

class Window():
    def __init__(self, app) -> None:
        self.app = app
        self.surfaceOptions = HWSURFACE|DOUBLEBUF|RESIZABLE
        self.externalWidth = 640
        self.externalHeight = 480
        self.width = 640
        self.height = 480
        self.maxWidth = 9999999
        self.maxHeight = 999999999
        self.children = {}
        self.caption = "Evourge"

    def init(self):
        self.children["field"] = Field(self.app)
        self.children["minimap"] = Minimap(self.app)


    def getSize(self, scaled = True):
        if scaled and self.getSurfaceOptions() & SCALED:
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
  
