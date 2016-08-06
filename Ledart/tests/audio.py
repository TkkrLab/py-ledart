import pyaudio
import numpy as np
import math

audio_params = (pyaudio.paInt16, 1, 44100, True, True, 1024)


class PyAudioController(object):
    def __init__(self, format=pyaudio.paInt16, channels=1, rate=44100,
                 input=True, output=False, frames=1024):
        self.format = format
        self.channels = channels
        self.rate = rate
        self.input = input
        self.output = output
        self.frames = frames

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.format,
                                  channels=self.channels,
                                  rate=self.rate,
                                  input=self.input,
                                  output=self.output,
                                  frames_per_buffer=self.frames
                                  )

    def rms(self, buff):
        rms_val = math.sqrt(sum(np.multiply(buff, buff)) / len(buff))
        return rms_val

    def colorconvertif(self, color, length=1):
        # length is used to say how many bytes long.
        temp = []
        for c in color:
            temp.append(float(c / (2 ** (length * 8))))

    def colorconvertfi(self, color):
        temp = []
        for c in color:
            temp.append(int(0xff * c))
        return tuple(temp)

    def interp_color(self, pos):
        c = [(14, 82, 127),
             (69, 138, 44),
             (208, 203, 57),
             (196, 28, 28)]
        f = np.divide(c, 255.)
        sector1 = max(min((pos * len(f)) - 0.5, float(len(f) - 1)), 0.)
        sector2 = max(min((pos * len(f)) + 0.5, float(len(f) - 1)), 0.)
        f1 = f[int(sector1)]
        f2 = f[int(sector2)]
        blend = sector1 - int(sector1)
        return (f2 * blend) + (f1 * (1. - blend))

    def getaudio(self):
        try:
            raw = self.stream.read(audio_params[5])
        except IOError as e:
            if e[1] != pyaudio.paInputOverFlowed:
                raise
            else:
                print("Warning: audio input buffer overflow")
            raw = '\x00' * audio_params[5]
        return np.array(np.frombuffer(raw, np.int16), dtype=np.float64)
