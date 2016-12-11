from Ledart.utils import chunked, translate
from Ledart.Tools.Graphics import Graphics, BLUE, WHITE, BLACK

import alsaaudio
import audioop
import struct
import time

class VUmeter(Graphics):
    def __init__(self, **kwargs):
        Graphics.__init__(self, **kwargs)

        self.mode = kwargs.get('mode', 3)
        
        self.sample_rate = 44100 / 4
        self.chunk = self.width * 2
        self.no_channels = 1

        self.stream = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL)
        self.stream.setchannels(self.no_channels)
        self.stream.setrate(self.sample_rate)
        self.stream.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        self.stream.setperiodsize(self.chunk)

        self.chunks = []

    def mean(self, a):
        return sum(a) / len(a)

    def average_lists(self, lists):
        return map(self.mean, zip(*lists))

    def generate(self):
        self.fill(BLACK)
        l, data = self.stream.read()
        h = 0
        if l:
            data = struct.unpack("%dh" % (len(data) / 2), data)
            self.chunks.append(data)
            if len(self.chunks) > 10:
                del self.chunks[0]
            data = self.average_lists(self.chunks)
            # scale values to the window.
            data = [translate(val, min(data), max(data), 1, self.height * 0.8) for val in data]

            for x in xrange(len(data)):
                if self.mode == 1:
                    self.draw_line(x, self.height - data[x], x, self.height, BLUE)
                elif self.mode == 2:
                    self.draw_pixel(x, self.height - data[x], BLUE)
                elif self.mode == 3:
                    self.draw_line(x, (self.height / 2) - data[x] / 2, x, (self.height / 2) + data[x] / 2, BLUE)
                elif self.mode == 4:
                    if x >= (self.width - 1):
                        self.draw_pixel(x, self.height - data[x], BLUE)
                    else:
                        hl = self.height - data[x]
                        hr = self.height - data[x + 1]
                        self.draw_line(x, hl, x, hr, BLUE)
            # for x, data in chunked(data, len(data) / self.width):
            #     if not (len(data) & 1):
            #         h = audioop.max(data, 2) / 100
            #     color = [min(h, 0xff), max(0xff - h, 0), 0]
            #     self.draw_line(x, self.height, x, self.height - h, color)