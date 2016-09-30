from Ledart.Tools.Graphics import Graphics, BLUE


class FillTest(Graphics):
    def __init__(self, **kwargs):
        Graphics.__init__(self, **kwargs)
        self.color = BLUE
        self.fill(self.color)

    def generate(self):
        pass
