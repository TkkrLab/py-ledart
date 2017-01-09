from Ledart.Tools.Graphics import Graphics, BLUE, BLACK, GREEN
from Ledart.utils import translate

import traceback
import alsaaudio
import colorsys
import struct
import numpy
import time
import math

stream = None


class Fft(Graphics):
    def __init__(self, **kwargs):
        Graphics.__init__(self, **kwargs)

        self.mode = kwargs.get('mode', 3)
        self.topcolor = kwargs.get('topcolor', GREEN)
        self.barcolor = kwargs.get('barcolor', BLUE)

        self.sample_rate = 44100 / 4
        self.chunk = self.width * 2
        self.no_channels = kwargs.get('channels', 1)

        self.stream = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL)
        self.stream.setchannels(self.no_channels)
        self.stream.setrate(self.sample_rate)
        self.stream.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        self.stream.setperiodsize(self.chunk)

        self.color_pallet = [c / self.height for c in range(self.height)]

        # self.window = numpy.bartlett(self.width)
        # self.window = numpy.blackman(self.width)
        self.window = numpy.hamming(self.width)
        # self.window = numpy.hanning(self.width)
        # self.window = numpy.kaiser(self.width, 0)
        # self.window = [1, ] * self.width

        self.fouriers = []

    def get_complex_abs(self, value):
        return ((value.real ** 2) + (value.imag ** 2)) ** 0.5

    def calc_levels(self, data):
        # convert raw data to numpy array
        data = struct.unpack("%dh" % (len(data) / 2), data)
        data = numpy.array(data, dtype='h')
        # apply fft - real data so rfft is used
        fourier = numpy.fft.rfft(data, n=len(data), norm='ortho')
        # get absolute values and apply a window.
        fourier = [self.get_complex_abs(val) * self.window[i] for i, val in enumerate(fourier[:len(fourier)-1])]
        # check if there is anything usefull transform for use if so.
        fourier = [(val) / 16000 if val != 0 else 0 for i, val in enumerate(fourier)]
        return fourier

    def mean(self, a):
        return sum(a) / len(a)

    def average_lists(self, lists):
        return map(self.mean, zip(*lists))

    # override function for special line drawing! 
    # def draw_bar(self, x, y, height):
    #     x, height = int(x), int(height)

    #     for yh in xrange(0, height):
    #         color = [int(c * 0xff) for c in colorsys.hsv_to_rgb(yh / float(self.height), 1, 1)]
    #         self.draw_pixel(x, y + self.height - yh - 1, color)

    # def draw_bartop(self, x, height):
    #     x, height = int(x), int(height)
    #     color = [int(c * 0xff) for c in colorsys.hsv_to_rgb(height / float(self.height), 1, 1)]
    #     self.draw_pixel(x, self.height - height - 1, color)

    def draw_pixel(self, x, y, color):
        color = [int(c * 0xff) for c in colorsys.hsv_to_rgb(y / float(self.height), 1, 1)]
        Graphics.draw_pixel(self, x, y, color)

    def generate(self):
        self.fill(BLACK)

        l, data = self.stream.read()

        if l:
            try:
                self.fouriers.append(self.calc_levels(data))
                if len(self.fouriers) > 5:
                    del self.fouriers[0]

                fourier_data = map(self.mean, zip(*self.fouriers))

                for x, f in enumerate(fourier_data):
                    h = self.height * f
                    if self.mode == 1:
                        self.draw_line(x, self.height, x, self.height - h, BLACK)
                    elif self.mode == 2:
                        self.draw_pixel(x, self.height - h, BLACK)
                    elif self.mode == 3:
                        self.draw_line(x, (self.height / 2) - h, x, (self.height / 2) + h, BLACK)
                    elif self.mode == 4:
                        if x >= (self.width - 1):
                            self.draw_pixel(x, self.height - h, BLACK)
                        else:
                            hl = self.height - self.height * fourier_data[x]
                            hr = self.height - self.height * fourier_data[x + 1]
                            self.draw_line(x, hl, x, hr, BLACK)
                    else:
                        raise Exception("Unknown Mode")
            except Exception as e:
                traceback.print_exc()
                if e.message != "not a whole number of frames":
                    raise e
