#fades colors
class ColorFadePattern:
	# Integral color shifting
	def __init__(self):
		self.phase = 0
		self.phasetable = [
			(255,   0,   0),
			(255,  64,   0),
			(255, 128,   0),
			(255, 192,   0),
			(255, 255,   0),
			(192, 255,   0),
			(128, 255,   0),
			( 64, 255,   0),
			(  0, 255,   0),
			(  0, 192,   0),
			(  0, 192,  64),
			(  0, 192, 128),
			(  0, 255, 192),
			(  0, 255, 255),
			(  0, 192, 255),
			(  0, 128, 255),
			(  0,   0, 255),
			( 64,   0, 255),
			(128,   0, 255),
			(192,   0, 255),
			(255,   0, 255),
			(255, 128, 255),
			(255, 255, 255),
			(255, 255, 128),
			(255, 128, 128),
			(255, 128,   0),
		]
	def generate(self):
		data = []
		for i in xrange(170):
			r, g, b = self.phasetable[int(self.phase)]
			data.append((r, g, b))
		self.phase += 1
		if (self.phase >= len(self.phasetable)):
			self.phase = 0
		return data
