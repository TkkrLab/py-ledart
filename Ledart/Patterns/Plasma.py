from Ledart.Tools.Graphics.RGBColorTools import ColorRGBOps
from Ledart.Tools.Graphics.ConvertColors import HSVtoRGB
from Ledart.Tools.Graphics import Graphics, BLACK, BLUE
from Ledart.Tools.Controllers import translate
from Ledart.Tools.Palet import PaletGenerate
from Ledart.Tools.Timing import Timer
from Ledart import constrain

from math import sin, cos, sqrt, pi, radians, hypot
import time
import random
import colorsys


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

        self.x_range = range(0, self.width, 1)
        self.y_range = range(0, self.height, 1)

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
        for x in range(0, 0xff * 3, 1):
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
                color_shift = self.palette[int(paletteShift % len(self.palette))]
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


class Plasma(Graphics):
    def __init__(self, **kwargs):
        Graphics.__init__(self, **kwargs)
        self.plasma = Graphics(surface=self)
        self.tshift = 0.0
        self.cshift = 0.0

    def dist(self, x1, y1, x2, y2):
        return hypot(x1 - x2, y1 - y2)

    def generate(self):
        self.tshift += 0.07
        self.cshift += 0.0

        for point in self.get_points():
            x, y = point
            w, h = self.width, self.height
            # cv = (1.0 + sin(hypot((x - w / 2.0), (y - h / 2.0)) / 8.0)) / 2
            # cv = (1.0 + sin(x / 16.0)) / 2.0 + (1.0 + sin(y / 16.0) / 2.0)

            # cv = (
            #         (1 + sin(x / 8.0) / 2.0)
            #       + (1 + sin(y / 8.0) / 2.0)
            #       + (1 + sin((x + y) / 8.0) / 2.0)
            #       + (1 + sin(hypot(x, y) / 8.0) / 2.0))
            # cv = (self.cshift + cv) % 1.0
            
            x_offset = w * sin(radians(self.tshift)) + w
            y_offset = h * cos(radians(self.tshift)) + h

            # cv = ((1 + sin(x_offset + self.dist(x + self.tshift, y, 128.0, 128.0) / 60.0) / 2)
            #       + (1 + sin(y_offset + self.dist(x + self.tshift, y, 64.0, 64.0) / 60.0) / 2)
            #       + (1 + sin(x_offset + self.dist(x, y / 7.0, 192.0, 64) / 60.0) / 2)
            #       + (1 + sin(y_offset + self.dist(x, y, 192.0, 100.0) / 60.0) / 2))

            stretch = 256
            cv = (sin(self.dist(x + x_offset + self.tshift, y + y_offset, self.height, self.width) / stretch)
                 + sin(self.dist(x + x_offset, y + y_offset, self.width, self.height) / stretch)
                 + sin(self.dist(x + x_offset, y + y_offset + self.tshift, self.height, self.width) / stretch)
                 + sin(self.dist(x + x_offset, y + y_offset, self.width, self.height) / stretch))

            color = [int(0xff * c) for c in colorsys.hsv_to_rgb(self.cshift + cv, 1, 1)]
            self.draw_pixel(x, y, color)
