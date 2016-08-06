class Pixel(object):
    def __init__(self, pos, size, color):
        self.color = color
        self.size = size
        self.pos = pos

    def setColor(self, color):
        self.color = color

    def getColor(self):
        return self.color

    def setPos(self, pos):
        self.pos = pos

    def setSize(self, size):
        self.size = size

    def getRect(self):
        x, y = self.pos
        return (x, y, self.size, self.size)
