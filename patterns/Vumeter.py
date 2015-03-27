from matrix import matrix_width, matrix_height
from Graphics.Graphics import Graphics, BLUE, BLACK
from Controllers.Controllers import AudioController, translate


class VUmeterThree(object):
    def __init__(self):
        pass

    def generate(self):
        pass


class VUmetertwo(object):
    def __init__(self):
        self.graphics = Graphics(matrix_width, matrix_height)
        self.controller = AudioController(channel=1, rate=256000, period=64)
        self.color = BLUE
        self.inputlength = matrix_height
        self.inputs = []
        self.offset = 13
        self.max = 1500
        self.lim = self.max
        self.rate = 2

    def getaverageof(self, number):
        averages = []
        for i in range(0, number):
            data = self.controller.getinput()
            while(data is None):
                data = self.controller.getinput()
            averages.append(data)
        sums = 0
        for num in averages:
            sums += num
        return int(sums / len(averages))

    def getinputs(self):
        self.inputs = []
        sums = 0
        for input in range(0, self.inputlength):
            data = self.getaverageof(3)
            self.inputs.append(data)
            sums += data
        return sums / len(self.inputs)

    def generate(self):
        average = self.getinputs()
        self.graphics.fill(BLACK)
        for i, line in enumerate(self.inputs):
            if line > self.max:
                self.max = line
            else:
                if self.max <= self.lim:
                    self.max = self.lim
                else:
                    self.max -= int((self.max - self.lim) / self.rate)
            length = int(translate(average, 0, self.max, 0, matrix_height))
            data = int(translate(line, 0, self.max, 0, length))
            if data > 0xff:
                self.data = 0xff
            if data > self.max:
                self.max = data
            print(data)
            self.graphics.drawLine(0, i, data - self.offset, i, self.color)
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
