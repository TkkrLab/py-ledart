
import sys,os
#first things first make sure we are able to find the necesary files we need.
wd = os.path.join(os.path.dirname(__file__), os.path.pardir)
print wd
sys.path.append(wd)
sys.path.append(wd+"/patterns/Graphics/")
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
		self.pygame.display.set_caption("pygame artnet matrix simulator.")

		widthRange = range(0, self.window_width, pixelSize)
		heightRange = range(0, self.window_height, pixelSize)[::-1] #reverse order because else the display is flipped.


		#due to how the ledmatrix is display x, y are filled as is the
		#window_width/height thing a bit above here.
		for x in widthRange:
			for y in heightRange:
				pos = (x,y)
				color = BLUE
				pixel = Pixel(pos, pixelSize, color)
				self.pixels.append(pixel)
	def handleInput(self):
		self.pygame.event.pump()
		for event in self.pygame.event.get():
			if event.type == self.pygame.QUIT:
				sys.exit(0)
			if event.type == self.pygame.KEYDOWN:
				if event.key == self.pygame.K_c and self.pygame.key.get_mods()&self.pygame.KMOD_LCTRL:
					raise KeyboardInterrupt
	def draw(self, data):
		#extract pixels and color from data
		#get both a list index and the color data.
		for i,color in enumerate(data):
			self.pixels[i].setColor(color)

		#clear the pygame window
		self.window.fill(BLACK)

		#display the pixels.
		for pixel in self.pixels:
			r = pixel.color[COLOR_ORDER[0]]
			g = pixel.color[COLOR_ORDER[1]]
			b = pixel.color[COLOR_ORDER[2]]
			color = (r,g,b)
			self.pygame.draw.rect(self.window, color, pixel.getRect())
			#draw a nice little square around so it looks more like a pixel.
			self.pygame.draw.rect(self.window, BLACK, pixel.getRect(), 1)

		#update the screen so our data show.
		self.pygame.display.update()
	def process(self, data):
		self.handleInput()
		self.draw(data)
	def __del__(self):
		self.pygame.quit()