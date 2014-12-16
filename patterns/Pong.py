from Graphics import *
import serial, sys

class Controller(object):
	def __init__(self, port = "/dev/ttyACM0", baud=9600):
		self.ser_port = serial.Serial(port, baud)
	def getPotVal(self):
		try:
			self.ser_port.flushInput()
			return ord(self.ser_port.read())
		except:
			sys.exit(0)

class Paddle(object):
	def __init__(self, pos, color, controller, graphics):
		self.pos = pos
		self.paddle_width = 3
		self.side = pos[1]
		self.color = color
		self.controller = controller
		self.graphics = graphics
	def process(self):
		pass
	def handleInput(self):
		x = self.controller.getPotVal()-1
		if x > self.graphics.getSurfaceWidth()-self.paddle_width:
			x = self.graphics.getSurfaceWidth()-self.paddle_width+1
		self.pos = x,self.side
	def draw(self):
		x,y = self.pos
		self.graphics.drawLine(x, y, x+self.paddle_width-1, y, self.color)

class Pong(object):
	def __init__(self):
		self.graphics = Graphics(matrix_width, matrix_height)
		
		self.player1 = Controller("/dev/ttyACM0", baud=9600)
		self.paddle1 = Paddle((0,0), BLUE, self.player1, self.graphics)
	def generate(self):
		self.graphics.fill(BLACK)
		self.paddle1.handleInput()
		self.paddle1.process()
		self.paddle1.draw()
		return self.graphics.getSurface()
