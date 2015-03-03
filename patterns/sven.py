from matrix import *
from Graphics import *  
import random
import time


class sven(object):
	def __init__(self):
		self.graphics = Graphics(matrix_width, matrix_height)
		self.color = RED
		BLUE = self.color = RED
		self.pos = 0,0
		
	def generate(self):
		self.graphics.fill(GREEN)
		x, y = self.pos
		#self.graphics.drawLine(matrix_width-x,matrix_height-y,x,y, self.color)
		b = 0
		i = 0
		while(1):
			#b2 = 0
			#i = 0
			while(i<= 10):
				color2 = randColor()
				a = random.randint(0,matrix_width)
				b = random.randint(0,matrix_height)
				self.graphics.drawPixel(a,b, color2)
				print i, ":", b
				i = i+1

			#time.sleep(1)
			b = b +1
			return self.graphics.getSurface()
