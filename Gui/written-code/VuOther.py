from Tools.Graphics import Graphics, BLUE, BLACK
from matrix import matrix_width, matrix_height
from Controllers.Controllers import translate
from Tools.Timing import Timer

import numpy as np
import numpy
import pyaudio
import math
import struct

audio_params = (pyaudio.paInt16, 1, 44100, True, False, 1024)

select = "VisualizerTwo"


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

class Visualizer(object):
    """
    testing with this is cool:
    https://www.youtube.com/watch?v=82Q6DRqf9H4
    https://youtu.be/XzjmPo6qr_0?list=RD05IZxpCWSao
    https://youtu.be/UUIQox072QA?list=RD05IZxpCWSao
    https://youtu.be/JTNXgzSpiTU?list=RD05IZxpCWSao
    https://youtu.be/S5xOj3JGU0c?list=RD05IZxpCWSao
    https://youtu.be/7Ul7uBoewdM?list=RD05IZxpCWSao
    https://youtu.be/B1DDpyt8qyg?list=RD05IZxpCWSao
    https://youtu.be/VwME67reIYk?list=RD05IZxpCWSao
    https://youtu.be/hn_T2rMPL4c?list=RD05IZxpCWSao
    https://youtu.be/U20HZoCnRGA
    https://youtu.be/eRE0dfOfVYE
    """
    def __init__(self):
        self.graphics = Graphics(matrix_width, matrix_height)
        self.graphics.fill(BLUE)
        self.color = BLUE
        
        self.timer = Timer(0)
        
        self.chunk = 1024
        self.scale = 55
        self.exponent = 2
        self.samplerate = 44100	
        self.audio_params = (pyaudio.paInt16, 1, self.samplerate, True, self.chunk)
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.audio_params[0],
                                  channels=self.audio_params[1],
                                  rate=self.audio_params[2],
                                  input=self.audio_params[3],
                                  frames_per_buffer=self.audio_params[4])
        self.data = self.stream.read(self.chunk)

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
        self.graphics.fill(BLACK)
        self.data = self.stream.read(self.chunk)
        levels = self.calculate_levels(self.data, self.chunk, self.samplerate, matrix_height)
        for i, level in enumerate(levels):
            self.color = color_convert(interp_color(level/max(levels)))
            level = max(min(level/self.scale, 1.0), 0.0)
            level = level**self.exponent
            level = int(level*0xff)
            self.graphics.drawLine(0, i, level, i, self.color)
        return self.graphics.getSurface()

    def __del__(self):
        print("Closing Stream")
        self.stream.close()
        self.p.terminate()

class VisualizerTwo(object):
    def __init__(self):
        self.graphics = Graphics(matrix_width, matrix_height)
        self.graphics.fill(BLUE)
        self.color = BLUE
        
        self.timer = Timer(0)
        
        self.chunk = 1024
        self.scale = 55
        self.exponent = 2
        self.samplerate = 44100	
        self.audio_params = (pyaudio.paInt16, 1, self.samplerate, True, self.chunk)
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.audio_params[0],
                                  channels=self.audio_params[1],
                                  rate=self.audio_params[2],
                                  input=self.audio_params[3],
                                  frames_per_buffer=self.audio_params[4])
        self.data = self.stream.read(self.chunk)

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
        self.graphics.fill(BLACK)
        if self.stream.get_read_available():
            self.data = self.stream.read(self.chunk)
        levels = self.calculate_levels(self.data, self.chunk, self.samplerate, matrix_height)
        for i, level in enumerate(levels):
            self.color = color_convert(interp_color(level/max(levels)))
            level = max(min(level/self.scale, i), 0.0)
            level = level**self.exponent
            level = int(level*0xff)
            self.graphics.drawLine(0, i, level, i, self.color)
        return self.graphics.getSurface()

    def __del__(self):
        print("Closing Stream")
        self.stream.close()
        self.p.terminate()


class VisualizerCircle(object):
    def __init__(self):
        self.graphics = Graphics(matrix_width, matrix_height)
        self.graphics.fill(BLUE)
        self.color = BLUE
        
        self.timer = Timer(0)
        
        self.chunk = 1024
        self.scale = 55
        self.exponent = 2
        self.samplerate = 44100	
        self.audio_params = (pyaudio.paInt16, 1, self.samplerate, True, self.chunk)
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.audio_params[0],
                                  channels=self.audio_params[1],
                                  rate=self.audio_params[2],
                                  input=self.audio_params[3],
                                  frames_per_buffer=self.audio_params[4])
        self.data = self.stream.read(self.chunk)

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
        self.graphics.fill(BLACK)
        if self.stream.get_read_available():
            self.data = self.stream.read(self.chunk)
        levels = self.calculate_levels(self.data, self.chunk, self.samplerate, matrix_height)
        for i, level in enumerate(levels):
            self.color = color_convert(interp_color(level/max(levels)))
            level = max(min(level/self.scale, 1.0), 0.0)
            level = level**self.exponent
            level = int(level*0xff)
            self.graphics.drawCircle(matrix_width/2, matrix_height/2, level, self.color)
        return self.graphics.getSurface()

    def __del__(self):
        print("Closing Stream")
        self.stream.close()
        self.p.terminate()

