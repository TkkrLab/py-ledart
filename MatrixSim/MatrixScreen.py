import time
import sys

from Pixel import Pixel

from Tools.Graphics import BLUE, BLACK

# setup interface options, if no interface possible
# set to a dummy
from Interfaces.DummyInterface import DummyInterface
interface_opts = {
    "dummy": DummyInterface
}

# set an option for a pygame interface
try:
    from Interfaces.PygameInterface import PygameInterface
    interface_opts["pygame"] = PygameInterface
except Exception as e:
    print("module not installed, %s" % str(e))
    interface_opts["pygame"] = DummyInterface

# set an option for a opengl interface
try:
    from Interfaces.OpenGlInterface import OpenGlInterface
    interface_opts["opengl"] = OpenGlInterface
except Exception as e:
    print("Module not installed, %s" % str(e))
    interface_opts["opengl"] = DummyInterface


class MatrixScreen(object):
    """
    this module/class is a matrix simulator (led)
    it draws blocks in a array the size of the pixels is
    defined in matrix.py
    """
    def __init__(self, width, height, pixelsize, fullscreen=False,
                 interface=DummyInterface):
        self.interface = interface(width, height, pixelsize, fullscreen)
        self.width = width
        self.height = height
        self.pixelSize = pixelsize

        self.pixels = []

        self.window_width = width * pixelsize
        self.window_height = height * pixelsize

        self.interface.setcaption("artnet matrix simulator.")

        widthrange = range(0, self.window_width, pixelsize)
        # reverse order because else the display is flipped.
        heightrange = range(0, self.window_height, pixelsize)

        # create pixels.
        for y in heightrange:
            for x in widthrange:
                pos = (x, y)
                color = BLUE
                pixel = Pixel(pos, pixelsize, color)
                self.pixels.append(pixel)

        self.interface.setcaption("Matrix Simulator.")

    def get_pixels(self):
        """
        returns the internal list representation of the pixels
        """
        return self.pixels

    def handleinput(self):
        self.interface.handleinput()

    def draw(self, data):
        self.interface.clear(BLACK)
        # get the indexes of every pixel
        indexes = data.indexes
        # itterate of the colors of every pixel.
        for i, index in enumerate(indexes):
            # take the color
            color = data[index]
            # skip drawing if it's a drawing a black pixel on a black surface.
            if color == BLACK:
                continue

            # calculate position based on index, pixelsize, and data offset.
            x, y = index
            x, y = x * self.pixelSize, y * self.pixelSize
            xo, yo = data.get_d_offset()
            xo, yo = xo * self.pixelSize, yo * self.pixelSize
            x, y = x + xo, y + yo
            # create a rect based on calculated positions.
            width, height = self.pixelSize, self.pixelSize
            rect = (x, y, width, height)
            # draw the actual block
            self.interface.drawblock(rect, color)

    def process(self, data):
        self.draw(data)
        # update the screen so our data is shown.
        self.interface.update()

    def printfps(self):
        sys.stdout.write("%s      \r" % self.fps)

    def __del__(self):
        self.interface.quit()
