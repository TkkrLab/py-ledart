from Ledart import Graphics, BLACK, GREEN
from Ledart import translate
from Ledart import Vector

import noise
import random

class PerlinTest(Graphics):
    def __init__(self, **kwargs):
        Graphics.__init__(self, **kwargs)
        self.t = 0

    def generate(self):
        self.fill(BLACK)
        x = noise.pnoise1(self.t)
        x = translate(x, 0, 1., 10, self.width - 10)
        self.draw_circle(x, self.height / 2, 10, GREEN)
        self.t += 0.01
