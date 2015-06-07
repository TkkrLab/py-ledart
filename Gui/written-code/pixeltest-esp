from Tools.Graphics import Graphics, WHITE
from matrix import matrix_width, matrix_height
import random

class TestPat(object):
    def __init__(self):
        self.graphics = Graphics(matrix_width, matrix_height)
        self.graphics.fill((0, 0, 0))
    def generate(self):
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.graphics.drawLine(0, 0, matrix_width-1, matrix_height-1, color)
        return self.graphics.getSurface()