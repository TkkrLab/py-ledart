class Interface(object):
    """
    the basic drawing interface api
    """
    def __init__(self, width, height, blocksize, fullscreen=False):
        """ Initialize the interface. it know how big the screen is."""
        # due to physical matrix layout these are switched.
        self.width = width * blocksize
        self.height = height * blocksize
        self.blocksize = blocksize
        self.fullscreen = fullscreen

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

    def drawblock(self, rect, color, bordercolor=None, borderwidth=None):
        """ draws the blocks that are the pixels."""
        pass

    def update(self):
        """ updates the interface window. """
        pass

    def quit(self):
        """ called when quiting the program."""
        pass
