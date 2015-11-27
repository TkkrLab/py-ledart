from Tools.Graphics import Graphics, BLACK
from matrix import matrix_height, matrix_width


class Capture(Graphics):
    def __init__(self):
        Graphics.__init__(self, matrix_height, matrix_width)
        self.fill(BLACK)

    def generate(self):
        pass
