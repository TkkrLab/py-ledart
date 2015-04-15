from Graphics.Graphics import Graphics, BLUE, BLACK, WHITE, GREEN, RED
from matrix import *
from Controllers.Controllers import translate
from scipy.signal import hilbert
import numpy as np
import numpy
import pyaudio
import math
import pylab
import cmath
import struct

audio_params = (pyaudio.paInt16, 1, 44100, True, False, 17)

select = "Visualizer"


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


class VuBarVertiPir(object):
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
        self.max = 0

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
        self.color = interp_color(rms(audio/10000))
        self.color = color_convert(self.color)
        for i in range(0, matrix_height):
            rmsed = translate(rms(audio), 0, ((2**16)/2), 0, matrix_width*i)
            self.graphics.drawLine(0, i, rmsed, i, self.color)
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
        self.max = 0

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


class VuBarHoriPir(object):
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
        self.color = interp_color(rms(audio/10000))
        self.color = color_convert(self.color)
        for i in range(0, matrix_width):
            rmsed = translate(rms(audio), 0, ((2**16)/2)/2, 0, matrix_height*i)
            self.graphics.drawLine(i, 0, i, rmsed, self.color)
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

from Timing import Timer

class Visualizer(object):
    def __init__(self):
        self.graphics = Graphics(matrix_width, matrix_height)
        self.graphics.fill(BLUE)
        self.color = BLUE
        
        self.timer = Timer(1/25)
        
        self.chunk = 2**9
        self.scale = 14
        self.exponent = 4.2
        self.samplerate = 22050	
        self.audio_params = (pyaudio.paInt16, 1, self.samplerate, True, self.chunk)
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.audio_params[0],
                                  channels=self.audio_params[1],
                                  rate=self.audio_params[2],
                                  input=self.audio_params[3],
                                  frames_per_buffer=self.audio_params[4])

    def calculate_levels(self, data, chunk, samplerate, points=6, maxi=0):
        # Use FFT to calculate volume for each frequency
        MAX=maxi
         
        # Convert raw sound data to Numpy array
        fmt = "%dH"%(len(data)/2)
        data2 = struct.unpack(fmt, data)
        data2 = numpy.array(data2, dtype='h')
         
        # Apply FFT
        fourier = numpy.fft.fft(data2)
        ffty = numpy.abs(fourier[0:len(fourier)/2])/1000
        ffty1=ffty[:len(ffty)/2]
        ffty2=ffty[len(ffty)/2::]+2
        ffty2=ffty2[::-1]
        ffty=ffty1+ffty2
        ffty=numpy.log(ffty)-2
        fourier = list(ffty)[4:-4]
        fourier = fourier[:len(fourier)/2]
        size = len(fourier)
         
        # Add up for 6 lights
        levels = [sum(fourier[i:(i+size/points)]) for i in xrange(0, size, size/points)][:points]
        return levels 

    def getaudio(self):
        try:
            raw = self.stream.read(self.audio_params[5])
        except IOError as e:
            if e[1] != pyaudio.paInputOverflowed:
                raise
            else:
                print("Warning: audio input buffer overflow")
            raw = '\x00' * self.audio_params[5]
        return np.array(np.frombuffer(raw, np.int16), dtype=np.float64)

    def generate(self):
        data = self.stream.read(self.chunk)
        if self.timer.valid():
            self.graphics.fill(BLACK)
            audio = np.array(np.frombuffer(data, np.int16), dtype=np.float64)
            self.color = color_convert(interp_color(rms(audio/2500)))
            levels = self.calculate_levels(data, self.chunk, self.samplerate, matrix_height)
            for i, level in enumerate(levels):
                level = max(min(level/self.scale, 1.0), 0.0)
                level = level**self.exponent
                level = int(level*0xff)
                height = level
                self.graphics.drawLine(0, i, height, i, self.color)
        return self.graphics.getSurface()

    def __del__(self):
        print("Closing Stream")
        self.stream.close()
        self.p.terminate()






