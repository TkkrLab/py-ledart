from Ledart.matrix import matrix_width, matrix_height
from Ledart.Tools.Graphics import Graphics, BLUE


class FillTest(Graphics):
    def __init__(self):
        Graphics.__init__(self, width=matrix_width, height=matrix_height)
        self.color = BLUE
        # self.draw_pixel(10, 10, self.color)
        self.fill(self.color)

    def generate(self):
        pass
