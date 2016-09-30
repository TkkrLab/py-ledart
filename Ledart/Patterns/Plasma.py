from math import sin, cos, sqrt, pi, radians
import time
import random

from Ledart.Tools.Graphics import Graphics, BLACK, BLUE
from Ledart.Tools.Graphics.ConvertColors import HSVtoRGB
from Ledart.Tools.Graphics.RGBColorTools import ColorRGBOps
from Ledart.Tools.Palet import PaletGenerate
from Ledart.Tools.Timing import Timer
from Ledart.Tools.Controllers import translate


class RainbowEffect(Graphics):
    """
        this doesn't work for now. will fix later.
    """
    def __init__(self, **kwargs):
        Graphics.__init__(self, **kwargs)
        speed = kwargs.get('speed', 0.1)
        self.fill(BLACK)
        self.palet = PaletGenerate()
        self.offset = 10
        self.speed = speed

        self.surfaceSize = len(self)
        self.timer = Timer(self.speed)
        self.time = 0
        self.palet = PaletGenerate()
        self.c = self.palet.colorFade()

    def generate(self):
        # effect = []
        # for i in range(0, self.surfaceSize):
        #     effect.append(self.rainbow[i + self.offset])
        # self.offset += self.speed
        # if (self.offset + self.surfaceSize) >= len(self.rainbow):
        #     self.offset = -self.surfaceSize
        # self.setSurface(effect, 1)
        # return self.getSurface()
        pass


class ColorFade(Graphics):
    def __init__(self, **kwargs):
        Graphics.__init__(self, **kwargs)
        speed = kwargs.get('speed', 4)
        self.fill(BLACK)
        self.palet = PaletGenerate()
        self.speed = speed

    def generate(self):
        # cycle a bit faster through the palet if we want.
        for i in range(0, self.speed):
            color = self.palet.colorFade()
        self.fill(color)


class RevolvingCircle(Graphics):
    def __init__(self, **kwargs):
        Graphics.__init__(self, **kwargs)
        self.plasma = Graphics(surface=self)

        self.x_range = xrange(0, self.width, 1)
        self.y_range = xrange(0, self.height, 1)

        self.speed = kwargs.get('speed', 1)
        self.interval = 1000 / self.speed
        self.time = random.randint(0, 100)
        self.previousTick = 0
        self.plasma_width = kwargs.get('plasma_width', 5)

        self.angle = 0

        self.generatePalette()
        self.generatePlasmaSurface()

    def generatePalette(self):
        self.palette = []
        pal = PaletGenerate()
        for x in xrange(0, 0xff * 3, 1):
            color = pal.colorFade()
            r, g, b = color
            colorRGB = (r, g, b)
            self.palette.append(colorRGB)
        # print self.palette[0], self.palette[len(self.palette) - 1]

    def generatePlasmaSurface(self):
        self.angle = int(self.time / self.speed)
        x_offset = (self.width * sin(radians(self.angle)) +
                    self.width * sin(radians(self.angle)))
        y_offset = (self.height * cos(radians(self.angle)) +
                    self.height * cos(radians(self.angle)))
        for y in self.y_range:
            for x in self.x_range:
                c = int((0x7f * sin(sqrt(float((x + x_offset) /
                         self.plasma_width *
                        (x + x_offset) / self.plasma_width +
                        (y + y_offset) / self.plasma_width *
                        (y + y_offset) / self.plasma_width
                        )))))
                color = (abs(c),) * 3
                self.plasma.draw_pixel(x, y, color)

    def process(self):
        millis = round(time.time() * 1000)
        if((millis - self.previousTick) >= self.interval):
            self.previousTick = time.time()
            self.time += 1

    def draw(self):
        paletteShift = self.time / self.speed
        self.generatePlasmaSurface()
        for y in self.y_range:
            for x in self.x_range:
                plasma_color = self.plasma.read_pixel(x, y)
                color_shift = self.palette[paletteShift % len(self.palette)]
                r = (plasma_color[0] + color_shift[0]) % (len(self.palette))
                g = (plasma_color[1] + color_shift[1]) % (len(self.palette))
                b = (plasma_color[2] + color_shift[2]) % (len(self.palette))
                color = (r, g, b,)
                # darken the color to create a better contrast
                color = ColorRGBOps.darken(color, 50)
                self.draw_pixel(x, y, color)

    def generate(self):
        self.fill(BLACK)
        self.process()
        self.draw()


class PlasmaThird(Graphics):
    def __init__(self, **kwargs):
        Graphics.__init__(self, **kwargs)
        self.plasma = Graphics(surface=self)

        self.x_range = xrange(0, self.width, 1)
        self.y_range = xrange(0, self.height, 1)

        speed = kwargs.get('speed', 10)
        self.speed = speed
        self.interval = speed
        self.time = random.randint(0, 100)
        self.previousTick = 0

        self.angle = 0

        self.generatePalette()
        self.generatePlasmaSurface()

    def generatePalette(self):
        self.palette = []
        for x in xrange(0, (2 ** 8), 1):
            r = int(128 + 256 * sin(x) / 20)
            g = int(128 + 256 * sin(r) / 100)
            b = int(128 + 256 * sin(g) / 50)
            colorRGB = (r, g, b)
            self.palette.append(colorRGB)

    def generatePlasmaSurface(self):
        self.angle = self.time
        x_offset = self.width * sin(radians(self.angle)) + self.width
        y_offset = self.height * cos(radians(self.angle)) + self.height
        for y in self.y_range:
            for x in self.x_range:
                c = int(128 + (128 * sin((x + x_offset) / 2.0))
                        + 128 + (128 * sin((y + y_offset) / 2.0))
                        + 128 + (128 * sin(((x + x_offset) + (y + y_offset)) /
                                 2.0))
                        + 128 + (128 * sin(sqrt(float((x + x_offset) *
                                 (x + x_offset) +
                                 (y + y_offset) * (y + y_offset))) / 2.0))
                        ) / 4
                color = (c,) * 3
                self.plasma.draw_pixel(x, y, color)

    def process(self):
        if((time.time() - self.previousTick) >= 1. / self.interval):
            self.previousTick = time.time()
            self.time += 1

    def draw(self):
        paletteShift = self.time
        self.generatePlasmaSurface()
        for y in self.y_range:
            for x in self.x_range:
                plasma_color = self.plasma.read_pixel(x, y)
                color_shift = self.palette[paletteShift % 256]
                r = (plasma_color[0] + color_shift[0]) % 256
                g = (plasma_color[1] + color_shift[1]) % 256
                b = (plasma_color[2] + color_shift[2]) % 256
                color = (r, g, b,)
                # darken the color to create a better contrast
                color = ColorRGBOps.brighten(color, 20)
                self.draw_pixel(x, y, color)

    def generate(self):
        self.fill(BLACK)
        self.process()
        self.draw()


class PlasmaSecond(Graphics):
    def __init__(self, **kwargs):
        Graphics.__init__(self, **kwargs)
        self.plasma = Graphics(surface=self)

        self.x_range = xrange(0, self.width, 1)
        self.y_range = xrange(0, self.height, 1)

        speed = kwargs.get('speed', 1)
        self.speed = speed
        self.interval = 1000 / self.speed
        self.time = random.randint(0, 100)
        self.previousTick = 0

        self.angle = 0

        self.generatePalette()
        self.generatePlasmaSurface()

    def generatePalette(self):
        self.palette = []
        for x in xrange(0, (2 ** 16), 1):
            # int(128.0 +128*sin(pi*x/40.))
            r = 30
            g = int(128.0 + 128 * sin(pi * x / 160.))
            b = int(128.0 + 128 * sin(pi * x / 80.))
            colorRGB = (r, g, b)
            self.palette.append(colorRGB)

    def generatePlasmaSurface(self):
        self.angle = self.time / self.speed
        x_offset = (self.width * sin(radians(self.angle)) +
                    self.width * sin(radians(self.angle)))
        y_offset = (self.height * cos(radians(self.angle)) +
                    self.height * cos(radians(self.angle)))
        for y in self.y_range:
            for x in self.x_range:
                c = int(128 + (128 * sin((x + x_offset) / 2.0))
                        + 128 + (128 * sin((y + y_offset) / 2.0))
                        + (128 + (128 * sin(((x + x_offset) +
                           (y + y_offset)) / 2.0)))
                        + (128 + (128 * sin(sqrt(float((x + x_offset) *
                           (x + x_offset) + (y + y_offset) * (y + y_offset)))
                            / 2.0)))
                        ) / 4
                color = (c,) * 3
                self.plasma.draw_pixel(x, y, color)

    def process(self):
        millis = round(time.time() * 1000)
        if((millis - self.previousTick) >= self.interval):
            self.previousTick = time.time()
            self.time += 1

    def draw(self):
        paletteShift = self.time / self.speed
        self.generatePlasmaSurface()
        for y in self.y_range:
            for x in self.x_range:
                plasma_color = self.plasma.read_pixel(x, y)
                color_shift = self.palette[paletteShift % len(self.palette)]
                r = (plasma_color[0] + color_shift[0]) % 256
                g = (plasma_color[1] + color_shift[1]) % 256
                b = (plasma_color[2] + color_shift[2]) % 256
                color = (r, g, b,)
                # darken the color to create a better contrast
                color = ColorRGBOps.darken(color, 50)
                self.draw_pixel(x, y, color)

    def generate(self):
        self.fill(BLACK)
        self.process()
        self.draw()


class PlasmaFirst(Graphics):
    def __init__(self, **kwargs):
        Graphics.__init__(self, **kwargs)
        self.plasma = Graphics(surface=self)

        self.x_range = xrange(0, self.width, 1)
        self.y_range = xrange(0, self.height, 1)

        speed = kwargs.get('speed', 20)
        self.interval = .1 / speed
        self.time = 0
        self.previousTick = 0

        self.generatePalette()
        self.generatePlasmaSurface()

    def generatePalette(self):
        self.palette = []
        for x in xrange(0, 256, 1):
            colorRGB = HSVtoRGB((x, 255, 255,))
            self.palette.append(colorRGB)

    def generatePlasmaSurface(self):
        for y in self.y_range:
            for x in self.x_range:
                # c = int(abs(256*sin((x+y+self.time)/3.0)))
                c = int(128.0 + (128.0 * sin((x + 6) / 2.4))
                        + 128.0 + (128.0 * cos(y / 3.4))
                        ) / 2
                color = (c,) * 3
                self.plasma.draw_pixel(x, y, color)

    def process(self):
        if((time.time() - self.previousTick) >= self.interval):
            self.previousTick = time.time()
            self.time += 1
        paletteShift = self.time
        for y in self.y_range:
            for x in self.x_range:
                plasma_color = self.plasma.read_pixel(x, y)
                color_shift = self.palette[paletteShift % 256]
                r = (plasma_color[0] + color_shift[0]) % 256
                g = (plasma_color[1] + color_shift[1]) % 256
                b = (plasma_color[2] + color_shift[2]) % 256
                color = (r, g, b,)
                color = ColorRGBOps.darken(color, 50)
                self.draw_pixel(x, y, color)

    def draw(self):
        pass

    def generate(self):
        self.fill(BLACK)
        self.process()
        self.draw()

import colorsys

def generate_color(n=5):
    hsv_tuples = [(x * 0.9 / n, 0.9, 0.9) for x in xrange(n)]
    hex_out = []
    for rgb in hsv_tuples:
        rgb = map(lambda x: int(x*0xff), colorsys.hsv_to_rgb(*rgb))
        hex_out.append(rgb)
    return hex_out

class TestPlasma(Graphics):
    def __init__(self, **kwargs):
        Graphics.__init__(self, **kwargs)
        self.colors = generate_color(self.get_size())
        self.scaler = 10
        self.n = 1
        self.lim = 1e2

    def generate(self):
        for point in self.get_points():
            x, y = point
            nx = int(self.n * sin(radians(x)) / self.scaler)
            ny = int(self.n * cos(radians(y)) / self.scaler)
            np = int((nx * ny) ** 0.5)
            if (np % len(self.colors)) < self.lim:
                np = self.lim
            self[x, y] = self.colors[int(np % len(self.colors))]
            self.n += 1
