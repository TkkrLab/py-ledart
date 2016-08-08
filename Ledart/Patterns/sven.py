"""
made by: sven
Displays: random leds at random positions.
"""

from Ledart.matrix import matrix_width, matrix_height
from Ledart.Tools.Graphics import Graphics, BLACK, rand_color
import random


class Sven(Graphics):
    def __init__(self):
        Graphics.__init__(self, width=matrix_width, height=matrix_height)
        self.color = rand_color()

    def generate(self):
        self.fill(BLACK)
        b = 0
        i = 0
        while(i <= 10):
            color2 = rand_color()
            a = random.randint(0, matrix_width)
            b = random.randint(0, matrix_height)
            self.draw_pixel(a, b, color2)
            i = i + 1
        b = b + 1
