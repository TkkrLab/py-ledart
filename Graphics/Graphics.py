from matrix import matrix_width, matrix_height
import random

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)

COLORS = [RED, GREEN, BLUE, WHITE, BLACK, PURPLE, YELLOW, CYAN]


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
        if x >= self.width or y >= self.height:
            return 0
        elif x < 0 or y < 0:
            return 0
        else:
            self.surface[y][x] = color

    def readPixel(self, x, y):
        if x >= self.width or y >= self.height:
            return BLACK
        elif x < 0 or y < 0:
            return BLACK
        else:
            return self.surface[y][x]

    def calcIndex(self, x, y):
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
        # because cordinate system starts at 0
        width, height = width - 1, height - 1
        self.drawLine(x, y, x + width, y, color)
        self.drawLine(x, y + height, x + width, y + height, color)
        self.drawLine(x, y, x, y + height, color)
        self.drawLine(x + width, y, x + width, y + height, color)

    def drawCircle(self, x0, y0, radius, color):
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


class GraphicsPixelTest(object):
    def __init__(self):
        self.graphics = Graphics(matrix_width, matrix_height)
        self.color = GREEN
        self.pos = (random.randint(1, matrix_width - 1),
                    random.randint(1, matrix_height - 1))
        self.speed = 1
        self.deltax, self.deltay = self.speed, self.speed

    def generate(self):
        self.graphics.fill(BLACK)
        x, y = self.pos
        self.graphics.drawPixel(x, y, self.color)
        if x >= matrix_width - 1 or x <= 0:
            self.deltax *= -1
        if y >= matrix_height - 1 or y <= 0:
            self.deltay *= -1
        self.pos = x + self.deltax, y + self.deltay
        return self.graphics.getSurface()


class GraphicsLineTest(object):
    def __init__(self):
        self.graphics = Graphics(matrix_width, matrix_height)
        self.color = YELLOW
        self.pos = 0, 0

    def generate(self):
        self.graphics.fill(BLACK)
        x, y = self.pos
        self.graphics.drawLine(matrix_width - x, matrix_height - y,
                               x, y, self.color)
        if x >= matrix_height:
            x = 0
            y = 0
        self.pos = x + 1, y
        return self.graphics.getSurface()


class GraphicsRectTest(object):
    def __init__(self):
        self.graphics = Graphics(matrix_width, matrix_height)
        self.color = CYAN
        self.rect_size = matrix_width
        self.pos = 0, 0

    def generate(self):
        # clear the drawing surface
        self.graphics.fill(BLACK)
        # put a rectangle on the surface
        x, y = self.pos
        if x >= matrix_width:
            x = 0
        if y >= matrix_height:
            y = 0
        self.graphics.drawRect(x, y, matrix_width - x,
                               matrix_height - y, self.color)
        self.pos = x + 1, y + 1
        # get te surface drawn
        return self.graphics.getSurface()


class GraphicsCircleTest(object):
    def __init__(self):
        self.graphics = Graphics(matrix_width, matrix_height)
        self.radius = 0
        self.direction = 1
        self.color = RED

    def generate(self):
        # clear the drawing surface
        self.graphics.fill(BLACK)
        # put a circle on our surface
        self.graphics.drawCircle(matrix_width / 2, matrix_height / 2,
                                 self.radius, self.color)

        # circle grows and shrinks based on direction.
        if self.direction:
            self.radius += 1
        else:
            self.radius -= 1

        # if the circle is to big or to small inverse growth direction.
        if self.radius >= (matrix_height / 2) or self.radius <= 0:
            self.direction = not self.direction

        # get the surface drawn
        return self.graphics.getSurface()


class GraphicsDotTest(object):
    def __init__(self):
        self.graphics = Graphics(matrix_width, matrix_height)
        self.color = (123, 111, 222)

    def generate(self):
        self.graphics.fill(BLACK)
        for i in range(0, 5):
            self.graphics.drawPixel(i, i, self.color)
        return self.graphics.getSurface()
