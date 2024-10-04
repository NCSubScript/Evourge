from src.app.gui.gui import GUI
from src.app.world.world import World
import math
import time
class App():
    def __init__(self) -> None:
        self.gui = GUI(self)
        self.world = World(self)
        self.now = 0
        self.pnow = time.time()
        self.lastFrame = self.pnow
        self.frameRate = 0
        self.fdt = 0.0001
        self.maxFrameRate = 0
        self.lastFrameTime = self.pnow - self.gui.fps

    def run(self) -> None:
        self.gui.initPygame()
        self.world.initWorld()

        self._running = True

        while self._running:
            self.clockFrame()
            self.running()
                


        self.onExit()

    def clockFrame(self):
        self.now = time.time()
        while self.now == self.pnow:
            self.now = time.time()
        self.dt = self.now - self.pnow
        self.maxFrameRate = 60 / self.dt / 60
        # print(f'FPS={60 / self.fdt / 60} {self.maxFrameRate=}')
        if self.now < self.lastFrameTime + (((60 / self.gui.fps) / 60) / 2):
            time.sleep((self.now + (((60 / self.gui.fps) / 60) / 2)) - self.now)
        self.pnow = self.now

    def loop(self):
        self.gui.processEvents()
        self.gui.processInputs()
        self.world.update()


    def running(self):
        self.loop()
        if self.now > self.lastFrameTime + ((60 / self.gui.fps) / 60):
            self.fdt = self.now - self.lastFrameTime
            self.lastFrameTime = time.time()
            
            self.gui.render()
            self.world.tick()

    def onExit(self) -> None:
        self.gui.close()

    def sigKill(self):
        self._running = False

    def repositionCreatures(self):
        self.world.data.creatures.genLocation()