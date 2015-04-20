class ColorHSL(object):
	def __init__(self, h, s, l):
		self.hue = h
		self.saturation = s
		self.lightness = l
	def getColor(self):
		return (self.hue, self.saturation, self.lightness)

class ColorHSLOps(object):
	def __init__(self):
		pass

ColorHSLOps = ColorHSLOps