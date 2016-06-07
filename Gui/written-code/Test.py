from Tools.Graphics import Graphics
from matrix import matrix_width, matrix_height

selected = 'Test'

class Test(Graphics):
    def __init__(self):
        Graphics.__init__(self, matrix_width, matrix_height)
        self.fill((255, 255, 255))
    
    def generate(self):
        pass