from src.app.entities.species.common.Base import Entity, MicroEntity, GroupSingle
from src.app.entities.life.Genetices import Genetics
from src.app.entities.life.neural.Brain import Brain
from src.wrappers.pygame.Surface import Surface, draw
from src.wrappers.pygame.Rect import Rect


from src.wrappers.Datatypes import Dict

class Types(Entity):

    def __init__(self, app, group, parent=None, data=None):
        super().__init__(app, group, parent, data)

        self.minimap = GroupSingle(self.app, parent=self, sprite=None,  data=None)
        self.minimap.add(MicroEntity(self.minimap, self, self))

        self.traits = Dict()

    # def defineStartingTraits(self):
    #     self.traits.colors = 8
    #     self.traits.sensors = 4 #Neural Inputs
    #     self.traits.actions = 4 #Neural Outputs
    #     self.genetics = Genetics(self)

        

    def initBrain(self):
        neurons = {}
        for nidx in range(len(self.genetics.nerualShape)):
            neurons[nidx] = {}
            for x in range(self.genetics.nerualShape[nidx]):
                neurons[nidx][x] = {"weights": 0.5, "bias": 1, "activation": "relu", "activation_strength": 1}
        self.brain = Brain(neurons)



    

class Plant(Types):

    def __init__(self, app, group, parent=None, data=None):
        self.minimapSize = 2
        super().__init__(app, group, parent, data)
        
    def addHighlightColors(self):
        self.data.rect2 = Rect((self.app.world.width / 2) - 21, (self.app.world.height / 2) - 21, 42,42)
        self.image2 = Surface(self.rect2.size)
        self.image2.fill(self.color2)
        draw.circle(self.image2, self.color3, (self.data.rect2.width/2, self.data.rect2.height/2), (self.data.rect2.width/2)-4)
        self.image.blit(self.image2, (4, 4))



class Animal(Types):

    def __init__(self, app, group, parent=None, data=None):
        self.minimapSize = 8
        super().__init__(app, group, parent, data)
        
    