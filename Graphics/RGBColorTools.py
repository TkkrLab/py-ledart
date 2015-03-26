class ColorRGB(object):
	def __init__(self, r, g, b):
		self.r = r
		self.g = g
		self.b = b
		self.color = (r,g,b)
	def setColor(self, color):
		self.color = color
	def getColor(self):
		return self.color

class ColorRGBOps(object):
	def __init__(self):
		self.redChannel = 0
		self.greenChannel = 1
		self.blueChannel = 2
	def swapChannel(self, color, first, second):
		color = list(color)
		first = color[first]
		second = color[second]
		color[first] = second
		color[second] = first
		return tuple(color)
	def removeChannel(self, color, channel):
		r,g,b = color
		if channel == self.redChannel:
			r = 0
		if channel == self.greenChannel:
			g = 0
		if channel == self.blueChannel:
			b = 0
		return (r,g,b)
	def grayscale(self, color):
		r,g,b = color
		return ((r+g+b)/3,)*3
	def brighten(self, color, amount):
		if type(amount) == tuple:
			ra,ga,ba = amount
		elif type(amount) == int:
			ra,ga,ba = (amount,amount,amount)
		r,g,b = color
		r -= ra
		g -= ga
		b -= ba
		if r > 255: r = 255
		if g > 255: g = 255
		if b > 255: b = 255
		if r < 0 : r = 10
		if g < 0 : g = 10
		if b < 0 : b = 10
		return (r,g,b)
	def darken(self, color, amount):
		if type(amount) == tuple:
			ra,ga,ba = amount
		elif type(amount) == int:
			ra,ga,ba = (amount,amount,amount)
		r,g,b = color
		r -= ra
		g -= ga
		b -= ba
		if r > 255: r = 255
		if g > 255: g = 255
		if b > 255: b = 255
		if r < 0 : r = 10
		if g < 0 : g = 10
		if b < 0 : b = 10
		return (r,g,b)
	def negative(self, color):
		r,g,b = color
		color = (255-r, 255-g, 255-b)
		return color

ColorRGBOps = ColorRGBOps()