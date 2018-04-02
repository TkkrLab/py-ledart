from Ledart.utils import chunked, translate, chunks, mean, average_lists
from Ledart.Tools.Graphics import Graphics, BLUE, WHITE, BLACK

import colorsys
import pyaudio
import struct
import random

def colors(N):
    HSV_tuples = [(x*1.0/N, 1.0, 1.0) for x in range(N)]
    RGB_tuples = list(map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples))
    return RGB_tuples

class SoundColor(Graphics):
    def __init__(self, **kwargs):
        super(Graphics, self).__init__(**kwargs)
        self.mode = kwargs.get("mode", 0)
        self.audioChannels = 1
        self.rate = 44100
        self.chunksize = 1024

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt32,
                                  channels=self.audioChannels,
                                  rate=self.rate,
                                  input=True,
                                  output=False,
                                  frames_per_buffer=self.chunksize,
                                  stream_callback=self.audioCallback)

        self.stream.start_stream()

        self.data = None
        self.new_data = False

        self.height_wave_data = []
        self.width_wave_data = []
        self.avg_value = kwargs.get("num_avg", 2)

        self.lines = []
        self.max_lines = 4
        self.index = 0
        # self.palette = seaborn.color_palette('Blues_d', n_colors=0xff + 1)
        self.palette = colors(0xff + 1)
        self.offset = 0

    def audioCallback(self, in_data, frame_count, time_info, status):
        self.data = struct.unpack("%si" % int(len(in_data) / 4), in_data)
        self.new_data = True
        return (None, pyaudio.paContinue)

    def calc_data(self, length, scale):
        data = []
        for i, chunk in enumerate(chunks(self.data, int(self.chunksize / length))):
            # value = self.height / 2 + self.height * ((mean(chunk) / self.chunksize) / 200000)
            value = scale / 2 + scale * (chunk[0] / (2 ** 32)) * 20

            # lvalue = list([((ch / (2 ** 30))  + 2) * self.height / 4 for ch in chunk])
            # value = int(sum(lvalue) / len(lvalue))
            
            data.append(value)
        return data

    def generate(self):
        self.fill(BLACK)
        if self.new_data:
            if self.mode == 0:
                self.width_wave_data.append(self.calc_data(self.width, self.height))
                if(len(self.width_wave_data) > self.avg_value):
                    del self.width_wave_data[0]

                xdata = average_lists(self.width_wave_data)
                xdata_min = min(xdata)
                xdata_max = max(xdata)

                for x in range(self.width):
                    c = translate(xdata[x], xdata_min, xdata_max, 0, 0xff)
                    c = int(abs(c))
                    color = self.palette[int(c)]
                    color = [int(c * 0xff) for c in color]
                    for y in range(self.height):
                        self.draw_pixel(x, y, color)
            if self.mode == 1:
                self.height_wave_data.append(self.calc_data(self.height, self.width))
                if(len(self.height_wave_data) > self.avg_value):
                    del self.height_wave_data[0]

                ydata = average_lists(self.height_wave_data)
                ydata_min = min(ydata)
                ydata_max = max(ydata)

                for y in range(self.height):
                    c = translate(ydata[y], ydata_min, ydata_max, 0, 0xff)
                    c = int(abs(c))
                    color = self.palette[int(c)]
                    color = [int(c * 0xff) for c in color]
                    for x in range(self.width):
                        self.draw_pixel(x, y, color)
            if self.mode == 2:
                self.width_wave_data.append(self.calc_data(self.width, self.height))
                if(len(self.width_wave_data) > self.avg_value):
                    del self.width_wave_data[0]

                self.height_wave_data.append(self.calc_data(self.height, self.width))
                if(len(self.height_wave_data) > self.avg_value):
                    del self.height_wave_data[0]
                
                ydata = average_lists(self.height_wave_data)
                ydata_min = min(ydata)
                ydata_max = max(ydata)

                xdata = average_lists(self.width_wave_data)
                xdata_min = min(xdata)
                xdata_max = max(xdata)

                for x in range(self.width):
                    for y in range(self.height):
                        xc = translate(xdata[x], xdata_min, xdata_max, 0, 0xff)
                        yc = translate(ydata[y], ydata_min, ydata_max, 0, 0xff)
                        c = abs((xc + yc) / 2)
                        color = self.palette[int(c)]
                        color = [int(c * 0xff) for c in color]
                        self.draw_pixel(x, y, color)


class VUmeter(Graphics):
    def __init__(self, **kwargs):
        Graphics.__init__(self, **kwargs)

        self.mode = kwargs.get('mode', 3)
        
        self.sample_rate = int(44100 / 4)
        self.chunk = self.width * 2
        self.no_channels = 1
        self.average_size = 10

        self.stream = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL)
        self.stream.setchannels(self.no_channels)
        self.stream.setrate(self.sample_rate)
        self.stream.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        self.stream.setperiodsize(self.chunk)

        self.chunks = []

    def mean(self, a):
        return sum(a) / len(a)

    def average_lists(self, lists):
        return list(map(self.mean, zip(*lists)))

    def draw_pixel(self, x, y, color):
        color = [int(c * 0xff) for c in colorsys.hsv_to_rgb(y / float(self.height), 1, 1)]
        Graphics.draw_pixel(self, x, y, color)

    def generate(self):
        self.fill(BLACK)
        l, data = self.stream.read()
        h = 0
        if l:
            data = struct.unpack("%dh" % (len(data) / 2), data)
            self.chunks.append(data)
            if len(self.chunks) > self.average_size:
                del self.chunks[0]
            data = self.average_lists(self.chunks)
            # scale values to the window.
            data = [translate(val, min(data), max(data), 1, self.height * 0.8) for val in data]

            for x in range(len(data)):
                if self.mode == 0:
                    self.draw_line(x, self.height - data[x], x, self.height, BLUE)
                elif self.mode == 1:
                    self.draw_pixel(x, self.height - data[x], BLUE)
                elif self.mode == 2:
                    self.draw_line(x, (self.height / 2) - data[x] / 2, x, (self.height / 2) + data[x] / 2, BLUE)
                elif self.mode == 3:
                    if x >= (self.width - 1):
                        self.draw_pixel(x, self.height - data[x], BLUE)
                    else:
                        hl = self.height - data[x]
                        hr = self.height - data[x + 1]
                        self.draw_line(x, hl, x, hr, BLUE)