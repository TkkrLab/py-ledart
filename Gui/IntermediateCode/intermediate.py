from Graphics.Graphics import Graphics, BLACK, WHITE, GREEN, BLUE, RED
from matrix import *
from Timing import *

numbers = [
           [[0, 1, 1, 0],
            [1, 0, 0, 1],
            [1, 0, 0, 1],
            [0, 0, 0, 0],
            [1, 0, 0, 1],
            [1, 0, 0, 1],
            [0, 1, 1, 0]],

           [[0, 0, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 0, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 0, 1],
            [0, 0, 0, 0]],

           [[0, 1, 1, 0],
            [0, 0, 0, 1],
            [0, 0, 0, 1],
            [0, 1, 1, 0],
            [1, 0, 0, 0],
            [1, 0, 0, 0],
            [0, 1, 1, 0]],

           [[0, 1, 1, 0],
            [0, 0, 0, 1],
            [0, 0, 0, 1],
            [0, 1, 1, 0],
            [0, 0, 0, 1],
            [0, 0, 0, 1],
            [0, 1, 1, 0]],

           [[0, 0, 0, 0],
            [1, 0, 0, 1],
            [1, 0, 0, 1],
            [0, 1, 1, 0],
            [0, 0, 0, 1],
            [0, 0, 0, 1],
            [0, 0, 0, 0]],

           [[0, 1, 1, 0],
            [1, 0, 0, 0],
            [1, 0, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 0, 1],
            [0, 0, 0, 1],
            [0, 1, 1, 0]],

           [[0, 1, 1, 0],
            [1, 0, 0, 0],
            [1, 0, 0, 0],
            [0, 1, 1, 0],
            [1, 0, 0, 1],
            [1, 0, 0, 1],
            [0, 1, 1, 0]],

           [[0, 1, 1, 0],
            [0, 0, 0, 1],
            [0, 0, 0, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 0, 1],
            [0, 0, 0, 0]],

           [[0, 1, 1, 0],
            [1, 0, 0, 1],
            [1, 0, 0, 1],
            [0, 1, 1, 0],
            [1, 0, 0, 1],
            [1, 0, 0, 1],
            [0, 1, 1, 0]],

           [[0, 1, 1, 0],
            [1, 0, 0, 1],
            [1, 0, 0, 1],
            [0, 1, 1, 0],
            [0, 0, 0, 1],
            [0, 0, 0, 1],
            [0, 1, 1, 0]],
          ]

class Pattern(object):
    def __init__(self):
        self.graphics = Graphics(matrix_width, matrix_height)
        self.letter_width = 4
        self.letter_height = 7
        self.timer = Timer(1/2.)
        self.number = 0
    def generate(self):
        self.graphics.fill(BLACK)
        if self.timer.valid():
            self.number += 1
            if self.number > 9:
                self.number = 0
        for x, row in enumerate(numbers[self.number]):
            for y, pixel in enumerate(row):
                color = (0, 0, 0xff*pixel)
                self.graphics.drawPixel(6-x, y, color)
        return self.graphics.getSurface()