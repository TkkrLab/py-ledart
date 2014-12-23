class MegaController(object):
    import pygame
    def __init__(self, axis=0):
        self.pygame.init()
        self.axis = axis
        self.joystick = self.pygame.joystick.Joystick(0)
        self.joystick.init()
    def translate(self, value, leftmin, leftmax, rightmin, rightmax):
        leftspan = leftmax - leftmin
        rightspan = rightmax - rightmin
        valuescaled = float(value-leftmin)/float(leftspan)
        return rightmin+(valuescaled*rightspan)
    def getPos(self):
        for event in self.pygame.event.get():
            pass
        axis = self.joystick.get_axis(self.axis)
        value = int(self.translate(axis, -1., 1., 0, 10.1))
        if value:
            value = abs(value)
        return value
    def __del__(self):
        self.pygame.quit()

class Controller(object):
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

