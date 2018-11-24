from math import sqrt, sin, cos, atan

class Vector:
    def __init__(self, x=None, y=None, r=None, theta=None):
        if x is not None and y is not None:
            self.x = x
            self.y = y
        elif r is not None and theta is not None:
            self.x = r * cos(theta)
            self.y = r * sin(theta)
        else:
            raise ValueError("Should use either 'x' and 'y' OR 'r' and 'theta'.")

    def __str__(self):
        return "<Vector x:{} y:{} r:{} theta:{}>".format(self.x, self.y, self.mag(), self.theta())
    
    def mag(self):
        return sqrt(self.x**2 + self.y**2)

    def theta(self):
        return atan(self.y/self.x)

    def add(self, other):
        return Vector(self.x+other.x, self.y+other.y)

    def to_list(self):
        return [self.x, self.y]