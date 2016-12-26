from Ledart import Graphics, BLACK, GREEN
from Ledart import translate
from Ledart import Vector

import noise
import random
import colorsys

class PerlinTest(Graphics):
    def __init__(self, **kwargs):
        Graphics.__init__(self, **kwargs)
        self.t = 0
        self.y_offset = random.randint(0, self.height)

    def generate(self):
        # self.fill(BLACK)
        x = noise.pnoise1(self.t) + 1
        y = noise.pnoise1(self.t + self.y_offset) + 1
        x = translate(x, 0, 2., 10, self.width - 10)
        y = translate(y, 0, 2., 10, self.height - 10)
        # self.draw_circle(x, y, 10, GREEN)
        color = [int(0xff * c) for c in colorsys.hsv_to_rgb(self.t, 1, 1)]
        self.draw_pixel(x, y, color)
        self.t += 0.001
