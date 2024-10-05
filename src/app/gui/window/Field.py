import math
import random

from pygame import PixelArray
from pygame.sprite import spritecollide, collide_rect
from pygame.locals import *

from src.wrappers.Datatypes import Dict
from src.wrappers.pygame.Surface import *
from src.wrappers.pygame.Sprite import GroupSingle, Entity
from src.wrappers.pygame.Rect import Rect
from src.LOCALS import *


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
        bgTile = Surface((56,math.ceil(32*0.866)),HIDDEN,24)

        bgTileFill = Surface((math.ceil(bgTile.get_width()/2),math.ceil(bgTile.get_height() / 2)),HIDDEN|SRCALPHA,32)

        buffer = PixelArray(bgTileFill)

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
        transform.flip(bgTileFill, True, False)
        bgTile.blit(bgTileFill, (math.ceil(bgTile.get_width() / 2), 0))
        buffer = bgTile.copy()
        transform.flip(buffer, False, True)
        bgTile.blit(buffer, (0, math.ceil(bgTile.get_height() / 2)))
        
        color = (0,0,0)
        draw.line(bgTile, color, (0, math.ceil(bgTile.get_height() / 2)), (10, math.ceil(bgTile.get_height() / 2)), 1)
        # draw.line(bgTile, color, (0, math.floor(bgTile.get_height() / 2)+1), (10, math.floor(bgTile.get_height() / 2)+1), 1)
        draw.line(bgTile, color, (10, math.floor(bgTile.get_height() / 2)), (19, 0), 1)
        draw.line(bgTile, color, (10, math.floor(bgTile.get_height() / 2)), (19, bgTile.get_height()), 1)
        draw.line(bgTile, color, (19, 0), (38, 0), 1)
        draw.line(bgTile, color, (38, 0), (47, math.floor(bgTile.get_height() / 2)), 1)
        draw.line(bgTile, color, (38, bgTile.get_height()), (47, math.floor(bgTile.get_height() / 2)), 1)
        draw.line(bgTile, color, (47, math.ceil(bgTile.get_height() / 2)), (56, math.ceil(bgTile.get_height() / 2)), 1)


        self.bgTile = bgTile.copy()

        self.update()

    def update(self):
        self.image = Surface((self.field.width, self.field.height),HIDDEN,24)

        x = 0
        while x < self.field.width:
            y = 0
            while y < self.field.height:
                self.image.blit(self.bgTile, (x, y))
                y += self.bgTile.get_height()
            x += self.bgTile.get_width()

        self.image = self.image.convert_alpha()
        self.image.set_alpha(128)

class Viewport(Entity):
    def __init__(self, group, app):
        self.app = app
        super().__init__(group)
        self.zoom = 2.5
        self.following = None

        
        self.rect = None
        self.setSize()
        self.rect = Rect(int(self.app.world.width / 2 - ((self.width * self.zoom) / 2)), int((self.app.world.height / 2) - ((self.height * self.zoom) / 2)), int(self.width * self.zoom), int(self.height * self.zoom))
        self.rect.center = (int(self.rect.left + (self.rect.width / 2)), int(self.rect.top + (self.rect.height / 2)))

    def shift(self, direction):
        self.following = None
        x, y = (0, 0)
        if direction == UP:
            y = -25 * self.zoom
            y = -min(self.rect.top, abs(y))
        if direction == DOWN:
            y = 25 * self.zoom
            y = min(self.app.world.height - (self.rect.top + self.rect.height), y)
        if direction == LEFT:
            x = -25 * self.zoom
            x = -min(self.rect.left, abs(x))
        if direction == RIGHT:
            x = 25 * self.zoom
            x = min(self.app.world.width - (self.rect.left + self.rect.width), x)

        self.rect.move_ip(x, y)

    def setSize(self, size = None):
        self.width = self.app.gui.window.width
        self.height = self.app.gui.window.height

        self.scaleRatioWidth = self.width / self.app.world.width
        self.scaleRatioWidthUp = self.app.world.width / self.width
        self.scaleRatioHeight = self.height / self.app.world.height
        self.scaleRatioHeightUp = self.app.world.height / self.height


        if self.rect is not None:
            self.rect.update(max(0, min(self.app.world.width, int(self.rect.center[0] - ((self.width * self.zoom) / 2)))), max(0, min(self.app.world.height, int(self.rect.center[1] - ((self.height * self.zoom) / 2)))), int(self.width * self.zoom), int(self.height * self.zoom))

    def scaleMousePos(self, pos):
        w = ((self.rect.center[0]) + (pos[0] * self.scaleRatioWidth))

        h = ((self.rect.center[0]) + (pos[1]  * self.scaleRatioHeight))

        return (w, h)

    def processScrollUp(self, pos):
        pos = self.scaleMousePos(pos)

        if self.zoom > 1:
            self.zoom = max(1, self.zoom - 0.5)
            # self.rect.center = pos
            self.rect.update(max(0, min(self.app.world.width, int(self.rect.center[0] - ((self.width * self.zoom) / 2)))), max(0, min(self.app.world.height, int(self.rect.center[1] - ((self.height * self.zoom) / 2)))), int(self.width * self.zoom), int(self.height * self.zoom))


    def processScrollDown(self, pos):
        pos = self.scaleMousePos(pos)

        if self.zoom < 5:
            self.zoom = min(5, self.zoom + 0.5)
            # self.rect.center = pos
            self.rect.update(max(0, min(self.app.world.width, int(self.rect.center[0] - ((self.width * self.zoom) / 2)))), max(0, min(self.app.world.height, int(self.rect.center[1] - ((self.height * self.zoom) / 2)))), int(self.width * self.zoom), int(self.height * self.zoom))



class Minimap(GroupSingle):
    def __init__(self, app):
        self.app = app
        super().__init__()

        self.visible = True

        self.fraction = 16
        self.width = max(300, self.app.gui.window.height / self.fraction)
        self.height = max(300, self.app.gui.window.height / self.fraction)
        self.lastUpdate = 0

        
        self.add(Entity(self))
        self.app.gui.clickables.left.add(self.sprite)
        self.app.gui.clickables.right.add(self.sprite)

        

        

        self.viewportFrame = GroupSingle()
        self.viewportFrame.add(Entity(self.viewportFrame))
        self.locateViewport()
        self.sprite.image = Surface((self.width, self.height), HIDDEN|SRCALPHA, 32)
        
          
    def drawImage(self):
        if self.fraction == 1:
            self.sprite.rect = Rect(self.app.gui.window.width / 2 - self.width /2, self.app.gui.window.height / 2 - self.height / 2, self.width, self.height)
            self.sprite.rect.center = (self.app.gui.window.width / 2, self.app.gui.window.height / 2)
        else:
            self.sprite.rect = Rect(0, self.app.gui.window.height - self.height, self.width, self.height)
            self.sprite.rect.center = (self.width / 2, self.app.gui.window.height - (self.height / 2))

        self.viewportFrame.sprite.image = Surface((self.viewportFrame.sprite.rect.width, self.viewportFrame.sprite.rect.height), HIDDEN|SRCALPHA, 32)
        self.viewportFrame.sprite.image.fill((0,0,0,0))
        draw.rect(self.viewportFrame.sprite.image, (255, 255, 255, 200), (0,0, self.viewportFrame.sprite.rect.width, self.viewportFrame.sprite.rect.height), 1)

    
    def viewportMoved(self, rect):
        last = self.data.viewport_rect

        if last.left != rect.left or last.top != rect.top or last.width != rect.width or last.height != rect.height or last.center[0] != rect.center[0] or last.center[1] != rect.center[1]:
            return True
        
        return False
    
    def setScaleFactors(self):
        self.scale = self.height / self.app.world.height
        self.scaleUp = self.app.world.height / self.height
    
    def locateViewport(self, force = False):
        if self.app.gui.window.children["field"].viewport.sprite.following is not None:
            self.app.gui.window.children["field"].viewport.sprite.rect.center = self.app.gui.window.children["field"].viewport.sprite.following.rect.center
            self.app.gui.window.children["field"].viewport.sprite.setSize()
        viewportRect = self.app.gui.window.children["field"].viewport.sprite.rect

        if not "viewport_rect" in self.data.previous.keys() or self.viewportMoved(viewportRect) or force:
            self.setScaleFactors()
            rect = Rect(max(0, viewportRect.left * self.scale), \
                        max(0, viewportRect.top * self.scale), \
                        max(3, viewportRect.width * self.scale), \
                        max(3, viewportRect.height * self.scale))
            rect.center = (max(1, viewportRect.center[0] * self.scale), max(1, viewportRect.center[1] * self.scale))

            self.data.change("viewport_rect", viewportRect.copy())
            
            self.viewportFrame.sprite.rect = rect

            self.drawImage()

    def render(self, display, force = False):
        self.locateViewport()
        if not self.visible:
            return

        if self.app.now - self.lastUpdate >= 2 or force == True:
            self.buffer = Surface((self.width, self.height), HIDDEN|SRCALPHA, 32)
            self.app.world.allObjects.drawMicro(self.buffer, self.scale)
            self.lastUpdate = self.app.now
        self.sprite.image.fill((0,0,0,32))
        self.sprite.image = self.buffer.copy()
        self.viewportFrame.draw(self.sprite.image)
        self.draw(display)

    def setSize(self, size):
        self.width = max(size[1] / self.fraction, 300)
        self.height = max(size[1] / self.fraction, 300)
        self.setScaleFactors()
        self.drawImage()

    def processLeftClick(self, pos):
        self.app.gui.window.children["field"].viewport.sprite.following = None
        if self.fraction == 1:
            self.app.gui.window.children["field"].moveViewportTo((max(0, min(self.app.world.width, (((pos[0] - self.sprite.rect.left) * self.scaleUp) - self.sprite.rect.center[0] * (1.125 * self.app.gui.window.children["field"].viewport.sprite.zoom)))), \
                                                                     max(0, min(self.app.world.height, ((pos[1] - self.sprite.rect.top) * self.scaleUp) - self.sprite.rect.center[1] * (1.25 * self.app.gui.window.children["field"].viewport.sprite.zoom)))))
        else:
            self.app.gui.window.children["field"].moveViewportTo((max(0, min(self.app.world.width, ((pos[0] * self.scaleUp) - self.sprite.rect.center[0]  * (4 * self.app.gui.window.children["field"].viewport.sprite.zoom)))), \
                                                                     max(0, min(self.app.world.height, ((pos[1] - self.sprite.rect.top) * self.scaleUp) - self.sprite.rect.center[1] * (1.05 * self.app.gui.window.children["field"].viewport.sprite.zoom)))))
            


    def processRightClick(self, pos):
        if self.fraction == 1:
            self.fraction = 16
        else:
            self.fraction = 1

        self.width = max(300, self.app.gui.window.height / self.fraction)
        self.height = max(300, self.app.gui.window.height / self.fraction)
        self.locateViewport(True)
        self.render(self.app.gui.display, True)


class Field(GroupSingle):
    def __init__(self, app) -> None:
        self.app = app

        super().__init__()

        self.width = self.app.gui.window.width
        self.height = self.app.gui.window.height

        self.viewport = GroupSingle()
        self.viewport.add(Viewport(self.viewport, self.app))
        self.app.gui.clickables.scrollUp.add(self.viewport.sprite)
        self.app.gui.clickables.scrollDown.add(self.viewport.sprite)

        
        self.red = 255
        self.green = 255
        self.blue = 255

        self.background = Background(self)

        self.surface = Surface((self.width, self.height), HIDDEN, 32)

        
        

    def updateBackgroundColor(self, color):
        self.red, self.green, self.blue = zip(list(color))

    def getBgColor(self):
        return self.app.world.getSkyColor()
        
    def setSize(self, size):
        self.width = max(size[0], 640)
        self.height = max(size[1], 480)

        self.viewport.sprite.setSize(size)

        self.surface = Surface((self.width, self.height), HIDDEN, 32)

    def render(self, display):
        self.surface = self.surface.convert_alpha()
        self.surface.fill(self.getBgColor())
        # self.surface.blit(self.background.image, (0,0))
        if len(self.app.world.visableObjects):
            self.app.world.visableObjects.empty()
        self.app.world.visableObjects.add(spritecollide(self.viewport.sprite, self.app.world.allObjects, False, collided=collide_rect))

        bgimage = self.background.image.copy()
        renderSurface = self.surface.copy()
        
      
        surface_size = self.surface.get_size()
        bgimage = transform.scale(bgimage, (max(surface_size[0], surface_size[0] * (5 - self.viewport.sprite.zoom)), max(surface_size[1], surface_size[1] * (5 - self.viewport.sprite.zoom))))
        bg_size = bgimage.get_size()
        renderSurface.blit(bgimage, (-(bg_size[0] - surface_size[0]),-(bg_size[1] - surface_size[1])))

        renderSurface = transform.scale(renderSurface, (self.viewport.sprite.rect.width, self.viewport.sprite.rect.height))

        if len(self.app.world.visableObjects):
            self.app.world.visableObjects.draw(renderSurface)

        renderSurface = transform.scale(renderSurface, surface_size)


        display.blit(renderSurface, (0, 0), special_flags=BLEND_RGBA_ADD)

    def moveViewportTo(self, pos):
        self.viewport.sprite.rect.update((int(pos[0]), int(pos[1])), (self.viewport.sprite.rect.width, self.viewport.sprite.rect.height))
