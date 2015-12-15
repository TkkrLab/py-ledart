from Tools.Graphics import Graphics, RED
from Tools.Graphics import ImageSurface
from matrix import matrix_width, matrix_height


class DisplayImage(ImageSurface):
    def __init__(self, fname='images/sisters-sprites.png'):
        ImageSurface.__init__(self, matrix_width, matrix_height, fname)

    def generate(self):
        pass


class RectTest(Graphics):
    def __init__(self):
        Graphics.__init__(self, matrix_width, matrix_height)
        self.draw_pixel(0, 0, RED)
        self.draw_pixel(1, 0, RED)

    def generate(self):
        pass
