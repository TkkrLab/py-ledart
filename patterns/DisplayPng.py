from Tools.Graphics import Graphics, RED
from Tools.Graphics import ImageSurface
from matrix import matrix_width, matrix_height


class DisplayImage(ImageSurface):
    def __init__(self, fname='images/sisters-sprites.png'):
        ImageSurface.__init__(self, matrix_width, matrix_height, fname,
                              thumbnail_it=True)

    def generate(self):
        pass


class RectTest(Graphics):
    def __init__(self):
        Graphics.__init__(self, 10, 10)
        self.set_d_offset((56 - 10, 32 - 10))
        self.fill(RED)

    def generate(self):
        pass
