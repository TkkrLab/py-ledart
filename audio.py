import pyaudio
import numpy as np
import math

audio_params = (pyaudio.paInt16, 1, 44100, True, True, 1024)


def rms(buff):
    rms_val = math.sqrt(sum(np.multiply(buff, buff)) / len(buff))
    return rms_val


def color_convert(color):
    temp = []
    for c in color:
        temp.append(int(0xff * c))
    return tuple(temp)


def interp_color(pos):
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

p = pyaudio.PyAudio()
stream = p.open(format=audio_params[0],
                channels=audio_params[1],
                rate=audio_params[2],
                input=audio_params[3],
                output=audio_params[4],
                frames_per_buffer=audio_params[5]
                )


def getaudio():
    try:
        raw = stream.read(audio_params[5])
    except IOError as e:
        if e[1] != pyaudio.paInputOverFlowed:
            raise
        else:
            print("Warning: audio input buffer overflow")
        raw = '\x00' * audio_params[5]
    return np.array(np.frombuffer(raw, np.int16), dtype=np.float64)
