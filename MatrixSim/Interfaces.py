from OpenGL.GL import *
from OpenGL.GLUT import *

import pygtk
pygtk.require('2.0')
import gtk


class Interface(object):
    """
    the basic drawing interface api
    """
    def __init__(self, width, height, blocksize):
        """ Initialize the interface. it know how big the screen is."""
        # due to physical matrix layout these are switched.
        self.width = height * blocksize
        self.height = width * blocksize
        self.blocksize = blocksize

    def handleinput(self):
        """
        this function handles the inputs. basic q/esc for quit or
        ctrl-z for quiting. and checking mouse focus.
        """
        pass

    def setcaption(self, caption):
        """ sets the title/caption of the window for the simulator."""
        pass

    def clear(self, color):
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


class GtkInterface(Interface):
    def __init__(self, width, height, pixelsize, fullscreen):
        Interface.__init__(self, width, height, pixelsize)
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.resize(self.width, self.height)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.set_title("testy")
        self.window.connect("destroy", self.exit)
        self.window.connect("key_press_event", self.keyboardinput)
        self.window.set_events(gtk.gdk.KEY_PRESS_MASK)

        self.darea = gtk.DrawingArea()
        self.window.add(self.darea)

        self.darea.show()
        self.window.show()
        self.cr = self.darea.window.cairo_create()

    def expose(self, widget, event):
        print(widget == self.darea)

    def colorconvertf(self, color, depth=8):
        temp = []
        for c in color:
            if c:
                temp.append((2 ** depth) / c)
            else:
                temp.append(c)
        return tuple(temp)

    def draw_rect(self, rect, color):
        r, g, b = self.colorconvertf(color)
        x, y, width, height = rect

        self.cr.set_source_rgb(r, g, b)
        self.cr.rectangle(x, y, width, height)
        self.cr.fill()

    def drawblock(self, rect, color, bordercolor, borderwidth=1):
        self.draw_rect(rect, bordercolor)
        x, y, width, height = rect
        rect = (x + borderwidth, y + borderwidth,
                width - borderwidth, height - borderwidth)
        self.draw_rect(rect, color)

    def clear(self, color):
        self.draw_rect((0, 0, self.width, self.height), color)

    def update(self):
        self.handle_events()

    def setcaption(self, caption):
        self.window.set_title(caption + " (gtk)")

    def handle_events(self):
        if gtk.events_pending():
            gtk.main_iteration()

    def keyboardinput(self, widget, data=None):
        if data.keyval == ord('q') or data.keyval == 65307:
            raise SystemExit
        else:
            print(data.keyval)

    def exit(self, widget):
        raise SystemExit


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
        if(args[0] == 'q' or args[0] == '\x1b'):
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
        self.pygame.display.set_caption(caption + " (pygame)")

    def clear(self, color):
        self.window.fill(color)

    def drawblock(self, rect, color, bordercolor, borderwidth=1):
        self.pygame.draw.rect(self.window, color, rect)
        # draw a nice little square around so it looks more like a pixel.
        self.pygame.draw.rect(self.window, bordercolor, rect, borderwidth)

    def update(self):
        self.pygame.display.update()

    def quit(self):
        self.pygame.quit()
