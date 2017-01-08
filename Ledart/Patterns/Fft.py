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

        self.fouriers = []

    def get_complex_abs(self, value):
        return ((value.real ** 2) + (value.imag ** 2)) ** 0.5

    def calc_levels(self, data):
        # convert raw data to numpy array
        data = struct.unpack("%dh" % (len(data) / 2), data)
        data = numpy.array(data, dtype='h')
        # apply fft - real data so rfft is used
        fourier = numpy.fft.rfft(data, n=len(data), norm='ortho')
        fourier = [self.get_complex_abs(val) for i, val in enumerate(fourier[:len(fourier)-1])]
        fourier = [(val) / max(fourier) if val != 0 else 0 for i, val in enumerate(fourier)]
        # fourier = [translate(val, min(fourier), max(fourier), 1, self.height * 0.8) * math.log(i + 1)  for i, val in enumerate(fourier)]
        return fourier

    def mean(self, a):
        return sum(a) / len(a)

    def average_lists(self, lists):
        return map(self.mean, zip(*lists))

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
                    if self.mode == 1:
                        c = [int(0xff * c) for c in colorsys.hsv_to_rgb(f, 1, 1)]
                        self.draw_line(x, self.height - self.height * f, x, self.height, c)
                    # elif self.mode == 2:
                    #     self.draw_pixel(x, self.height - fourier_data[x], GREEN)
                    # elif self.mode == 3:
                    #     self.draw_line(x, (self.height / 2) - fourier_data[x], x, (self.height / 2) + fourier_data[x], GREEN)
                    # elif self.mode == 4:
                    #     if x >= (self.width - 1):
                    #         self.draw_pixel(x, self.height - fourier_data[x], GREEN)
                    #     else:
                    #         hl = self.height - fourier_data[x]
                    #         hr = self.height - fourier_data[x + 1]
                    #         self.draw_line(x, hl, x, hr, GREEN)
                    # else:
                    #     raise Exception("Unknown Mode")
            except Exception as e:
                traceback.print_exc()
                if e.message != "not a whole number of frames":
                    raise e
