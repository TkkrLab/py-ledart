from __future__ import division

from Ledart.Tools import Graphics
from Ledart.Tools import BLUE

class Mandelbrot(Graphics):
    def __init__(self, **kwargs):
        Graphics.__init__(self, **kwargs)
        self.scale = 1
        self.offset = 0
        self.zdistance = 0
        self.fill(BLUE)

    def linspace(self, lower, upper, length):
        return [lower + x*(upper-lower)/length for x in range(length)]

    def translate(self, value, leftMin, leftMax, rightMin, rightMax):
        # Figure out how 'wide' each range is
        leftSpan = float(leftMax - leftMin) + 0.0000000001
        rightSpan = float(rightMax - rightMin) + 0.000000001

        # Convert the left range into a 0-1 range (float)
        valueScaled = float(value - leftMin) / float(leftSpan)

        # Convert the 0-1 range into a value in the right range.
        return rightMin + (valueScaled * rightSpan)

    def mandelbrot(self, z, maxiter):
        c = z
        for n in range(maxiter):
            if abs(z) > 2:
                return n
            z = z*z + c
        return maxiter

    def mandelbrot_set(self, xmin, xmax, ymin, ymax, width, height, maxiter=0xff):
        r1 = self.linspace(xmin, xmax, width)
        r2 = self.linspace(ymin, ymax, height)
        return (r1, r2, [self.mandelbrot(complex(r, i), maxiter) for r in r1 for i in r2])


    def generate(self):
        r1, r2, mandel_set = self.mandelbrot_set((-2.0 + self.offset) / self.scale,
                                                 (0.5 + self.offset) / self.scale,
                                                 (-1.25 + self.offset) / self.scale,
                                                 (1.25 + self.offset) / self.scale,
                                                 self.height, self.width)
        for i, (x, y) in enumerate(self.get_points()):
            c = self.translate(float(mandel_set[i]),
                               float(min(mandel_set)),
                               float(max(mandel_set)),
                               float(0xff),
                               float(0x00))
            self[x, y] = [int(c), ]*3