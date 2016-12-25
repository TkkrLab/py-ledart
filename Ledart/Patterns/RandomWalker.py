from Ledart import Graphics, BLACK, GREEN
from Ledart import Vector
from colorsys import hsv_to_rgb

import random

class Walker(object):
	def __init__(self, g, x, y, stepsize=4):
		self.pos = Vector(x=x, y=y)
		self.stepsize = stepsize
		self.numsteps = 1
		self.g = g
		self.previous = 0

	def walk(self):
		self.xdir = random.randint(-1, 1) * self.stepsize
		self.ydir = random.randint(-1, 1) * self.stepsize
		self.previous = Vector(x=self.pos.x, y=self.pos.y)
		self.pos += Vector(x=self.xdir, y=self.ydir)
		self.handle_collision()

		self.color = [min(int(0xff * c), 0xff) for c in hsv_to_rgb(self.numsteps / float(0xfff), 1, 1)]
		self.numsteps += 1

	def handle_collision(self):
		if self.pos.x - self.stepsize < 0:
			self.pos.x = 0
		if self.pos.x > self.g.width - self.stepsize:
			self.pos.x = self.g.width
		if self.pos.y - self.stepsize < 0:
			self.pos.y = 0
		if self.pos.y > self.g.height - self.stepsize:
			self.pos.y = self.g.height

	def draw(self):
		self.g.draw_line(self.pos.x, self.pos.y, self.previous.x, self.previous.y, self.color)

class RandomWalker(Graphics):
	def __init__(self, **kwargs):
		Graphics.__init__(self, **kwargs)
		self.walker = Walker(self, self.width/2, self.height/2)

	def generate(self):
		# self.fill(BLACK)
		self.walker.walk()
		self.walker.draw()