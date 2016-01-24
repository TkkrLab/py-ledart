import sys

import alsaaudio
import time
import audioop
import alsaseq

try:
    from PygameController import PygameController, PygameDummyController
except Exception as e:
    print("pygamecontroller>> " + str(e))


def translate(value, leftmin, leftmax, rightmin, rightmax):
    leftspan = leftmax - leftmin
    rightspan = rightmax - rightmin
    valuescaled = float(value - leftmin) / float(leftspan)
    return rightmin + (valuescaled * rightspan)


class DummyController(object):
    def __init__(self, plugged=0, **kwargs):
        self.value = 0
        self.increment = 50

    def getValue(self):
        if self.value >= 1023 or self.value < 0:
            self.increment *= -1
        self.value += self.increment
        return self.value


class LogiTechController(object):
    LTHUMB_X = 1
    RTHUMB_X = 3
    LTHUMB_Y = 0
    RTHUMB_Y = 2
    BUTTON_LEFT = 0
    BUTTON_RIGHT = 2
    BUTTON_UP = 3
    BUTTON_DOWN = 1


class PiranhaController(object):
    LTHUMB_X = 1
    RTHUMB_X = 3
    LTHUMB_Y = 0
    RTHUMB_Y = 2


class MegaController(object):
    JOY_X = 0
    JOY_Y = 1
    THROTTLE_Y = 2
    THROTTLE_X = 3
    F1 = 0
    F2 = 1
    F3 = 2
    F4 = 3
    F5 = 4
    F6 = 5
    F7 = 6
    F8 = 7


class XboxController(object):
    LEFT_TRIGGER = 3
    RIGHT_TRIGGER = 5
    LEFT_AXIS_X = 0
    LEFT_AXIS_Y = 1
    RIGHT_AXIS_X = 2
    RIGHT_AXIS_Y = 4

    A_BUTTON = 0
    B_BUTTON = 1
    X_BUTTON = 2
    Y_BUTTON = 3
    LEFT_DPAD = 11
    RIGHT_DPAD = 12
    UP_DPAD = 13
    DOWN_DPAD = 14
    START = 7
    SELECT = 6
    LB = 4
    RB = 5
    LOGO_BUTTON = 8
    LEFT_AXIS_BUTTON = 9
    RIGHT_AXIS_BUTTON = 10


class PongTtyController(object):
    LTHUMB_X = 1
    RTHUMB_X = 0
    LTHUMB_Y = 1
    RTHUMB_Y = 0


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
                print(key)
                chan, button = key
                while(mc.getInputed()[key] == 0):
                    value = mc.getButton(chan, button)
                print(value)
        # for x in range(0, 16):
        #     for y in range(0, 4):
        #         value = mc.getButton(x, y)
        #         while(value == 0):
        #             value = mc.getButton(x, y)
        #         print((x, y), value)
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


class ttyController(object):
    ser_port = None
    serial = __import__('serial')
    def __init__(self, plugged=0):
        self.pos = (0, 0)
        self.args = get_args()
        port = "/dev/tty" + self.args.ttyport
        baud = self.args.ttybaud
        self.debug = self.args.ttydebug
        if not self.ser_port:
            self.ser_port = self.serial.Serial(port, baud, interCharTimeout=0.009)

    def getPos(self, button):
        try:
            # ask for next two bytes.
            for i in xrange(0, 10):
                self.ser_port.write('n')
            # look if anything in buffer.
            # if so extract values and return.
            if(self.ser_port.inWaiting()):
                for i in xrange(0, 9):
                    self.ser_port.read(2)
                first, second = self.ser_port.read(2)
                # get values.
                first, second = ord(first), ord(second)
                if self.debug:
                    print(first, second)
                self.pos = (first, second)
            return self.pos[button]
        except Exception as e:
            print("sys.exit: " + str(e))
            raise KeyboardInterrupt

    def __del__(self):
        if self.ser_port:
            print("closing serial port")
            self.ser_port.close()
