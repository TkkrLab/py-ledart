from matrix import matrix_width, matrix_height
from Graphics.Graphics import Graphics, BLUE, BLACK
from Controllers.Controllers import AudioController, translate


class VUmetertwo(object):
    def __init__(self):
        self.graphics = Graphics(matrix_width, matrix_height)
        self.controller = AudioController(channel=1, rate=32000, period=64)
        self.inputlength = matrix_height
        self.inputs = []
        self.offset = 100
        self.max = 1500
        self.lim = 1100
        self.rate = 500

    def getinputs(self):
        self.inputs = []
        for input in range(0, self.inputlength):
            data = self.controller.getinput()
            while(data is None):
                data = self.controller.getinput()
            self.inputs.append(data)

    def generate(self):
        self.getinputs()
        self.graphics.fill(BLACK)
        for i, line in enumerate(self.inputs):
            if line > self.max:
                self.max = line
            else:
                if self.max <= self.lim:
                    self.max = self.lim
                else:
                    self.max -= int((self.max - self.lim) / self.rate)
            data = int(translate(line, 0, self.max, 0, matrix_height))
            if data > 0xff:
                self.data = 0xff - 1
            if data == 0:
                data = 1
            r = g = b = data + self.offset
            color = (r, g, b)
            self.graphics.drawLine(0, i, data - 4, i, color)
        return self.graphics.getSurface()


class VUmeterone(object):
    def __init__(self):
        self.graphics = Graphics(matrix_width, matrix_height)
        self.controller = AudioController(channel=1, rate=8000, period=90)
        self.average = []
        self.averaged = 1
        self.averagelength = 10

    def generate(self):
        data = self.controller.getinput()
        if data:
            data = int(translate(data, 0, 500, 0, 10))
            self.graphics.fill(BLACK)
            self.graphics.drawLine(0, 0, data - 5, 0, BLUE)
        return self.graphics.getSurface()
