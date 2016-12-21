from Ledart import Graphics, BLACK, BLUE
from colorsys import hsv_to_rgb
import operator
import random
import math

class Vector(object):
    def __init__(self, **axes):
        super(Vector, self).__setattr__('axes', axes)

    def mag(self):
        """ for every N square it, sum list. take square root. """
        magnitude = sum([(self.axes[axis] * self.axes[axis]) for axis in self.axes]) ** 0.5
        return magnitude

    def dist(self, other):
        return 0

    def __operation__(self, op, val):
        result = {}
        if isinstance(val, (int, float)):
            pass
        elif isinstance(val, Vector):
            pass
        return Vector(**result)

    def __add__(self, val):
        return self.__operation__(operator.add, val)
        # result = {}
        # if isinstance(val, (int, float)):
        #     for axis in self.axes:
        #         result[axis] = self.axes[axis] + val
        # elif isinstance(val, Vector):
        #     for axis in self.axes:
        #         result[axis] = self.axes[axis] + val.axes[axis]
        # return Vector(**result)

    def __sub__(self, val):
        result = {}
        if isinstance(val, (int, float)):
            for axis in self.axes:
                result[axis] = self.axes[axis] - val
        elif isinstance(val, Vector):
            for axis in self.axes:
                result[axis] = self.axes[axis] - val.axes[axis]
        return Vector(**result)

    def __mul__(self, val):
        pass

    def __div__(self, val):
        pass

    def __len__(self):
        return self.mag()

    def __getattr__(self, attr):
        if attr in self.axes:
            return self.axes[attr]
        elif attr == 'mag':
            return self.mag()
        else:
            raise AttributeError

    def __setattr__(self, attr, value):
        if attr in self.axes:
            self.axes[attr] = value
        else:
            raise KeyError

    def __str__(self):
        values = {}
        values.update(self.axes)
        values['mag'] = self.mag()
        return str(values)


class Ball(object):
    def __init__(self, g=None, x=0, y=0, size=1):
        self.accel = Vector(x=0, y=0)
        self.speed = Vector(x=3, y=4, z=5)
        print(self.speed)
        self.pos = Vector(x=x, y=y)
        self.size = size
        self.g = g

    def update(self):
        self.pos += self.speed

        if (self.pos.x - self.size < 0 or
            self.pos.x > self.g.width - self.size):
            self.speed.x *= -1
        if (self.pos.y - self.size < 0 or 
            self.pos.y > self.g.height - self.size):
            self.speed.y *= -1

    def draw(self):
        self.g.draw_circle(self.pos.x, self.pos.y, self.size, BLUE)


class MetaBalls(Graphics):
    def __init__(self, **kwargs):
        Graphics.__init__(self, **kwargs)
        self.balls = []
        for i in range(1):
            size = random.randint(4, 10)
            x = random.randint(size, self.width - size)
            y = random.randint(size, self.height - size)
            ball = Ball(g=self, x=x, y=y, size=size)
            ball.speed += 0.4
            self.balls.append(ball)
 
    def generate(self):
        self.fill(BLACK)

        start = Vector(x=10, y = 20)
        middle = Vector(x=self.width/2, y=self.height/2)
        subtract = middle - start

        self.draw_line(subtract.x, subtract.y, middle.x, middle.y, BLUE)

        # for ball in self.balls:
        #     ball.update()
        #     ball.draw()
        #     for point in self.indexes:
        #         x, y = point
        #         pixel = Vector(x=x, y=y)
        #         distance = ball.pos.dist(pixel)
        #         # print(distance)
