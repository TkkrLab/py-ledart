from Graphics import *
from matrix import *
import random

#still a work in progress. not really done yet.

#falling stars by Duality
class Star(object):
	def __init__(self, color=BLUE):
		self.colorMax = 255
		self.color = color
		self.y = 0
		self.x = random.randint(0, matrix_width)
		self.pos = (self.x,self.y)
		self.height = self.y
		self.stream = []
	def getPos(self):
		return self.pos
	def setHeight(self, height):
		self.height = height
	def getHeight(self):
		return self.height
	def incrementHeight(self):
		self.height += 1
		self.y = self.height

def FallingStar(object):
	def __init__(self, color=BLACK, chance=0.2):
		self.color = color
		self.chance = chance
		self.graphics = Graphics(matrix_width, matrix_height)
	def process(self):
		self.data = [BLACK]*matrix_size
	def draw(self):
		pass
	def generate(self):
		self.process()
		self.draw()
		return self.graphics.getSurface()
