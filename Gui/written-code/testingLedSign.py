from Tools.Graphics import Graphics
from matrix import matrix_width, matrix_height

class TestPattern(object):
    def __init__(self):
        self.graphics = Graphics(matrix_width, matrix_height)
    
    def generate(self):
        self.graphics.fill((255, 255, 255));
        for i in range(0, 80):
            self.graphics.drawPixel(i, 2, (i, i, i))
        return self.graphics.getSurface()