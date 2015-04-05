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
        return self.graphics.getSurface()