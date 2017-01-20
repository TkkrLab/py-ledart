from Ledart.ArgumentParser import get_args
from Ledart import Graphics, BLUE, BLACK
from Ledart import xfrange
from Ledart import Timer

import fractions
import random
import colorsys
from math import sin, cos, radians, pi

class SpiroGraph(Graphics):
    def __init__(self, **kwargs):
        Graphics.__init__(self, **kwargs)

        self.res = kwargs.get('res', 0.001)
        self.scale = kwargs.get('scale', 0.7)

        self.new_params(**kwargs)

        self.mode = kwargs.get('mode', 0)
        self.timer = Timer(3.0)

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

    def new_params(self, **kwargs):
        self.xp = kwargs.get('xp', random.randint(1, self.width))
        self.yp = kwargs.get('yp', random.randint(1, self.height))

        self.R = kwargs.get('R', random.randint(1, self.width))
        self.r = kwargs.get('r', random.randint(1, self.width))
        self.d = kwargs.get('d', random.randint(1, self.width))

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

    def get_around(self, x, y):
        n = 0
        # for i in range(0, 3):
        #     for j in range(0, 3):
        #         nx = (x + i + self.width) % self.width
        #         ny = (y + i + self.height) % self.height
        #     if self[(x, y)] != BLACK:
        #         n += 1
        if self[(x, y)] != BLACK:
            n += 1
        if self[(x - 1, y)] != BLACK:
            n += 1
        if self[(x + 1, y)] != BLACK:
            n += 1

        if self[(x, y + 1)] != BLACK:
            n += 1
        if self[(x - 1, y + 1)] != BLACK:
            n += 1
        if self[(x + 1, y + 1)] != BLACK:
            n += 1

        if self[(x, y - 1)] != BLACK:
            n += 1
        if self[(x - 1, y - 1)] != BLACK:
            n += 1
        if self[(x + 1, y - 1)] != BLACK:
            n += 1

        return n

    def draw_color_spiro(self):
        self.draw_spiro()
        for x in range(1, self.width - 1):
            for y in range(1, self.height - 1):
                cv = self.get_around(x, y) / 9.
                color = [int(0xff * c) for c in colorsys.hsv_to_rgb(cv, 1, 1)]
                self[(x, y)] = color

    def generate(self):
        if self.mode == 0:
            self.draw_spiro()
        elif self.mode == 1:
            self.new_params()
            if self.timer.valid():
                self.draw_spiro()
        elif self.mode == 2:
            self.new_params()
            if self.timer.valid():
                self.draw_color_spiro()
