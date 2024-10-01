from gui import GUI
from seasons import Cycles
from creature import Creature
import math
class App():
    def __init__(self) -> None:
        self.gui = GUI(self)
        self.cycles = None
        self.creatures = []
        self.maxCreatures = int(math.sqrt(self.gui.window.width * self.gui.window.height) / 2)

    def run(self) -> None:
        self.gui.initPygame()
        self.cycles = Cycles(self.gui.window.children["field"])
        
        for i in range(self.maxCreatures):
            self.creatures.append(Creature(self))


        self._running = True
        

        while self._running:
            self.running()

        self.onExit()

    def loop(self):
        self.cycles.changeColors()
        for creature in self.creatures:
            creature.move()


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
        for creature in self.creatures:
            creature.genLocation()