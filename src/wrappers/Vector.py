import pygame.math as pgVector
from src.wrappers.Datatypes import Dict



class Motion(Dict):
    def __init__(self, position=(0, 0),  starting_velocity=(0, 0), starting_acceleration=(0, 0), acceleration=(0, 0), friction=(0, 0), data=None) -> None:
        super().__init__(data)

        if data is not None:
            self.position = position
            self.velocity = starting_velocity
            self.acceleration = starting_acceleration
            
            self.acceleration_rates = acceleration
            self.deceleration_rates = friction
        


class VectorBound():
    def setBounds(self, bounds):
        self.bounds = Bounds(bounds)

    def clamp(self):
        if hasattr(self, "bounds"):
            self = self.bounds.clamp(self)
        return ValueError("Must set boundries before calling clamp")

class Vector2(pgVector.Vector2, VectorBound):
    def __init__(self) -> None:
        return super().__init__()

class Vector3(pgVector.Vector3, VectorBound):
    def __init__(self) -> None:
        return super().__init__()


class Bounds():
    def __init__(self, vector):
        self.dimentions = []

        for element in self.dimentions:
            self.dimentions.append(Dict({"min": 0, "max": 0}))
            self.set(self.dimentions[-1], element)

    def set(self, cord, val):
        if len(val):
            if val[0] <= val[1]:
                cord.min = val[0]
                cord.max = val[1]
            else:
                cord.min = val[1]
                cord.max = val[0]
        else:
            if val > 0:
                cord.min = 0
                cord.max = val
            else:
                cord.min = val
                cord.max = 0

    def __len__(self):
        return len(self.dimentions)
    
    def clamp(self, vector: Vector2 | Vector3):
        result = vector.copy()

        parts = []
        parts.append(result.x)
        parts.append(result.y)
        if isinstance(vector, Vector3):
            parts.append(result.z)
        if len(parts) != self.dimentions:
            TypeError(f"Size Mismatch ({self.dimentions=}:vector={parts})")

        for i in range(len(vector)):
            result[i] = (min(self.dimentions[i].max, max(self.dimentions[i].min, vector[i])))
        
        return result


