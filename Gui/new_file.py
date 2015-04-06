from Graphics.Graphics import Graphics
from matrix import *
from Timing import *

class Pattern(object):
    def __init__(self):
        self.pos = ()
        self.graphics = Graphics(matrix_width, matrix_height)