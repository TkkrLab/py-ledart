from itertools import cycle


class PaletGenerate(object):
    def __init__(self):
        self.cvalue = 0
        self.cpledselect = 2
        self.cledselect = 0
        self.colors = [0, 0, 0]
        self.colors[self.cpledselect] = 0xff
        self.colors[self.cledselect] = 0
        self.rainbow = self.generateRainbow()
        self.pool = cycle(self.rainbow)

    def colorFade(self):
        self.cvalue += 1
        if self.cvalue > 255:
            self.cledselect += 1
            self.cvalue = 1
            if self.cledselect == 3:
                self.cledselect = 0
                self.cpledselect = 2
            else:
                self.cpledselect = self.cledselect - 1
        self.colors[self.cpledselect] = 255 - self.cvalue
        self.colors[self.cledselect] = self.cvalue
        return list(self.colors)

    def rainbowRange(self):
        return next(self.pool)

    def generateRainbow(self):
        rainbow = []
        for i in range(0, 0xff * 3, 1):
            rainbow.append(self.colorFade())
        return rainbow
