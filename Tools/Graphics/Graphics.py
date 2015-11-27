import random
from Surface import Surface


def rand_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)


def to_matrix(l, n):
    return [l[i:i + n] for i in range(0, len(l), n)]


class Graphics(Surface):
    def __init__(self, width, height):
        Surface.__init__(self, width=width, height=height)

    def fill(self, color):
        self.surface = self.gen_surface(default=color)

    def read_pixel(self, x, y):
        return self.surface[(x, y)]

    def draw_pixel(self, x, y, color):
        self.surface[(x, y)] = color

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
        for x in range(x1, x2 + 1):
            if issteep:
                self.draw_pixel(y, x, color)
            else:
                self.draw_pixel(x, y, color)
            error -= deltay
            if error < 0:
                y += ystep
                error += deltax

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
        radius = int(radius)
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
