from src.wrappers.Datatypes import Dict
import Neuron

class Brain:
    def __init__(self, structure={}, max_layers=6):

        self.layers = Dict()
        self.max_layers  = max_layers
        for l in range(max_layers):
            self.layers[l] = Dict()
            if l in structure.keys():
                for nidx, n in structure[l].items():
                    self.layers[l][nidx] = Neuron(self, l, n.wieghts, n.bias, n.activation, n.activation_strength)

    def forward(self, inputs):
        o = []
        for lidx, l in self.layers.tiems():
            for nidx, n in l.items()
                n.fire(inputs[nidx] if lidx == 0 else None)
                if lidx == self.max_layers-1:
                    o.append(n.getValue())
        return o
