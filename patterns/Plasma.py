from Graphics import *
import time
from math import sin, cos, sqrt


class PlasmaFirst(object):
	def __init__(self, speed=10):
		self.graphics = Graphics(matrix_width, matrix_height)
		self.plasma = Graphics(matrix_width, matrix_height)
		
		self.x_range = xrange(0, matrix_width, 1)
		self.y_range = xrange(0, matrix_height, 1)

		self.interval = .1/speed #interval/speed is how many ticks a second.
		self.time = 0
		self.previousTick = 0

		self.generatePalette()
		self.generatePlasmaSurface()
	def generatePalette(self):
		self.palette = []
		for x in xrange(0, 256, 1):
			colorRGB = HSVtoRGB((x,255,255,))
			self.palette.append(colorRGB)
	def generatePlasmaSurface(self):
		for y in self.y_range:
			for x in self.x_range:
				#c = int(abs(256*sin((x+y+self.time)/3.0)))
				c = int(
					128.0 + (128.0*sin(x/2.0))
					+128.0 + (128.0*sin(y/3.5))
					)/2
				color = (c,)*3
				self.plasma.drawPixel(x,y,color)
		return list(self.plasma.getSurface())
	def process(self):
		if( (time.time()-self.previousTick) >= self.interval ):
			self.previousTick = time.time()
			self.time += 1
		paletteShift = self.time
		for y in self.y_range:
			for x in self.x_range:
				plasma_color = self.plasma.readPixel(x,y)
				color_shift = self.palette[paletteShift%256]
				r = (plasma_color[0]+color_shift[0])%256
				g = (plasma_color[1]+color_shift[1])%256
				b = (plasma_color[2]+color_shift[2])%256
				color = (r,g,b,)
				print color
				self.graphics.drawPixel(x,y, color)
	def draw(self):
		pass
	def generate(self):
		self.graphics.fill(GREEN)
		self.process()
		self.draw()
		return self.graphics.getSurface()