from Graphics.Graphics import Graphics, RED, GREEN, BLUE, WHITE, BLACK
from matrix import matrix_width, matrix_height, matrix_size


class Test(object):
    def __init__(self):
        self.surf = Graphics(matrix_width, matrix_height)
        self.color = GREEN
        self.surf.fill(self.color)
    def generate(self):
        return self.surf.getSurface()