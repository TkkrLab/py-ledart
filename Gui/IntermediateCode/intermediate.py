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

class SegmentDisplay(object):
    def __init__(self, graphics, color = (0, 0, 0xff), digits=1):
        self.graphics = graphics
        self.value = 0
        self.number = []
        self.pos = (0, 0)

        self.letter_width = 4
        self.letter_height = 7
    def drawnumber(self, x, y, value, offset=0):
        if value > 9:
            return
        for x, row in enumerate(numbers[value]):
            for y, pixel in enumerate(row):
                color = (0*pixel, 0*pixel, 0xff*pixel)
                self.graphics.drawPixel(6-x, y+offset, color)
        
class Pattern(object):
    def __init__(self):
        self.graphics = Graphics(matrix_width, matrix_height)
        self.timer = Timer(1/2.)
        self.number = 0
        self.segmentdisp = SegmentDisplay(self.graphics)
    def generate(self):
        self.graphics.fill(BLACK)
        if self.timer.valid():
            self.number += 1
            if self.number > 9:
                self.number = 0
        self.segmentdisp.drawnumber(0, 0, self.number)
        return self.graphics.getSurface()