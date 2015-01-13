from Graphics import *
import time
from math import sin, cos, sqrt, pi

class PlasmaSecond(object):
	def __init__(self, speed=0.8):
		self.graphics = Graphics(matrix_width, matrix_height)
		self.plasma = Graphics(matrix_width, matrix_height)

		self.x_range = xrange(0, matrix_width, 1)
		self.y_range = xrange(0, matrix_height, 1)

		self.interval = .1/speed
		self.time = 0
		self.previousTick = 0

		self.generatePalette()
		self.generatePlasmaSurface()
	def generatePalette(self):
		self.palette = []
		for x in xrange(0, (2**8), 1):
			r =  10#int(128.0 +128*sin(pi*x/128.0))
			g = int(128.0 +128*sin(pi*x/64.0))
			b = int(128.0 +128*sin(pi*x/16.0))
			if r < 10: r = 10
			if g < 10: g = 10
			if b < 10: b = 10
			colorRGB = (r,g,b)
			self.palette.append(colorRGB)
	def generatePlasmaSurface(self):
		x_offset = self.time+int(self.time*(matrix_width/matrix_height))
		y_offset = self.time+int(self.time*(matrix_height/matrix_width))
		for y in self.y_range:
			for x in self.x_range:
				c = int(
					 128+(128*sin((x+x_offset)/2.0))
					+128+(128*sin((y+y_offset)/2.0))
					+128+(128*sin(((x+x_offset)+(y+y_offset))/4.0))
					+128+(128*sin(sqrt(float((x+x_offset)*(x+x_offset)+(y+y_offset)*(y+y_offset)))/2.0))
					)/4
				color = (c,)*3
				self.plasma.drawPixel(x,y,color)
		return list(self.plasma.getSurface())
	def process(self):
		if((time.time()-self.previousTick) >= self.interval):
			self.previousTick = time.time()
			self.time+=1
		paletteShift = self.time
		self.generatePlasmaSurface()
		for y in self.y_range:
			for x in self.x_range:
				plasma_color = self.plasma.readPixel(x,y)
				color_shift = self.palette[paletteShift%256]
				r = (plasma_color[0]+color_shift[0])%256
				g = (plasma_color[1]+color_shift[1])%256
				b = (plasma_color[2]+color_shift[2])%256
				color = (r,g,b,)
				self.graphics.drawPixel(x,y, color)
	def draw(self):
		pass
	def generate(self):
		self.graphics.fill(BLACK)
		self.process()
		self.draw()
		return self.graphics.getSurface()

class PlasmaFirst(object):
	def __init__(self, speed=20):
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
					128.0 + (128.0*sin((x+6)/2.4))
					+128.0 + (128.0*cos(y/3.4))
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
				color = ColorRGBOps.darken(color, 50)
				self.graphics.drawPixel(x,y, color)
	def draw(self):
		pass
	def generate(self):
		self.graphics.fill(BLACK)
		self.process()
		self.draw()
		return self.graphics.getSurface()