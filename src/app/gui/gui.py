import pygame
import random
import math
import time
from src.wrappers.pygame.Sprite import Group
from src.wrappers.Datatypes import Dict

from src.LOCALS import *

from src.app.gui.Window import Window

class GUI():
    def __init__(self, app) -> None:
        self.app = app
        self.window = Window(self.app)
        self.clickables = Dict()
        self.clickables.left = Group()
        self.clickables.right = Group()
        self.clickables.middle = Group()
        self.clickables.scrollUp = Group()
        self.clickables.scrollDown = Group()



        
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
        self.window.children["field"].setSize(self.window.getSize())
        self.window.children["field"].background.render()
        self.activeDisplay = self.screenId
        
        pygame.display.set_caption(self.window.caption)

    def initPygame(self):
        if not self.muted:
            pygame.mixer.init()
        
        pygame.display.init()
        pygame.font.init()
        self.fonts = pygame.font.get_fonts()
        self.window.init()
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
        if key[pygame.K_w]:
            self.window.children["field"].viewport.sprite.shift(UP)
        if key[pygame.K_s]:
            self.window.children["field"].viewport.sprite.shift(DOWN)
        if key[pygame.K_a]:
            self.window.children["field"].viewport.sprite.shift(LEFT)
        if key[pygame.K_d]:
            self.window.children["field"].viewport.sprite.shift(RIGHT)

    def onEvent(self, event):
        if event.type == pygame.QUIT:
            self.app.sigKill()
        if event.type == pygame.WINDOWDISPLAYCHANGED:
            self.screenId = int(event.display_index)
        if event.type == pygame.VIDEORESIZE:
            self.window.setSize(event.w, event.h)
            self.updateDisplay()
            self.app.repositionCreatures()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.app.sigKill()
            if event.key == pygame.K_m:
                self.window.children["minimap"].visible = False if self.window.children["minimap"].visible else True
            if event.key == pygame.K_p:
                self.app.world.paused = False if self.app.world.paused else True
            

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.processLeftClick(event.pos)
            if event.button == 3:
                self.processRightClick(event.pos)
            if event.button == 4:
                self.processScrollUp(event.pos)
            if event.button == 5:
                self.processScrollDown(event.pos)

    def processLeftClick(self, pos):
        viewport = self.window.children["field"].viewport
        for item in self.clickables.left:
            if item.rect.collidepoint(pos[0], pos[1]) or item.rect.collidepoint((pos[0] * viewport.sprite.zoom) + viewport.sprite.rect.left, (pos[1] * viewport.sprite.zoom) + viewport.sprite.rect.top):
                item.processLeftClick(pos)

    def processRightClick(self, pos):
        for item in self.clickables.right:
            if item.rect.collidepoint(pos[0], pos[1]):
                item.processRightClick(pos)

    def processScrollUp(self, pos):
        for item in self.clickables.scrollUp:
            if item.rect.collidepoint(pos[0] + self.window.children["field"].viewport.sprite.rect.left, pos[1] + self.window.children["field"].viewport.sprite.rect.top):
                item.processScrollUp((pos[0], pos[1]))

    def processScrollDown(self, pos):
        for item in self.clickables.scrollDown:
            if item.rect.collidepoint(pos[0] + self.window.children["field"].viewport.sprite.rect.left, pos[1] + self.window.children["field"].viewport.sprite.rect.top):
                item.processScrollDown((pos[0], pos[1]))

    def render(self):
        # print(f'{self.window.children["field"].getBgColor()=}')
        self.display.fill((0, 0, 0, 0))
        self.window.render(self.display)
        pygame.display.flip()
        # pygame.time.Clock().tick(self.fps)

    def renderLoading(self, label, percentage, lastUpdate, color=(128, 172, 245)):
        self.app.now = time.time()
        if self.app.now  >= lastUpdate + ((60 / (self.fps) / 60) / 4):
            for event in pygame.event.get():
                self.onLodatingEvent(event)
            font = pygame.font.SysFont("impact", 24, bold=False, italic=False)
            self.display.fill((0, 0, 0, 0))

            text = font.render(f'{label}', True, color)
            textSize = font.size(f'{label}')
            center = (self.window.width / 2, self.window.height / 2)
            self.display.blit(text, (center[0] - (textSize[0] / 2), center[1] - (textSize[1] * 2)))

            if percentage:
                pygame.draw.rect(self.display, color, (int(center[0] * 0.2), center[1] + (textSize[1]), int(center[0] * 1.6), 40), width=1, border_radius=5)
                pygame.draw.rect(self.display, (int(color[0]/2), int(color[1]/2), int(color[2]/2)), (int(center[0] * 0.2) + 1, center[1] + int(textSize[1]) + 1, int((center[0] * 1.6) * percentage) - 2, 38), border_radius=5)

            pygame.display.flip()
            if self.app.devmode == False:
                time.sleep(0.00025)

            return self.app.now
        return lastUpdate
    
    def onLodatingEvent(self, event):
        if event.type == pygame.QUIT:
            self.app.sigKill()
        if event.type == pygame.WINDOWDISPLAYCHANGED:
            self.screenId = int(event.display_index)
        if event.type == pygame.VIDEORESIZE:
            self.window.setSize(event.w, event.h)
            self.updateDisplay()
            self.app.repositionCreatures()