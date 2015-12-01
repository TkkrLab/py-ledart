from Tools.Graphics import Graphics, BLACK, BLUE
from Tools.Graphics.ConvertColors import HSVtoRGB
from Tools.Graphics.RGBColorTools import ColorRGBOps
from Tools.Palet import PaletGenerate
from Tools.Timing import Timer
from Tools.Controllers import translate, MidiController
from matrix import matrix_width, matrix_height
from math import sin, cos, sqrt, pi, radians
import time
import random

select = "RainbowEffect"


class RainbowEffect(Graphics):
    """
        this doesn't work for now. will fix later.
    """
    def __init__(self, speed=0.1):
        Graphics.__init__(self, matrix_width, matrix_height)
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
    def __init__(self, speed=4):
        Graphics.__init__(self, matrix_width, matrix_height)
        self.fill(BLACK)
        self.palet = PaletGenerate()
        self.speed = speed

    def generate(self):
        # cycle a bit faster through the palet if we want.
        for i in range(0, self.speed):
            color = self.palet.colorFade()
        self.fill(color)


class PlasmaFifth(Graphics):
    def __init__(self, speed=1):
        Graphics.__init__(self, matrix_width, matrix_height)
        self.plasma = Graphics(matrix_width, matrix_height)

        self.x_range = xrange(0, matrix_width, 1)
        self.y_range = xrange(0, matrix_height, 1)

        self.speed = speed
        self.interval = 1000 / self.speed
        self.time = random.randint(0, 100)
        self.previousTick = 0

        self.angle = 0
        self.mc = MidiController()

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

    def generatePlasmaSurface(self):
        self.angle = self.time % 360
        x_offset = matrix_width * sin(radians(self.angle)) + matrix_width
        y_offset = matrix_height * cos(radians(self.angle)) + matrix_height
        size = 1.5
        # good values: 6.328125 , 0.1328125
        offset = self.mc.getButton(0, 0)
        offset = translate(offset, 0, 128, 0, self.mc.getButton(0, 1))
        fac = self.mc.getButton(0, 2)
        fac = translate(fac, 0, 128, 0, self.mc.getButton(0, 3))
        for y in self.y_range:
            for x in self.x_range:
                c = int(offset + (offset * sin(x_offset + x / (size * 2)))
                        + offset + (offset * sin(y_offset + y / size))
                        + offset + (offset * sin((x_offset + x + y_offset + y)
                                    / (size * 2)))
                        + offset + (offset * sin(sqrt(((x_offset + x) *
                                    (x_offset + x) + (y_offset + y) *
                                    (y_offset + y))) / size))
                        ) / fac
                color = (abs(int(c)),) * 3
                self.plasma.draw_pixel(x, y, color)

    def process(self):
        millis = round(time.time() * 1000)
        if((millis - self.previousTick) >= self.interval):
            self.previousTick = time.time()
            self.time += 1

    def draw(self):
        self.fill(BLACK)
        paletteShift = self.time / self.speed
        self.generatePlasmaSurface()
        for y in self.y_range:
            for x in self.x_range:
                plasma_color = self.plasma.read_pixel(x, y)
                color_shift = self.palette[paletteShift % len(self.palette)]
                r = (plasma_color[0] + color_shift[0])
                g = (plasma_color[1] + color_shift[1])
                b = (plasma_color[2] + color_shift[2])
                color = (r, g, b,)
                # darken the color to create a better contrast
                # also boundery checks make it more smooth in ColorRGBOps
                color = ColorRGBOps.darken(color, 200)
                self.draw_pixel(x, y, color)

    def generate(self):
        self.process()
        self.draw()


class PlasmaFourth(Graphics):
    def __init__(self, speed=1):
        Graphics.__init__(self, matrix_width, matrix_height)
        self.plasma = Graphics(matrix_width, matrix_height)

        self.x_range = xrange(0, matrix_width, 1)
        self.y_range = xrange(0, matrix_height, 1)

        self.speed = speed
        self.interval = 1000 / self.speed
        self.time = random.randint(0, 100)
        self.previousTick = 0

        self.angle = 0
        self.mc = MidiController()

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
        print self.palette[0], self.palette[len(self.palette) - 1]

    def generatePlasmaSurface(self):
        self.angle = self.time
        x_offset = matrix_width * sin(radians(self.angle)) + matrix_width
        y_offset = matrix_height * cos(radians(self.angle)) + matrix_height
        plasma_set = [76, 81, 1, 90, 4, 4, 1, 89, 21, 1]
        fac = translate(plasma_set[7], 0, 128, 0, 8)
        fac2 = translate(plasma_set[8], 0, 128, 0, 8)
        for y in self.y_range:
            for x in self.x_range:
                c = int((plasma_set[0] * 2 * sin((x + x_offset) /
                         plasma_set[4]))
                        + (plasma_set[1] * 2 * sin((y + y_offset) /
                           plasma_set[5]))
                        + (plasma_set[2] * 2 * sin(((x + x_offset) +
                           (y + y_offset)) / plasma_set[6]))
                        + (plasma_set[3] * 2 * sin(sqrt(float((x + x_offset) *
                           (x + x_offset) + (y + y_offset) * (y + y_offset))) /
                            fac))
                        ) / fac2
                color = (int(abs(c)),) * 3
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
                # also boundery checks make it more smooth in ColorRGBOps
                color = ColorRGBOps.darken(color, 50)
                self.draw_pixel(x, y, color)

    def generate(self):
        self.fill(BLACK)
        self.process()
        self.draw()


class RevolvingCircle(Graphics):
    def __init__(self, width=5, speed=1):
        Graphics.__init__(self, matrix_width, matrix_height)
        self.plasma = Graphics(matrix_width, matrix_height)

        self.x_range = xrange(0, matrix_width, 1)
        self.y_range = xrange(0, matrix_height, 1)

        self.speed = speed
        self.interval = 1000 / self.speed
        self.time = random.randint(0, 100)
        self.previousTick = 0
        self.plasma_width = width

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
        x_offset = (matrix_width * sin(radians(self.angle)) +
                    matrix_width * sin(radians(self.angle)))
        y_offset = (matrix_height * cos(radians(self.angle)) +
                    matrix_height * cos(radians(self.angle)))
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
    def __init__(self, speed=10):
        Graphics.__init__(self, matrix_width, matrix_height)
        self.plasma = Graphics(matrix_width, matrix_height)

        self.x_range = xrange(0, matrix_width, 1)
        self.y_range = xrange(0, matrix_height, 1)

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
        x_offset = matrix_width * sin(radians(self.angle)) + matrix_width
        y_offset = matrix_height * cos(radians(self.angle)) + matrix_height
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
    def __init__(self, speed=1):
        Graphics.__init__(self, matrix_width, matrix_height)
        self.plasma = Graphics(matrix_width, matrix_height)

        self.x_range = xrange(0, matrix_width, 1)
        self.y_range = xrange(0, matrix_height, 1)

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
        x_offset = (matrix_width * sin(radians(self.angle)) +
                    matrix_width * sin(radians(self.angle)))
        y_offset = (matrix_height * cos(radians(self.angle)) +
                    matrix_height * cos(radians(self.angle)))
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
    def __init__(self, speed=20):
        Graphics.__init__(self, matrix_width, matrix_height)
        self.plasma = Graphics(width=matrix_width, height=matrix_height)

        self.x_range = xrange(0, matrix_width, 1)
        self.y_range = xrange(0, matrix_height, 1)

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
