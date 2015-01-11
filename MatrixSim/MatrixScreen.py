
import sys,os
#first things first make sure we are able to find the necesary files we need.
cwd = os.getcwd()
sys.path.append(cwd)
sys.path.append(cwd+"/patterns/Graphics/")

from Graphics import *
from Pixel import *
from matrix import *

class MatrixScreen(object):
	import pygame
	def __init__(self, width, height, pixelSize):
		self.width = width
		self.height = height
		self.pixelSize = pixelSize

		self.pixels = []

		self.window_width = height*pixelSize
		self.window_height = width*pixelSize

		self.window = self.pygame.display.set_mode((self.window_width, self.window_height))

		widthRange = range(0, self.window_width, pixelSize)
		heightRange = range(0, self.window_height, pixelSize)[::-1] #reverse order because else the display is flipped.


		#due to how the ledmatrix is display x, y are filled as is the
		#window_width/height thing a bit above here.
		for x in widthRange:
			for y in heightRange:
				pos = (x,y)
				color = randColor()
				pixel = Pixel(pos, pixelSize, color)
				self.pixels.append(pixel)
	def handleInput(self):
		for event in self.pygame.event.get():
			if event.type == self.pygame.QUIT:
				sys.exit(0)
	def draw(self, data):
		#extract pixels and color from data
		#get both a list index and the color data.
		for i,color in enumerate(data):
			self.pixels[i].setColor(color)

		#clear the pygame window
		self.window.fill(BLACK)

		#display the pixels.
		for pixel in self.pixels:
			self.pygame.draw.rect(self.window, pixel.color, pixel.getRect())
			#draw a nice little square around so it looks more like a pixel.
			self.pygame.draw.rect(self.window, BLACK, pixel.getRect(), 1)

		#update the screen so our data show.
		self.pygame.display.update()
	def process(self, data):
		self.handleInput()
		self.draw(data)
	def __del__(self):
		self.pygame.quit()