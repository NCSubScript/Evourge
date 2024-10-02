from gui import GUI
from seasons import Cycles
from creature import Creatures
import math
import time
class App():
    def __init__(self) -> None:
        self.gui = GUI(self)
        self.cycles = None
        self.creatures = Creatures(self)
        self.pnow = time.time()
        self.lastFrame = self.pnow
        self.frameRate = 0
        self.fdt = 0.0001
        self.maxFrameRate = 0
        self.lastFrameTime = self.pnow - self.gui.fps

    def run(self) -> None:
        self.gui.initPygame()
        self.cycles = Cycles(self.gui.window.children["field"])
        self.creatures.generate()


        self._running = True
        

        while self._running:
            self.clockFrame()
            if self.now > self.lastFrameTime + ((60 / self.gui.fps) / 60):
                self.fdt = self.now - self.lastFrameTime
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
        self.cycles.changeColors()
        self.creatures.move()


    def running(self):
        self.lastFrameTime = time.time()
        self.gui.processEvents()
        self.gui.processInputs()
        self.loop()
        self.gui.render()

    def onExit(self) -> None:
        self.gui.close()

    def sigKill(self):
        self._running = False

    def repositionCreatures(self):
        self.creatures.genLocation()