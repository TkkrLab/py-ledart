from Ledart.Tools.Graphics import Graphics, BLUE, BLACK, GREEN
from Ledart.utils import translate

import traceback
import alsaaudio
import struct
import numpy
import time


class Fft(Graphics):
    def __init__(self, **kwargs):
        Graphics.__init__(self, **kwargs)

        self.mode = kwargs.get('mode', 3)
        self.topcolor = kwargs.get('topcolor', GREEN)
        self.barcolor = kwargs.get('barcolor', BLUE)

        self.sample_rate = 44100 / 4
        self.chunk = self.width * 2
        self.no_channels = 1

        self.stream = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL)
        self.stream.setchannels(self.no_channels)
        self.stream.setrate(self.sample_rate)
        self.stream.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        self.stream.setperiodsize(self.chunk)

        self.fouriers = []

    def calc_levels(self, data):
        # convert raw data to numpy array
        data = struct.unpack("%dh" % (len(data) / 2), data)
        data = numpy.array(data, dtype='h')
        # apply fft - real data so rfft is used
        fourier = numpy.fft.rfft(data)
        fourier = [int(abs(val.real) / 4000) for val in fourier[:len(fourier)-1]]
        return fourier

    def mean(self, a):
        return sum(a) / len(a)

    def generate(self):
        self.fill(BLACK)

        l, data = self.stream.read()

        if l:
            try:
                self.fouriers.append(self.calc_levels(data))
                if len(self.fouriers) > 4:
                    del self.fouriers[0]

                matrix = map(self.mean, zip(*self.fouriers))

                for x in xrange(len(matrix)):
                    if self.mode == 1:
                        self.draw_line(x, self.height - matrix[x], x, self.height, BLUE)
                    elif self.mode == 2:
                        self.draw_pixel(x, self.height - matrix[x], GREEN)
                    elif self.mode == 3:
                        self.draw_line(x, (self.height / 2) - matrix[x], x, (self.height / 2) + matrix[x], GREEN)
                    elif self.mode == 4:
                        if x >= (self.width - 1):
                            self.draw_pixel(x, self.height - matrix[x], GREEN)
                        else:
                            hl = self.height - matrix[x]
                            hr = self.height - matrix[x + 1]
                            self.draw_line(x, hl, x, hr, GREEN)
                    else:
                        raise Exception("Unknown Mode")
            except Exception as e:
                traceback.print_exc()
                if e.message != "not a whole number of frames":
                    raise e
