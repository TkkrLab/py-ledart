from Ledart.stripinfo import strip_width, strip_height
from Ledart.Tools.Graphics import Graphics, BLUE


class FillTest(Graphics):
    def __init__(self):
        Graphics.__init__(self, width=strip_width, height=strip_height)
        self.color = BLUE
        # self.draw_pixel(10, 10, self.color)
        self.fill(self.color)

    def generate(self):
        pass
