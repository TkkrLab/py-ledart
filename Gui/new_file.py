from Graphics.Graphics import Graphics, BLACK, WHITE, RED, GREEN, BLUE
from matrix import matrix_width, matrix_height
from NumberSegmentBitMap import numbers
import time

colors1 = [WHITE, GREEN]
colors2 = [RED, BLUE]

class SegmentDisplay(object):
    def __init__(self, graphics):
        self.graphics = graphics
        self.letter_width = 4
        self.letter_height = 7

    def drawnumber(self, x_off, y_off, value, color, offset=0):
        value %= 10
        for x, row in enumerate(numbers[value]):
            for y, pixel in enumerate(row):
                r, g, b = color
                new_color = (r * pixel, g * pixel, b * pixel)
                new_x, new_y = 6 - x, y + (self.letter_width * offset)
                self.graphics.drawPixel(new_x + x_off, new_y + y_off, new_color)

    def drawnumbers(self, x, y, value, colors, digits):
        for i in range(digits - 1, -1, -1):
            self.drawnumber(x, y, value, colors[i], i)
            value /= 10


class SegmentClock(object):
    def __init__(self):
        self.graphics = Graphics(matrix_width, matrix_height)
        self.segmentdisp = SegmentDisplay(self.graphics)

    def generate(self):
        self.graphics.fill(BLACK)
        hour = time.localtime().tm_hour
        minutes = time.localtime().tm_min
        self.segmentdisp.drawnumbers(1, 0, hour, colors1, 2)
        self.segmentdisp.drawnumbers(1, matrix_height / 2 + 1, minutes, colors2, 2)
        return self.graphics.getSurface()
