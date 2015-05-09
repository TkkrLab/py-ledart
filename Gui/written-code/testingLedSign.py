from Tools.Graphics import Graphics, WHITE, BLACK
from matrix import matrix_width, matrix_height

class TestPattern(object):
    def __init__(self):
        self.graphics = Graphics(matrix_width, matrix_height)
    
    def generate(self):
        self.graphics.fill(BLACK)
        self.graphics.drawLine(0, matrix_height-1, matrix_width, matrix_height-1, WHITE)
        return self.graphics.getSurface()
    