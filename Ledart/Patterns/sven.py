"""
made by: sven
Displays: random leds at random positions.
"""

from Ledart.stripinfo import strip_width, strip_height
from Ledart.Tools.Graphics import Graphics, BLACK, rand_color
import random


class Sven(Graphics):
    def __init__(self):
        Graphics.__init__(self, width=strip_width, height=strip_height)
        self.color = rand_color()

    def generate(self):
        self.fill(BLACK)
        b = 0
        i = 0
        while(i <= 10):
            color2 = rand_color()
            a = random.randint(0, strip_width)
            b = random.randint(0, strip_height)
            self.draw_pixel(a, b, color2)
            i = i + 1
        b = b + 1
