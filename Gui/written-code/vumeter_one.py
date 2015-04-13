from Graphics.Graphics import Graphics, BLUE, BLACK, WHITE, GREEN, RED
from matrix import *
from Controllers.Controllers import translate
import numpy as np
import pyaudio
import math
import pylab
import cmath

audio_params = (pyaudio.paInt16, 1, 44100, True, True, 1024)


def rms(buff):
    rms_val = math.sqrt(sum(np.multiply(buff, buff))/len(buff))
    return rms_val


class fftPat(object):
    def __init__(self):
        self.graphics = Graphics(matrix_width, matrix_height)
        self.graphics.fill(BLUE)
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format = audio_params[0],
                                  channels = audio_params[1],
                                  rate = audio_params[2],
                                  input = audio_params[3],
                                  output = audio_params[4],
                                  frames_per_buffer = audio_params[5])
        self.color = BLUE
    def getaudio(self):
        try:
            raw = self.stream.read(audio_params[5])
        except IOError as e:
            if e[1] != pyaudio.paInputOverflowed:
                raise
            else:
                print "Warning: audio input buffer overflow"
            raw = '\x00' * self.audio_params[5]
        return np.array(np.frombuffer(raw, np.int16), dtype=np.float64)
    def generate(self):
        audio = self.getaudio()
        rmsed = rms(audio/1000)
        self.graphics.fill(BLACK)
        for i in range(0, matrix_height):
            self.graphics.drawLine(0, i, rmsed, i, self.color)
        return self.graphics.getSurface()
