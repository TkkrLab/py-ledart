import operator
import math


class Vector(object):
    def __init__(self, **axes):
        super(Vector, self).__setattr__('axes', axes)

    def magnitude(self):
        """ for every N square it, sum list. take square root. """
        magnitude = sum([(self.axes[axis] * self.axes[axis]) for axis in self.axes]) ** 0.5
        return magnitude

    def set_mag(self, mag):
        self = self.normalize()
        self *= mag

    def dist(self, other):
        deltas = [(self.axes[axis] - other.axes[axis]) ** 2 for axis in self.axes]
        return abs(sum(deltas)) ** 0.5

    def normalize(self):
        m = self.magnitude()
        if m:
            return self / m

        return self * 0

    def limit(self, lim):
        if self.mag > lim:
            self = self.normalize()
            self *= lim
        return Vector(**self.axes)

    def heading(self):
        pass

    def rotate(self):
        pass

    def lerp(self):
        pass

    def angleBetween(self):
        pass

    def dot(self):
        pass

    def cross(self):
        pass

    def randomVec(self):
        pass

    def __operation__(self, op, val):
        result = {}
        if isinstance(val, (int, float)):
            for axis in self.axes:
                result[axis] = op(self.axes[axis], val)
        elif isinstance(val, Vector):
            for axis in self.axes:
                result[axis] = op(self.axes[axis], val.axes[axis])
        else:
            raise TypeError
        return Vector(**result)

    def __add__(self, val):
        return self.__operation__(operator.add, val)

    def __sub__(self, val):
        return self.__operation__(operator.sub, val)

    def __mul__(self, val):
        return self.__operation__(operator.mul, val)

    def __div__(self, val):
        return self.__operation__(operator.div, val)

    def __len__(self):
        return self.mag

    def __getattr__(self, attr):
        if attr in self.axes:
            return self.axes[attr]
        elif attr == 'mag':
            return self.magnitude()
        else:
            raise AttributeError

    def __setattr__(self, attr, value):
        if attr in self.axes:
            self.axes[attr] = value
        elif attr == 'mag':
            self.set_mag(value)
        else:
            raise KeyError

    def __str__(self):
        values = {}
        values.update(self.axes)
        values['mag'] = self.mag
        return str(values)
