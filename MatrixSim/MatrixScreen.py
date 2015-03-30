import time

# first things first make sure we are able to find the necesary files we need.
# wd = os.path.join(os.path.dirname(__file__), os.path.pardir)
# sys.path.append(wd)
# sys.path.append(wd + "/patterns/Graphics/")

from Pixel import Pixel
import Graphics.Graphics as Graphics
import matrix


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


class GtkInterface(Interface):
    """
    abstract darwing interface that uses gtk.
    """
    def __init__(self, width, height, blocksize, fullscreen=False):
        Interface.__init__(self, width, height, blocksize)


class PygameInterface(Interface):
    """
    a abstract drawing interface that uses pygame.
    """
    def __init__(self, width, height, blocksize, fullscreen=False):
        Interface.__init__(self, width, height, blocksize)
        import pygame
        self.pygame = pygame
        self.flags = self.pygame.DOUBLEBUF | self.pygame.HWSURFACE
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


class MatrixScreen(object):
    """
    this module/class is a matrix simulator (led)
    it draws blocks in a array the size of the pixels is
    defined in matrix.py
    """
    def __init__(self, width, height, pixelsize, fullscreen=False,
                 interface=PygameInterface):
        self.interface = interface(width, height, pixelsize, fullscreen)
        self.width = width
        self.height = height
        self.pixelSize = pixelsize

        self.pixels = []

        self.window_width = height * pixelsize
        self.window_height = width * pixelsize

        self.interface.setcaption("pygame artnet matrix simulator.")

        widthrange = range(0, self.window_width, pixelsize)
        # reverse order because else the display is flipped.
        heightrange = range(0, self.window_height, pixelsize)[::-1]

        # due to how the ledmatrix is displayed x, y are filled as is the
        # window_width/height thing a bit above here.
        for x in widthrange:
            for y in heightrange:
                pos = (x, y)
                color = Graphics.BLUE
                pixel = Pixel(pos, pixelsize, color)
                self.pixels.append(pixel)

        # for keeping fps
        self.previous = 1
        self.time = 1
        self.fps = 0

    def handleinput(self):
        self.interface.handleinput()

    def draw(self, data):
        # extract pixels and color from data
        # get both a list index and the color data.
        for i, color in enumerate(data):
            self.pixels[i].setColor(color)

        # clear the pygame window
        self.interface.fill(Graphics.BLACK)

        # display the pixels.
        for pixel in self.pixels:
            r = pixel.color[matrix.COLOR_ORDER[0]]
            g = pixel.color[matrix.COLOR_ORDER[1]]
            b = pixel.color[matrix.COLOR_ORDER[2]]
            color = (r, g, b)
            # for a nice litle border that makes the pixels stand out.
            bordercolor = Graphics.BLACK
            self.interface.drawblock(pixel.getRect(), color, bordercolor)

        # update the screen so our data show.
        self.interface.update()

    def process(self, data):
        self.time = time.time()
        self.fps = 1. / (self.time - self.previous)
        self.previous = self.time
        self.interface.setcaption("artnet matrix sim FPS:" +
                                  str(int(self.fps)))
        self.handleinput()
        self.draw(data)

    def __del__(self):
        self.interface.quit()
