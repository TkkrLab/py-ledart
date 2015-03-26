import sys

try:
    from PygameController import PygameController, PygameDummyController
except Exception as e:
    print("pygamecontroller>> " + str(e))


def translate(value, leftmin, leftmax, rightmin, rightmax):
    leftspan = leftmax - leftmin
    rightspan = rightmax - rightmin
    valuescaled = float(value - leftmin) / float(leftspan)
    return rightmin + (valuescaled * rightspan)


class ControllerError(BaseException):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class DummyController(object):
    def __init__(self, plugged=0):
        self.value = 0
        self.increment = 50

    def getValue(self):
        if self.value >= 1023 or self.value < 0:
            self.increment *= -1
        self.value += self.increment
        return self.value


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
    POT1 = 0
    POT2 = 1


class AudioController(object):
    """
    controller that is connected to sound input (microphone)
    """
    def __init__(self, channel=1, rate=8000, period=160):
        import alsaaudio
        self.audio = alsaaudio
        import time
        self.time = time
        import audioop
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

    def __init__(self, plugged=0, baud=115200, port="ACM", debug=False):
        import serial
        self.serial = serial
        self.pos = (0, 0)
        port = "/dev/tty" + port + str(plugged)
        if not self.ser_port:
            self.ser_port = self.serial.Serial(port, baud,
                                               interCharTimeout=0.009)
        self.debug = debug

    def getPos(self, button):
        try:
            # ask for next two bytes.
            self.ser_port.write('n')
            # look if anything in buffer.
            # if so extract values and return.
            if(self.ser_port.inWaiting()):
                first, second = self.ser_port.read(2)
                # get values.
                first, second = ord(first), ord(second)
                self.pos = (first, second)
            if self.debug:
                print(first, second)
            return self.pos[button]
        except Exception as e:
            print("sys.exit: " + str(e))
            sys.exit(0)

    def __del__(self):
        if self.ser_port:
            print("closing serial port")
            self.ser_port.close()
