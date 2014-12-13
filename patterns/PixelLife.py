from Graphics import *
from Life.life import Life

class MatrixLifeBk(object):
	def __init__(self):
		self.graphics= Grahpics(matrix_width, matrix_height)
	def generate(self):
		pass
class MatrixLife(object):
	def __init__(self):
		self.life = Life(matrix_width, matrix_height, 1, color=BLUE)
		self.graphics = Graphics(matrix_width, matrix_height)
	def draw(self):
		for index,cel in enumerate(self.life.buffer):
			if cel:
				self.graphics.surface[index] = BLUE
			else:
				self.graphics.surface[index] = BLACK
	def generate(self):
		self.life.process()
		self.draw()
		return self.graphics.getSurface()
