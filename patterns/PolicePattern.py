class PolicePattern:
	# Rotating line with fading trail, default color blue
	def __init__(self, backwards=False, color=(0, 0, 255)):
		self.backwards = backwards
		self.color = color
		self.pos = 0
	def generate(self):
		data = []
		if self.backwards:
			leds = xrange(170, 0, -1)
		else:
			leds = xrange(0, 170, 1)
		for i in leds:
			# Light one LED at full strength, its neighbors at half
			place = (i % 7) + self.pos
			if (place >= 7):
				place -= 7
			distance = abs(3 - place)
			# val becomes 0 0.5 or 1
			val = 2 - distance
			if (val < 0):
				val = 0
			val /= 2.0
			# Multiply RGB-values by val
			color = map(lambda x: int(x * val), self.color)
			data.append(color)
		self.pos += 1
		if (self.pos >= 7):
			self.pos = 0
		return data
