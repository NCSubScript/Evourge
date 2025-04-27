from src.wrappers.Datatypes import Dict
from src.app.entities.life.neural.Neuron import Neuron

class Brain:
    MAX_NEURONS_PER_LAYER = 20
    MAX_CONNECTIONS_PER_NEURON = 6
    INPUT_NEURONS = 4
    OUTPUT_NEURONS = 4

    def __init__(self, structure={}, max_layers=6):

        self.layers = Dict()
        self.max_layers  = max_layers
        for l in range(max_layers):
            self.layers[l] = Dict()
            if l in structure.keys():
                for nidx, n in structure[l].items():
                    n = Dict(n)
                    self.layers[l][nidx] = Neuron(self, l, n.weights, n.bias, n.activation, n.activation_strength)

    def forward(self, inputs):
        o = []
        for lidx, l in self.layers.items():
            for nidx, n in l.items():
                n.fire(inputs[nidx] if lidx == 0 else None)
                if lidx == self.max_layers-1:
                    o.append(n.getValue())
        return o
