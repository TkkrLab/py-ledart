"""
made by: sven
Displays: random leds at random positions.
"""

from matrix import matrix_width, matrix_height
from Tools.Graphics import Graphics, BLACK, rand_color
import random


class Sven(object):
    def __init__(self):
        self.graphics = Graphics(matrix_width, matrix_height)
        self.color = rand_color()

    def generate(self):
        self.graphics.fill(BLACK)
        b = 0
        i = 0
        while(i <= 10):
            color2 = rand_color()
            a = random.randint(0, matrix_width)
            b = random.randint(0, matrix_height)
            self.graphics.drawPixel(a, b, color2)
            i = i + 1
        b = b + 1
