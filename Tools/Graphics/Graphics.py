import random


def randColor():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)


class Graphics(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.size = self.width * self.height
        self.widthRange = range(0, self.width)
        self.heightRange = range(0, self.height)
        self.surface = self.generatesurface()

    def generatesurface(self):
        surface = []
        templist = []
        for y in self.heightRange:
            for x in self.widthRange:
                templist.append(())
            surface.append(templist)
            templist = []
        return surface

    def toMatrix(self, l, n):
        return [l[i:i + n] for i in range(0, len(l), n)]

    def writePixel(self, x, y, color):
        x, y = int(x), int(y)
        if x >= self.width or y >= self.height:
            return 0
        elif x < 0 or y < 0:
            return 0
        else:
            self.surface[y][x] = color

    def readPixel(self, x, y):
        x, y = int(x), int(y)
        if x >= self.width or y >= self.height:
            return BLACK
        elif x < 0 or y < 0:
            return BLACK
        else:
            return self.surface[y][x]

    def calcIndex(self, x, y):
        x, y = int(x), int(y)
        return ((y * self.width) + x)

    def fill(self, color):
        for x in range(0, self.width):
            for y in range(0, self.height):
                self.drawPixel(x, y, color)

    def getSurfaceSize(self):
        return self.size

    def getSurfaceWidth(self):
        return self.width

    def getSurfaceHeight(self):
        return self.height

    def getSurface(self, dimension=1):
        if dimension == 1:
            surface = []
            for row in self.surface:
                surface += row
        else:
            surface = self.surface
        return surface

    def setSurface(self, surface, dimension=1):
        if dimension == 1:
            surface = self.toMatrix(surface, 2)
        self.surface = surface

    def drawPixel(self, x, y, color):
        self.writePixel(x, y, color)

# wiki http://www.roguebasin.com/index.php?title=Bresenham%27s_Line_Algorithm
    def drawLine(self, x1, y1, x2, y2, color):
        x1, y1 = int(x1), int(y1)
        x2, y2 = int(x2), int(y2)
        issteep = abs(y2 - y1) > abs(x2 - x1)
        if issteep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
        rev = False
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
            rev = True
        deltax = x2 - x1
        deltay = abs(y2 - y1)
        error = int(deltax / 2)
        y = y1
        ystep = None
        if y1 < y2:
            ystep = 1
        else:
            ystep = -1
        for x in range(x1, x2 + 1):
            if issteep:
                self.writePixel(y, x, color)
            else:
                self.writePixel(x, y, color)
            error -= deltay
            if error < 0:
                y += ystep
                error += deltax
        if rev:
            self.surface.reverse()

    def drawRect(self, x, y, width, height, color):
        x, y = int(x), int(y)
        width, height = int(width), int(height)
        # because cordinate system starts at 0
        width, height = width - 1, height - 1
        self.drawLine(x, y, x + width, y, color)
        self.drawLine(x, y + height, x + width, y + height, color)
        self.drawLine(x, y, x, y + height, color)
        self.drawLine(x + width, y, x + width, y + height, color)

    def drawCircle(self, x0, y0, radius, color):
        x0, y0 = int(x0), int(y0)
        radius = int(radius)
        # brensenham circle
        error = 1 - radius
        errory = 1
        errorx = -2 * radius
        x = radius
        y = 0
        self.writePixel(x0, y0 + radius, color)
        self.writePixel(x0, y0 - radius, color)
        self.writePixel(x0 + radius, y0, color)
        self.writePixel(x0 - radius, y0, color)
        while(y < x):
            if(error > 0):
                x -= 1
                errorx += 2
                error += errorx
            y += 1
            errory += 2
            error += errory
            self.writePixel(x0 + x, y0 + y, color)
            self.writePixel(x0 - x, y0 + y, color)
            self.writePixel(x0 + x, y0 - y, color)
            self.writePixel(x0 - x, y0 - y, color)
            self.writePixel(x0 + y, y0 + x, color)
            self.writePixel(x0 - y, y0 + x, color)
            self.writePixel(x0 + y, y0 - x, color)
            self.writePixel(x0 - y, y0 - x, color)
            self.writePixel(x0 - y, y0 + x, color)
            self.writePixel(x0 + y, y0 - x, color)
            self.writePixel(x0 - y, y0 - x, color)
