from Ledart import Graphics, BLACK, BLUE, RED, WHITE
from Ledart import translate
from colorsys import hsv_to_rgb
import operator
import random
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
        return self.__div__(self.magnitude())

    def limit(self, lim):
        pass

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
        return self.mag()

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


class Ball(object):
    def __init__(self, g=None, x=0, y=0, size=1):
        self.accel = Vector(x=0, y=0)
        self.speed = Vector(x=0, y=0)
        self.pos = Vector(x=x, y=y)
        self.size = size
        self.g = g
        self.mass = self.size
        self.max_speed = 0

    def update(self):
        self.speed += self.accel
        self.pos += self.speed
        self.accel *= 0

        self.handle_collision()

    def handle_collision(self):
        if (self.pos.x - self.size < 0 or
            self.pos.x > self.g.width - self.size):
            # self.pos.x -= self.speed.x
            self.pos -= self.speed
            self.speed.x *= -1
        if (self.pos.y - self.size < 0 or 
            self.pos.y > self.g.height - self.size):
            # self.pos.y -= self.speed.y
            self.pos -= self.speed
            self.speed.y *= -1

    def draw(self):
        self.g.draw_circle(self.pos.x, self.pos.y, self.size, BLUE)


class MetaBalls(Graphics):
    def __init__(self, **kwargs):
        Graphics.__init__(self, **kwargs)
        return
        self.balls = []
        for i in range(10):
            size = random.randint(4, 10)
            x = random.randint(size, self.width - size)
            y = random.randint(size, self.height - size)
            ball = Ball(g=self, x=x, y=y, size=size)
            # ball.speed += random.randint(20, 80) / 100.
            self.balls.append(ball)
        self.max = 0
 
    def generate(self):
        return
        self.fill(BLACK)

        for point in self.indexes:
            x, y = point
            sumc = 0
            
            for ball in self.balls:
                distance = (ball.pos.dist(Vector(x=x, y=y)) + 1)
                sumc += ball.size / distance

            color = min(sumc * 80, 0xff) / 0xff
            self[point] = [int(c * 0xff) for c in hsv_to_rgb(color, 1, 1)]

        for ball in self.balls:
            ball.update()
            ball.draw()
            for otherball in self.balls:
                if ball != otherball:
                    force = ball.pos - otherball.pos
                    dist = max(force.mag, ball.size)
                    force = force.normalize()
                    G = 0.01
                    strength = (G * ball.mass * otherball.mass) / (dist ** 2)
                    force *= strength
                    ball.accel -= force
            # print(ball.speed)
