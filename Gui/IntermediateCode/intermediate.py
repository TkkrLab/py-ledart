from Graphics.Graphics import Graphics, GREEN, BLACK, WHITE
from matrix import matrix_width, matrix_height
import random

class Colors(object):
    def __init__(self):
        pass

class Test(object):
    def __init__(self):
        self.graphics = Graphics(matrix_width, matrix_height)
        self.color = GREEN
    def generate(self):
        self.graphics.fill(BLACK)
        for i in range(1, matrix_width+1):
            print(0xff/i)
            r = 0xff/i
            g = 0xff/i*3.0
            b = 0xff/i*1.1
            color = (r, g, b)
            self.graphics.drawPixel(i-1, i-1, color)
        return self.graphics.getSurface()