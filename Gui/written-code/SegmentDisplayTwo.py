from Graphics.Graphics import Graphics, BLACK
from matrix import matrix_width, matrix_height
from Timing import Timer

numbers = [[[0, 1, 1, 0],
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
            [0, 1, 1, 0]]]


class SegmentDisplay(object):
    def __init__(self, graphics, color=(0, 0, 0xff)):
        self.graphics = graphics
        self.letter_width = 4
        self.letter_height = 7

    def drawnumber(self, x, y, value, offset=0):
        value %= 10
        for x, row in enumerate(numbers[value]):
            for y, pixel in enumerate(row):
                color = (0 * pixel, 0 * pixel, 0xff * pixel)
                new_x, new_y = 6 - x, y + (self.letter_width * offset)
                self.graphics.drawPixel(new_x, new_y, color)

    def drawnumbers(self, x, y, value, digits):
        for i in range(digits - 1, -1, -1):
            self.drawnumber(x, y, value, i)
            value /= 10


class Pattern(object):
    def __init__(self):
        self.graphics = Graphics(matrix_width, matrix_height)
        self.timer = Timer(1 / 2.)
        self.number = 0
        self.segmentdisp = SegmentDisplay(self.graphics)

    def generate(self):
        self.graphics.fill(BLACK)
        if self.timer.valid():
            self.number += 1
        self.segmentdisp.drawnumbers(0, 0, self.number, 4)
        return self.graphics.getSurface()
