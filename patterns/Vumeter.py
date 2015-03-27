from matrix import matrix_width, matrix_height, matrix_size
from Graphics.Graphics import Graphics, BLUE
from Controllers.Controllers import AudioController


class VUmeterone(object):
    def __init__(self):
        self.graphics = Graphics(matrix_width, matrix_height)

    def generate(self):
        self.graphics.fill(BLUE)
        return self.graphics.getSurface()
