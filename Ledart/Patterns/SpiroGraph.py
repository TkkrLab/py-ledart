from Ledart import Graphics, BLUE, BLACK
from Ledart import xfrange

import fractions
import random
from math import sin, cos, radians, pi

class SpiroGraph(Graphics):
    def __init__(self, **kwargs):
        Graphics.__init__(self, **kwargs)

        self.res = 0.01
        self.scale = 0.7

        self.xp = random.randint(1, self.width)
        self.yp = random.randint(1, self.height)

        self.R = random.randint(1, self.width)
        self.r = random.randint(1, self.width)
        self.d = random.randint(1, self.width)

        gcdval = fractions.gcd(self.r, self.R)
        self.turns = self.r // gcdval

        self.prev_pos = None

    def generate(self):
        self.fill(BLACK)

        for i in xfrange(0, (2 * pi) * self.turns + 1, self.res):
            a = (self.R - self.r)
            x = (a * cos(i) + self.d * cos(i * a / self.r))
            y = (a * sin(i) - self.d * sin(i * a / self.r))

            if self.prev_pos:
                x2, y2 = self.prev_pos
                self.draw_line((x * self.scale) + self.xp, (y * self.scale) + self.yp,
                               (x2 * self.scale) + self.xp, (y2 * self.scale) + self.yp,
                               BLUE)
            self.prev_pos = x, y

