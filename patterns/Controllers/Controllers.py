import sys
def translate(value, leftmin, leftmax, rightmin, rightmax):
    leftspan = leftmax - leftmin
    rightspan = rightmax - rightmin
    valuescaled = float(value-leftmin)/float(leftspan)
    return rightmin+(valuescaled*rightspan)

class ControllerError(BaseException):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class PygameController(object):
    import pygame
    #axis for which axis to read (button)
    #plugged for which controller to select
    def __init__(self, plugged=0):
        self.pygame.init()
        self.joystick = self.pygame.joystick.Joystick(plugged)
        self.joystick.init()

        self.num_axis = self.joystick.get_numaxes()
        self.num_buttons = self.joystick.get_numbuttons()
        self.num_hats = self.joystick.get_numhats()
    def handleEvents(self):
        self.pygame.event.pump()
        for event in self.pygame.event.get():
            if event.type == self.pygame.QUIT:
                sys.exit(0)
    def getAxis(self, button):
        self.handleEvents()
        if self.num_axis:
            return self.joystick.get_axis(button)
        else:
            raise ControllerError("No Axis")
    def getButtons(self, button):
        self.handleEvents()
        if self.num_buttons:
            return self.joystick.get_button(button)
        else:
            raise ControllerError("No Buttons")

    def getHats(self, button):
        self.handleEvents()
        if self.num_hats:
            return self.joystick.get_hat(button)
        else:
            raise ControllerError("No Hats")
    def __del__(self):
        self.pygame.quit()

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
    LEFT_TRIGGER = 4
    RIGHT_TRIGGER = 5
    LEFT_AXIS_X = 0
    LEFT_AXIS_Y = 1
    RIGHT_AXIS_X = 2
    RIGHT_AXIS_Y = 3

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



class TtyController(object):
    ser_port = None
    def __init__(self, port = "/dev/ttyACM0", baud=9600):
        if not self.ser_port:
            self.ser_port = serial.Serial(port, baud)
    def getPos(self):
        try:
            self.ser_port.flushInput()
            pos = ord(self.ser_port.read())
            return pos
        except Exception, e:
            print "sys.exit: "+str(e)
            sys.exit(0)
    def __del__(self):
        if self.ser_port:
            self.ser_port.close()

