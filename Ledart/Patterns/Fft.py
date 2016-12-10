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
        self.sound_mode = kwargs.get('soundmode', 'mono')
        self.topcolor = kwargs.get('topcolor', GREEN)
        self.barcolor = kwargs.get('barcolor', BLUE)

        if(self.sound_mode == 'mono'):
            self.no_channels = 1
        if(self.sound_mode == 'stereo'):
            self.no_channels = 2

        self.sample_rate = 44100 / 4
        self.chunk = self.width * 2

        self.stream = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL)
        self.stream.setchannels(self.no_channels)
        self.stream.setrate(self.sample_rate)
        self.stream.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        self.stream.setperiodsize(self.chunk)

    def calc_levels(self, data):
        # convert raw data to numpy array
        data = struct.unpack("%dh" % (len(data) / 2), data)
        data = numpy.array(data, dtype='h')
        # apply fft - real data so rfft is used
        fourier = numpy.fft.rfft(data)
        fourier = [abs(val.real) / 10000 for val in fourier[:len(fourier)-1]]
        return fourier


    def generate(self):
        self.fill(BLACK)

        l, data = self.stream.read()

        if l:
            try:
                matrix = self.calc_levels(data)
                # self.min = min(matrix)
                # self.max = max(matrix)
                for x in xrange(len(matrix)):
                    if self.mode == 1:
                        h = self.height - matrix[x]
                        self.draw_line(x, self.height - matrix[x], x, self.height, BLUE)
                    elif self.mode == 2:
                        self.draw_pixel(x, self.height - matrix[x], GREEN)
                    elif self.mode == 3:
                        self.draw_line(x, (self.height / 2) - matrix[x], x, (self.height / 2) + matrix[x], GREEN)
                    else:
                        if x >= (self.width - 1):
                            self.draw_pixel(x, self.height - matrix[x] + self.min, GREEN)
                        else:
                            hl = self.height - matrix[x] + self.min
                            hr = self.height - matrix[x + 1] + self.min
                            self.draw_line(x, hl, x, hr, GREEN)
            except Exception as e:
                traceback.print_exc()
                if e.message != "not a whole number of frames":
                    raise e
