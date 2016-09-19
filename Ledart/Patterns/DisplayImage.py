from Ledart.Tools.Graphics import ImageSurface
from Ledart.stripinfo import strip_width, strip_height


class DisplayImage(ImageSurface):
    def __init__(self, fname=None):
        if fname:
            ImageSurface.__init__(self, strip_width, strip_height, fname)

    def generate(self):
        pass
