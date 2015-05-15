from Tools.Graphics import Graphics, WHITE, BLACK
from matrix import matrix_width, matrix_height
import random

class TestPattern(object):
    def __init__(self):
        self.graphics = Graphics(matrix_width, matrix_height)
    
    def generate(self):
        self.graphics.fill(WHITE)
        return self.graphics.getSurface()
    