from matrix import matrix_width, matrix_height
from Graphics.Graphics import Graphics, BLUE, BLACK
from Controllers.Controllers import AudioController, translate

class VUmeterone(object):
    def __init__(self):
        self.graphics = Graphics(matrix_width, matrix_height)
        self.controller = AudioController(channel=1, rate=8000, period=128)
        self.average = []
        self.averaged = 1
        self.averagelength = 10

    def generate(self):
        data = getaverageof(10, self.controller)
        if data:
            data = int(translate(data, 0, 700, 0, 8))
            self.graphics.fill(BLACK)
            self.graphics.drawLine(0, 0, data - 10, 0, BLUE)
        return self.graphics.getSurface()