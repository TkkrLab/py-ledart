from Graphics.Graphics import Graphics, GREEN
from matrix import matrix_width, matrix_height
import random

class Test(object):
    def __init__(self):
        self.graphics = Graphics(matrix_width, matrix_height)
        self.color = GREEN
    def generate(self):
        self.graphics.fill(self.color)
        x, y = random.randint(0, matrix_width-1), random.randint(0, matrix_height-1)
        random_c = random.randint(0, 0xff)
        self.graphics.drawPixel(x, y, (random_c, random_c, random_c))
        return self.graphics.getSurface()