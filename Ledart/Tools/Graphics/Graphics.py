import random
from Surface import Surface


def rand_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return [r, g, b]


class Graphics(Surface):
    def __init__(self, **kwargs):
        Surface.__init__(self, **kwargs)

    def fill(self, color):
        if not isinstance(color, list):
            raise ValueError
        for i in xrange(0, self.get_size()):
            if self.surface[i] != color:
                self.surface[i] = color


    def read_pixel(self, x, y):
        if x < 0 or x >= self.get_width():
            raise IndexError
        if y < 0 or y >= self.get_height():
            raise IndexError
        return self[(x, y)]

    def draw_pixel(self, x, y, color):
        if x < 0 or x >= self.get_width():
            return
        if y < 0 or y >= self.get_height():
            return
        if self[(int(x), int(y))] != color:
            self[(int(x), int(y))] = list(color)

    def convert(self):
        pass

    def blit(self, source_image, dest_rect):
        pass

# wiki http://www.roguebasin.com/index.php?title=Bresenham%27s_Line_Algorithm
    def draw_line(self, x1, y1, x2, y2, color):
        x1, y1 = int(x1), int(y1)
        x2, y2 = int(x2), int(y2)
        issteep = abs(y2 - y1) > abs(x2 - x1)
        if issteep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2

        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        deltax = x2 - x1
        deltay = abs(y2 - y1)
        error = int(deltax / 2)
        y = y1
        ystep = None
        if y1 < y2:
            ystep = 1
        else:
            ystep = -1
        try:
            for x in xrange(x1, x2 + 1):
                if issteep:
                    self.draw_pixel(y, x, color)
                else:
                    self.draw_pixel(x, y, color)
                error -= deltay
                if error < 0:
                    y += ystep
                    error += deltax
        except Exception as e:
            print("x1: %d x2: %d" % (x1 , x2))
            raise e

    def draw_rect(self, x, y, width, height, color):
        x, y = int(x), int(y)
        width, height = int(width), int(height)
        # because cordinate system starts at 0
        width, height = width - 1, height - 1
        self.draw_line(x, y, x + width, y, color)
        self.draw_line(x, y + height, x + width, y + height, color)
        self.draw_line(x, y, x, y + height, color)
        self.draw_line(x + width, y, x + width, y + height, color)

    def draw_circle(self, x0, y0, radius, color):
        x0, y0 = int(x0), int(y0)
        radius = int(radius-1)
        # brensenham circle
        error = 1 - radius
        errory = 1
        errorx = -2 * radius
        x = radius
        y = 0
        self.draw_pixel(x0, y0 + radius, color)
        self.draw_pixel(x0, y0 - radius, color)
        self.draw_pixel(x0 + radius, y0, color)
        self.draw_pixel(x0 - radius, y0, color)
        while(y < x):
            if(error > 0):
                x -= 1
                errorx += 2
                error += errorx
            y += 1
            errory += 2
            error += errory
            self.draw_pixel(x0 + x, y0 + y, color)
            self.draw_pixel(x0 - x, y0 + y, color)
            self.draw_pixel(x0 + x, y0 - y, color)
            self.draw_pixel(x0 - x, y0 - y, color)
            self.draw_pixel(x0 + y, y0 + x, color)
            self.draw_pixel(x0 - y, y0 + x, color)
            self.draw_pixel(x0 + y, y0 - x, color)
            self.draw_pixel(x0 - y, y0 - x, color)
            self.draw_pixel(x0 - y, y0 + x, color)
            self.draw_pixel(x0 + y, y0 - x, color)
            self.draw_pixel(x0 - y, y0 - x, color)
