import alsaaudio
import time
import audioop
import alsaseq

class MidiController(object):
    """
    controller that can connect to midi devices.
    """
    def __init__(self, device_id=20, name="Arduino Leonardo",
                 portin=0, portout=0, numchannels=5, numinputs=16):
        self.alsaseq = alsaseq
        self.inputed = {}
        self.positions = []
        self.alsaseq.client(name, 1, 0, False)
        self.alsaseq.connectfrom(portin, device_id, portout)
        # starts at 0 so -1
        self.numchannels = numchannels
        self.numinputs = numinputs
        for y in range(0, self.numinputs):
            for x in range(0, self.numchannels):
                pos = (x, y)
                self.inputed[pos] = 0
                self.positions.append(pos)

    def getButton(self, chan=0, button=0):
        if self.alsaseq.inputpending():
            ev = list(self.alsaseq.input())
            datatuple = ev[7]
            pos = (datatuple[0], datatuple[4])
            data = datatuple[5]
            self.inputed[pos] = data
        pos = (chan, button)
        return self.inputed[pos] + 1

    def getInputed(self):
        return self.inputed


def TestMidiC():
    mc = MidiController()
    while(True):
        for y in range(0, mc.numinputs):
            for x in range(0, mc.numchannels):
                key = (x, y)
                value = mc.getInputed()[key]
                chan, button = key
                while(mc.getInputed()[key] == 0):
                    value = mc.getButton(chan, button)
        # for x in range(0, 16):
        #     for y in range(0, 4):
        #         value = mc.getButton(x, y)
        #         while(value == 0):
        #             value = mc.getButton(x, y)
        # if(time.time() - previous > 10):
        #     return


class AudioController(object):
    """
    controller that is connected to sound input (microphone)
    the lower the period and the higher the rate. the faster the sampeling.
    """
    def __init__(self, channel=1, rate=8000, period=160):
        self.audio = alsaaudio
        self.time = time
        self.audioop = audioop
        self.inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK)
        self.inp.setchannels(channel)
        self.inp.setrate(rate)
        self.inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        self.inp.setperiodsize(period)

    def getinput(self):
        l, data = self.inp.read()
        if l:
            return self.audioop.max(data, 2)
        else:
            return None

