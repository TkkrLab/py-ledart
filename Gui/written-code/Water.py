from Tools.Graphics import Surface
from Tools.Graphics import BLUE, RED
from matrix import matrix_width, matrix_height

class Water(Surface):
    def __init__(self):
        Surface.__init__(self, width=matrix_width, height=matrix_height)
        for point in self.get_points():
            self[point] = BLUE
    
    def generate(self):
        for point in self.get_points():
            self[point] = RED