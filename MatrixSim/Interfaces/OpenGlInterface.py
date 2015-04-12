from Interface import Interface
from OpenGL.GL import *
from OpenGL.GLUT import *


class OpenGlInterface(Interface):
    def __init__(self, width, height, pixelsize, fullscreen):
        Interface.__init__(self, width, height, pixelsize)
        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
        glutInitWindowSize(self.width, self.height)
        glutInitWindowPosition(self.width, self.height)
        self.window = glutCreateWindow("matrix Sim")
        glutKeyboardFunc(self.keyboardinput)
        if fullscreen:
            glutFullScreen()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0.0, self.width, 0.0, self.height, 0.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glutMainLoopEvent()

    def keyboardinput(self, *args):
        """ special way of input handling."""
        ctrl_c = '\x1b'
        if(args[0] == 'q' or args[0] == ctrl_c):
            raise SystemExit
        if(args[0] == '\x03'):
            raise SystemExit

    def setcaption(self, caption):
        glutSetWindowTitle(caption + " (opengl)")

    def clear(self, color):
        self.draw_rect((0, 0, self.width, self.height), color)

    def draw_rect(self, rect, color):
        r, g, b = color
        r /= float(0xff)
        g /= float(0xff)
        b /= float(0xff)
        x, y, width, height = rect
        # the y direction is flipped but this fixes it :)
        y = self.height - y - height

        glColor3f(r, g, b)
        glBegin(GL_QUADS)
        glVertex2f(x, y)
        glVertex2f(x + width, y)
        glVertex2f(x + width, y + height)
        glVertex2f(x, y + height)
        glEnd()

    def drawblock(self, rect, color, bordercolor, borderwidth=1):
        self.draw_rect(rect, bordercolor)
        x, y, width, height = rect
        rect = (x + borderwidth, y + borderwidth,
                width - borderwidth, height - borderwidth)
        self.draw_rect(rect, color)

    def update(self):
        glutSwapBuffers()
        glutMainLoopEvent()
