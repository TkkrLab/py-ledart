from Graphics.Graphics import Graphics, BLACK
from matrix import matrix_width, matrix_height
from NumberSegmentBitMap import numbers
import time


class SegmentDisplay(object):
    def __init__(self, graphics, color=(0, 0, 0xff)):
        self.graphics = graphics
        self.letter_width = 4
        self.letter_height = 7

    def drawnumber(self, x_off, y_off, value, offset=0):
        value %= 10
        for x, row in enumerate(numbers[value]):
            for y, pixel in enumerate(row):
                color = (0 * pixel, 0 * pixel, 0xff * pixel)
                new_x, new_y = 6 - x, y + (self.letter_width * offset)
                self.graphics.drawPixel(new_x + x_off, new_y + y_off, color)

    def drawnumbers(self, x, y, value, digits):
        for i in range(digits - 1, -1, -1):
            self.drawnumber(x, y, value, i)
            value /= 10


class SegmentClock(object):
    def __init__(self):
        self.graphics = Graphics(matrix_width, matrix_height)
        self.segmentdisp = SegmentDisplay(self.graphics)

    def generate(self):
        self.graphics.fill(BLACK)
        hour = time.localtime().tm_hour
        minutes = time.localtime().tm_min
        self.segmentdisp.drawnumbers(1, 0, hour, 2)
        self.segmentdisp.drawnumbers(1, matrix_height / 2 + 1, minutes, 2)
        return self.graphics.getSurface()


class SegmentClocked(object):
    def __init__(self):
        self.graphics = Graphics(matrix_width, matrix_height)
        self.segmentdisp = SegmentDisplay(self.graphics)
        self.previous = 1

    def generate(self):
        self.graphics.fill(BLACK)
        current = time.time()
        self.segmentdisp.drawnumbers(0, 0, int(1. / (current - self.previous)), 4)
        self.previous = time.time()
        return self.graphics.getSurface()
