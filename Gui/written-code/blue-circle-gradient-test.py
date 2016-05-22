from matrix import *
from Tools.Graphics import Graphics
from Tools.Graphics import BLUE
from Tools.Graphics import WHITE
from Tools.Graphics import BLACK

class testCircle(Graphics):
    def __init__(self):
        Graphics.__init__(self, matrix_width, matrix_height)
    def generate(self):
        Graphics.fill(self, BLACK)
        Graphics.draw_circle(self, matrix_width/2, matrix_height/2, matrix_width/4-1, BLUE)
        for i in range(0, matrix_height/2):
            Graphics.draw_circle(self, matrix_width/2, matrix_height/2, i, (0, 0, 0xff - (0xff / (matrix_height / 2) * i)))
            