from Graphics.Graphics import Graphics, GREEN, BLACK, WHITE
from matrix import matrix_width, matrix_height
import random
import math
import time

class Colors(object):
    def __init__(self):
        pass

class Timer(object):
    import time
    def __init__(self, interval):
        self.previous = 0
        self.current = self.time.time()
        self.interval = interval

    def valid(self):
        self.current = self.time.time()
        if(self.current - self.previous) >= self.interval:
            self.previous = self.current
            return True
        else:
            return False

class Test(object):
    def __init__(self):
        self.graphics = Graphics(matrix_width, matrix_height)
        self.color = GREEN
        self.x = 0
        self.y = 0
        self.x_offset = matrix_width / 2
        self.y_offset = matrix_height / 2
        self.angle = 0
        self.radius = (matrix_width/2)-5
        self.timer = Timer(0.1)
    def generate(self):
        self.graphics.fill(BLACK)
        for i in range(0, 360):
            self.x = math.sin(math.radians(i)) * self.radius + self.x_offset
            self.y = math.cos(math.radians(i)) * self.radius + self.y_offset
            self.graphics.drawPixel(self.x, self.y, self.color)
        #if self.timer.valid():
        #    self.angle += 1
        #    if self.angle > 360:
        #        self.angle = 0
        return self.graphics.getSurface()