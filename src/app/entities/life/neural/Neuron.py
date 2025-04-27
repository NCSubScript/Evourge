import numpy as np
from numpy import tanh
from src.wrappers.Datatypes import Dict
import time

def tanmoid(z):
    return sigmoid(tanh(z))

def sigmoid(z):
    return 1/(1 + np.exp(-z))

def leakyreluClamped(z, A=tuple((0.05, 1))):
    return min(A[1], leakyrelu(z, A[0]))

def reluClamped(z, A=tuple((0, 1))):
    return min(A[1], relu(z))

def relu(z):
    if isinstance(z, float):
        if z<0:
            return 0
        else:
            return z
    else:
        for i, x in enumerate(z):
            if x[0]<0:
                z[i] = 0
            else:
                z[i] = x[0]

        return z
    
def leakyrelu(z, A=tuple((0.05, 0))):
    if isinstance(z, float):
        if z<0:
            return A[0]*z
        else:
            return z
    else:
        for i, x in enumerate(z):
            if x[0]<0:
                z[i] = A[0]*x[0]
            else:
                z[i] = x[0]

        return z

class Neuron:
    

    def __init__(self, brain=None, layer=None, weights=Dict({"layers": {}}), bias=0, activation=None, activation_strength=None):
        self.brain = brain
        self.layer = layer
        self.weights = weights
        self.bias = bias
        self.activation = activation
        self.activation_strength = activation_strength
        self.value = 0
        self.previous_value = 0
        self.activated_value = 0
        self.previous_activated_value = 0

        self._fired_at = 0
        self._activated_at = 0


    def fire(self, value=None):
        self._fired_at = time.time()

        if value is None:
            self.previous_value = self.value
            self.previous_activated_value = self.activated_value
            self.value = 0
            for l in self.weights.layers:
                for lidx, neuron in l.items():
                    if lidx < self.layer:
                        self.value += self.brain.layer[lidx][neuron.key()].getValue() * neuron.value()
                    else:
                        self.value += self.brain.layer[lidx][neuron.key()].getPreviousValue() * neuron.value()

            self.value *= self.bias
        else:
            self.previous_value = self.value
            self.previous_activated_value = self.activated_value
            self.value = value
        

    def getValue(self, raw=False):
        if self.activation is None or raw is True:
            self._activated_at = time.time()
            return self.value
        else:
            if self._fired_at > self._activated_at:
                if self.activation_strength is None:
                    self.activated_value = self.actvation(self.value)
                else:
                    self.activated_value = self.actvation(self.value, self.activation_strength)
                self._activated_at = time.time()
        return self.activated_value 
            
    def getPreviousValue(self, raw=False):
        if self.activation is None or raw is True:
            return self.previous_value
        return self.previous_activated_value
