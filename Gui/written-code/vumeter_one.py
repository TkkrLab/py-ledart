from Graphics.Graphics import Graphics, BLUE, BLACK, WHITE, GREEN, RED
from matrix import *
from Controllers.Controllers import translate
from scipy.signal import hilbert
import numpy as np
import pyaudio
import math
import pylab
import cmath

audio_params = (pyaudio.paInt16, 1, 44100, True, False, 1024)

select = "VuBarVerti"


def rms(buff):
    rms_val = math.sqrt(sum(np.multiply(buff, buff)) / len(buff))
    return rms_val


def color_convert(color):
    temp = []
    for c in color:
        temp.append(int(0xff*c))
    return tuple(temp)


def interp_color(pos):
    c = [(14, 82, 127),
         (69, 138, 44),
         (208, 203, 57),
         (196, 28, 28)]
    f = np.divide(c, 255.)
    sector1 = max(min((pos*len(f))-0.5, float(len(f)-1)), 0.)
    sector2 = max(min((pos*len(f))+0.5, float(len(f)-1)), 0.)
    f1 = f[int(sector1)]
    f2 = f[int(sector2)]
    blend = sector1 - int(sector1)
    return (f2*blend) + (f1*(1. - blend))


class VuFlash(object):
    def __init__(self):
        self.graphics = Graphics(matrix_width, matrix_height)
        self.graphics.fill(BLUE)
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=audio_params[0],
                                  channels=audio_params[1],
                                  rate=audio_params[2],
                                  input=audio_params[3],
                                  output=audio_params[4],
                                  frames_per_buffer=audio_params[5]
                                  )
        self.color = BLUE

    def getaudio(self):
        try:
            raw = self.stream.read(audio_params[5])
        except IOError as e:
            if e[1] != pyaudio.paInputOverFlowed:
                raise
            else:
                print("Warning: audio input buffer overflow")
            raw = '\x00' * self.audio_params[5]
        return np.array(np.frombuffer(raw, np.int16), dtype=np.float64)

    def generate(self):
        audio = self.getaudio()
        rmsed = translate(rms(audio), 0, 0xffff/5, 0, matrix_height)
        self.color = interp_color(rms(audio/10000))
        self.color = color_convert(self.color)
        self.graphics.fill(self.color)
        return self.graphics.getSurface()


class VuBarVerti(object):
    def __init__(self):
        self.graphics = Graphics(matrix_width, matrix_height)
        self.graphics.fill(BLUE)
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=audio_params[0],
                                  channels=audio_params[1],
                                  rate=audio_params[2],
                                  input=audio_params[3],
                                  output=audio_params[4],
                                  frames_per_buffer=audio_params[5])
        self.color = BLUE

    def getaudio(self):
        try:
            raw = self.stream.read(audio_params[5])
        except IOError as e:
            if e[1] != pyaudio.paInputOverflowed:
                raise
            else:
                print("Warning: audio input buffer overflow")
            raw = '\x00' * self.audio_params[5]
        return np.array(np.frombuffer(raw, np.int16), dtype=np.float64)

    def generate(self):
        self.graphics.fill(BLACK)
        audio = self.getaudio()
        rmsed = translate(rms(audio), 0, ((2**16)/2)/2, 0, matrix_width*2)
        self.color = interp_color(rms(audio/10000))
        self.color = color_convert(self.color)
        for i in range(0, matrix_height):
            self.graphics.drawLine(0, i, rmsed, i, self.color)
        return self.graphics.getSurface()


class VuBarHori(object):
    def __init__(self):
        self.graphics = Graphics(matrix_width, matrix_height)
        self.graphics.fill(BLUE)
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=audio_params[0],
                                  channels=audio_params[1],
                                  rate=audio_params[2],
                                  input=audio_params[3],
                                  output=audio_params[4],
                                  frames_per_buffer=audio_params[5])
        self.color = BLUE

    def getaudio(self):
        try:
            raw = self.stream.read(audio_params[5])
        except IOError as e:
            if e[1] != pyaudio.paInputOverflowed:
                raise
            else:
                print("Warning: audio input buffer overflow")
            raw = '\x00' * self.audio_params[5]
        return np.array(np.frombuffer(raw, np.int16), dtype=np.float64)

    def generate(self):
        self.graphics.fill(BLACK)
        audio = self.getaudio()
        rmsed = translate(rms(audio), 0, ((2**16)/2)/2, 0, matrix_height*2)
        self.color = interp_color(rms(audio/10000))
        self.color = color_convert(self.color)
        for i in range(0, matrix_width):
            self.graphics.drawLine(i, 0, i, rmsed, self.color)
        return self.graphics.getSurface()

class Slide_filter():
    def __init__(self, a):
        self.buffer = np.zeros(2, dtype='complex128')
        self.a = a
    def filter(self, input_buff):
        b = np.zeros(len(input_buff), dtype='complex128')
        for i in range(len(input_buff)):
            self.buffer[1] = self.buffer[0]
            self.buffer[0] = self.buffer[1] + ((input_buff[i]-self.buffer[1]) / self.a)
            b[i] = self.buffer[0]
        return b

class Visualizer(object):
    def __init__(self):
        self.graphics = Graphics(matrix_width, matrix_height)
        self.graphics.fill(BLUE)
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=audio_params[0],
                                  channels=audio_params[1],
                                  rate=audio_params[2],
                                  input=audio_params[3],
                                  output=audio_params[4],
                                  frames_per_buffer=audio_params[5])
        self.color = BLUE
        self.scale = 0.04
        self.f = Slide_filter(50)
        self.line_points = np.zeros(audio_params[5]*2)
        self.wave_display = np.zeros(audio_params[5])

    def getaudio(self):
        try:
            raw = self.stream.read(audio_params[5])
        except IOError as e:
            if e[1] != pyaudio.paInputOverflowed:
                raise
            else:
                print("Warning: audio input buffer overflow")
            raw = '\x00' * self.audio_params[5]
        return np.array(np.frombuffer(raw, np.int16), dtype=np.float64)

    def generate(self):
        self.graphics.fill(BLACK)
        self.width = matrix_width
        self.height = matrix_height
        audio = self.getaudio()
        self.line_colour = interp_color(rms(audio/10000.))
        shifted = hilbert(audio)*self.scale
        shifted = np.add(shifted, self.width/2+(self.height/2)*1j)
        shifted = self.f.filter(shifted)
        wave_offset_y = self.height*0.5*(1-math.sqrt(2)) # To account for the 200+200j added earlier
        wave_offset_x = (self.width - len(shifted)/2)/2
        for i, co_ord in enumerate(shifted[::2]):
            self.wave_display[2*i] = i + wave_offset_x
            self.wave_display[(2*i)+1] = abs(co_ord) + wave_offset_y
        return self.graphics.getSurface()






