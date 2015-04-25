from Tools.Graphics import Graphics, GREEN, BLACK
from matrix import matrix_width, matrix_height
from Controllers.Controllers import translate
from Tools.Timing import Timer
import math

select = 'Test'

class Test(object):
    def __init__(self):
        self.graphics = Graphics(matrix_width, matrix_height)
        self.x = 0
        self.y = 0
        self.color = GREEN
        self.phase = 1
        self.timer = Timer(1/30.)
        self.wave_range = 3
        self.wave_step = 1
        self.amplitude = 4
        self.offset = matrix_width/2-1
        self.freq = 1./matrix_height*8

    def generate(self):
        self.graphics.fill(BLACK)
        if self.timer.valid():
            self.phase+=1
        for i in range(0, self.wave_range, self.wave_step):
            for self.y in range(0, matrix_height-1):
                self.x = math.sin(self.y*self.freq+self.phase)*self.amplitude+self.offset + i
                b = translate(i, 0, matrix_width, 0, 50)
                g = translate(self.y, 0, matrix_height, 0, 80)
                r = translate(self.x, 0, 12, 0, 24)
                self.color = (int(r), int(g), int(b))
                self.graphics.drawPixel(self.x, self.y, self.color)
        return self.graphics.getSurface()
