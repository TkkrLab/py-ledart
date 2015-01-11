from matrix import *
import random
#raindrop by Duality
class RainDrop(object):
	#color indexing in fridgefire's matrix is G B R
	def __init__(self, color=(100,255,100)):
		self.color = color
		self.y = 0
		self.x = random.randint(0, matrix_width)
		self.pos = (self.x, self.y)
		self.height = self.y
	def getPos(self):
		return self.pos
	def setHeight(self):
		self.height = height
	def getHeight(self):
		return self.height
	def incrementHeight(self):
		self.height+=1
		self.y = self.height

#rain pattern implementation by Duality
#will call 2.0 :D
class RainPattern(object):
	def __init__(self, color=(80,255,100), chance=0.04):
		self.color = color
		self.chance = chance
		self.data = [(0,0,0)]*matrix_size
		#insert single drop for testing
		self.drops = [RainDrop(color)]
	def generate(self):
		#clear data
		self.data = [(0,0,0)]*matrix_size
		#put drop in data and increment it's position
		for drop in self.drops:
			#calculate where to put it
			index = ((drop.y-1)*matrix_width+drop.x)-1
			#put drop op matrix screen
			if index >= 0:
				self.data[index] = drop.color
			#increment it's height
			drop.incrementHeight()
			#if it falls of the screen remove it.
			if drop.getHeight() > matrix_height:
				self.drops.remove(drop)
		#add a random chance for drops to appear.
		if(random.random() < self.chance):
			raindrop = RainDrop(self.color)
			self.drops.append(raindrop)
		return self.data

class RainPattern_original:
	# Falling drops, default color white/blue-ish
	def __init__(self, color=(100,255,100), chance=0.04):
		# Init empty data list
		self.color = color
		self.chance = chance
		self.data = []
		for i in xrange(matrix_size):
			self.data.insert(0, (0, 0, 0))  # black/off
	def generate(self):
		# Pop 7 times to move one line down
		for i in xrange(matrix_width):
			self.data.pop()
			if (random.random() < self.chance):  # random chance of raindrop
				self.data.insert(0, self.color)
			else:
				self.data.insert(0, (0, 0, 0))  # black/off
		return self.data
