"""
made by: sven
Displays: random leds at random positions.
"""
from matrix import matrix_width, matrix_height
from Graphics import Graphics, GREEN, randColor
import random


class sven(object):
    def __init__(self):
        self.graphics = Graphics(matrix_width, matrix_height)
        self.color = randColor()

    def generate(self):
        self.graphics.fill(GREEN)
        #self.graphics.drawLine(matrix_width-x,matrix_height-y,x,y, self.color)
        b = 0
        i = 0
        while(i <= 10):
            color2 = randColor()
            a = random.randint(0, matrix_width)
            b = random.randint(0, matrix_height)
            self.graphics.drawPixel(a, b, color2)
            i = i + 1
        b = b + 1
        return self.graphics.getSurface()