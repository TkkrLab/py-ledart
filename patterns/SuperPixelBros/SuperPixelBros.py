from Graphics import *
from Controllers import *
from time import time

c = BLACK
r = RED
g = GREEN
b = BLUE

level1 = [
			c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,
			c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,
			c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,
			c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,
			c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,c,
			g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,
			g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,
			g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,
			g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,
			g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,
		]

level = [BLUE]*matrix_size

def shift(l, n):
	return l[n:]+l[:n]

def to_matrix(l, n):
	return [l[i:i+n] for i in xrange(0, len(l), n)]


"""Tile class holds info on individual Tiles"""
class TilePixel(object):
	def __init__(self, pos, color, graphics):
		self.pos = pos[1],pos[0]
		self.color = color
		self.graphics = graphics
	def draw(self):
		x,y = self.pos
		self.graphics.drawPixel(x,y, self.color)

"""Player class handles how to player acts."""
class Player(TilePixel):
	def __init__(self, pos, color, graphics, game):
		TilePixel.__init__(self, pos, color, graphics)
		self.game = game
	def handleInput(self):
		pass
	def process(self):
		pass

"""
SuperPixelBros is a class that hanles function calling and processing.
makes sure the level is generated.
makes sure the player get the right data.

note for the way the matrix is hung on poles (rotated 90 anticlockwise)
we want to make our x the actuall y 
and vice versa.
but the Tile class takes care of that.

we also need to swap the matrix_width with matrix_height we want to use it.
the Graphics object it's self needs the correct way around though.
for actuall pixel position calculations.

screen_height and screen_width take care of swaping them.

"""
class SuperPixelBros(object):
	def __init__(self):
		#need the actuall width and height. or else the pixel calculations go wrong.
		self.graphics = Graphics(matrix_width, matrix_height)

		# screen_width-1 because counting starts at 0
		self.player = Player((14,5), BLUE, self.graphics, self)

		self.map = []

	def handleInput(self):
		pass
	def process(self):
		pass
	def draw(self):
		self.graphics.fill(BLACK)
		#draw the map.
		for tile in self.map:
			tile.draw()
		#draw the player.
		self.player.draw()
	def generate(self):
		self.handleInput()
		self.process()
		self.draw()
		return self.graphics.getSurface()