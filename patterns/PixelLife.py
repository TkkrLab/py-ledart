from Graphics import *
from Life.life import Life
import random

class MatrixLife(object):
	def __init__(self):
		self.life = Life(matrix_width, matrix_height, 1, color=BLUE)
		self.graphics = Graphics(matrix_width, matrix_height)
		self.color = BLACK
	"""
	this draw function manipulates the graphics surface directly.
	it's either elegent in one way.
	and really really ugly in another way.
	"""
	def pickRandomColor(self):
		color = random.randint(0,len(COLORS)-1)
		#make sure that that color isn't black
		while(COLORS[color] == BLACK):
			color = random.randint(0, len(COLORS)-1)
		self.color = COLORS[color]
	def draw(self):
		for index,cel in enumerate(self.life.field):
			if cel:
				self.pickRandomColor()
				#give every lifing cell a random color
				self.graphics.surface[index] = self.color
				#self.graphics.surface[index] = BLUE
			else:
				self.graphics.surface[index] = BLACK
	def generate(self):
		self.life.process()
		self.draw()
		return self.graphics.getSurface()
