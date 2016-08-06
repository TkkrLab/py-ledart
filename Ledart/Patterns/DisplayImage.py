from Tools.Graphics import ImageSurface
from matrix import matrix_width, matrix_height


class DisplayImage(ImageSurface):
    def __init__(self, fname='images/tkkrlab.png'):
        ImageSurface.__init__(self, matrix_width, matrix_height, fname)

    def generate(self):
        pass
