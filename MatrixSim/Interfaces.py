import sys


class Interface(object):
    """
    the basic drawing interface api
    """
    def __init__(self, width, height, blocksize):
        """ Initialize the interface. it know how big the screen is."""
        # due to physical matrix layout these are switched.
        self.width = height * blocksize
        self.height = width * blocksize

    def handleinput(self):
        """
        this function handles the inputs. basic q/esc for quit or
        ctrl-z for quiting. and checking mouse focus.
        """
        pass

    def setcaption(self, caption):
        """ sets the title/caption of the window for the simulator."""
        pass

    def fill(self, color):
        """ fills the window with a color."""
        pass

    def drawblock(self, rect, color, bordercolor, borderwidth=1):
        """ draws the blocks that are the pixels."""
        pass

    def update(self):
        """ updates the interface window. """
        pass

    def quit(self):
        """ called when quiting the program."""
        pass


from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


class OpenGlInterface(Interface):
    def __init__(self, width, height, pixelsize, fullscreen):
        Interface.__init__(self, width, height, pixelsize)
        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
        glutInitWindowSize(self.width, self.height)
        glutInitWindowPosition(self.width, self.height)
        self.window = glutCreateWindow("matrix Sim")
        glutMainLoopEvent()



class PygameInterface(Interface):
    """
    a abstract drawing interface that uses pygame.
    """
    def __init__(self, width, height, blocksize, fullscreen=False):
        Interface.__init__(self, width, height, blocksize)
        import pygame
        self.pygame = pygame
        self.flags = pygame.DOUBLEBUF | self.pygame.HWSURFACE
        if fullscreen:
            self.flags |= self.pygame.FULLSCREEN
        self.window = self.pygame.display.set_mode((self.width, self.height),
                                                   self.flags)

    def handleinput(self):
        for event in self.pygame.event.get():
            if event.type == self.pygame.QUIT:
                raise SystemExit
            if event.type == self.pygame.KEYDOWN:
                # quit on ctrl-c as if it were in the terminal.
                # to lazy to press x.
                lctrlpressed = (self.pygame.key.get_mods() &
                                self.pygame.KMDED_LCTRL)
                if event.key == self.pygame.K_c and lctrlpressed:
                    raise KeyboardInterrupt
                if event.key == self.pygame.K_q or self.pygame.K_ESCAPE:
                    raise KeyboardInterrupt

            # check if the mouse pointer is on/in the window.
            # and if so hide it.
            focused = self.pygame.mouse.get_focused()
            self.pygame.mouse.set_visible(not focused)

    def setcaption(self, caption):
        self.pygame.display.set_caption(caption)

    def fill(self, color):
        self.window.fill(color)

    def drawblock(self, rect, color, bordercolor, borderwidth=1):
        self.pygame.draw.rect(self.window, color, rect)
        # draw a nice little square around so it looks more like a pixel.
        self.pygame.draw.rect(self.window, bordercolor, rect, borderwidth)

    def update(self):
        self.pygame.display.update()

    def quit(self):
        self.pygame.quit()
