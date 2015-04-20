from Tools import Graphics
from matrix import matrix_height, matrix_width


class Capture(object):
    def __init__(self):
        self.graphics = Graphics(matrix_height, matrix_width)

    def generate(self):
        pass
