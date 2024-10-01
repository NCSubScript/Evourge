from gui import GUI
from seasons import Cycles
from creature import Creatures
import math
class App():
    def __init__(self) -> None:
        self.gui = GUI(self)
        self.cycles = None
        self.creatures = Creatures(self)

    def run(self) -> None:
        self.gui.initPygame()
        self.cycles = Cycles(self.gui.window.children["field"])
        self.creatures.generate()


        self._running = True
        

        while self._running:
            self.running()

        self.onExit()

    def loop(self):
        self.cycles.changeColors()
        self.creatures.move()


    def running(self):
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