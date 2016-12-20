from Ledart.ArgumentParser import get_args
from Ledart import Graphics, BLUE, BLACK
from Ledart import xfrange

import fractions
import random
from math import sin, cos, radians, pi

class SpiroGraph(Graphics):
    def __init__(self, **kwargs):
        Graphics.__init__(self, **kwargs)

        self.res = kwargs.get('res', 0.001)
        self.scale = kwargs.get('scale', 0.7)

        self.xp = kwargs.get('xp', random.randint(1, self.width))
        self.yp = kwargs.get('yp', random.randint(1, self.height))

        self.R = kwargs.get('R', random.randint(1, self.width))
        self.r = kwargs.get('r', random.randint(1, self.width))
        self.d = kwargs.get('d', random.randint(1, self.width))

        self.mode = kwargs.get('mode', 0)

        self.nice_ones = [(66, 15, 58),
                          (95, 10, 92),
                          (17, 118, 115),
                          (126, 27, 74),
                          (84, 66, 19),
                          (36, 21, 19),
                          (81, 6, 8),
                          (111, 18, 33),
                          (126, 40, 38),
                          (60, 17, 92),
                          (102, 6, 35),
                          (104, 60, 109),
                          (65, 25, 41),
                          (54, 16, 42),
                          (28, 44, 76),
                          (98, 2, 117),
                          (63, 119, 126),
                          (63, 90, 44)
                          ]

        args = get_args()
        if args.debug:
            print("[%s] R: %d, r: %d, d:%d \n" % (__file__, self.R, self.r, self.d))

        gcdval = fractions.gcd(self.r, self.R)
        self.turns = self.r // gcdval

        self.prev_pos = None
        self.draw_spiro()

    def draw_spiro(self):
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

    def generate(self):
        pass