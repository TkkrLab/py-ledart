from Graphics.Graphics import *
from matrix import *

class PixelBros(object):
	def __init__(self):
		self.graphics = Graphics(matrix_width, matrix_height)
	def generate(self):
		return self.graphics.getSurface()