from Graphics import *
import serial, sys

class Controller(object):
	ser_port = None
	def __init__(self, port = "/dev/ttyACM0", baud=9600):
		if not self.ser_port:
			self.ser_port = serial.Serial(port, baud)
	def getPotVal(self):
		try:
			self.ser_port.flushInput()
			value = ord(self.ser_port.read())
			print value
			return value
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
		self.inputValue = 0
	def getPos(self):
		return self.pos
	def getWidth(self):
		return self.paddle_width
	def process(self):
		x,y = self.pos
		x = self.inputValue-1 #offset make it go a bit into the screen on one side
		#boundery check make it only go one block in at the other end though.
		if x >= self.graphics.width-2:
			x = self.graphics.width-2
		self.pos = x,self.side
	def handleInput(self):
		self.inputValue = self.controller.getPotVal()
		"""
		x = self.controller.getPotVal()-1
		if x > self.graphics.getSurfaceWidth()-self.paddle_width:
			x = self.graphics.getSurfaceWidth()-self.paddle_width+1
		self.pos = x,self.side
		"""
	def draw(self):
		x,y = self.pos
		self.graphics.drawLine(x, y, x+self.paddle_width-1, y, self.color)

class Ball(object):
	def __init__(self, pos, color, graphics):
		self.graphics = graphics
		self.pos = pos
		self.size = 1
		self.color = color
		self.colliding = False
		self.dx = 1
		self.dy = 1
	def getPos(self):
		return self.pos
	def setPos(self, pos):
		self.pos = pos
	def getSize(self):
		return self.size
	def setColliding(self, colliding):
		self.colliding = colliding
	def process(self):
		x,y = self.pos
		if x >= self.graphics.width-1:
			x = self.graphics.width-1
			self.dx *= -1
		elif x <= 0:
			x = 0
			self.dx *= -1
		
		#the pong game will let us know when the ball is colliding with a paddle
		if self.colliding:
			self.dy *= -1
		
		x += self.dx
		y += self.dy
		self.pos = x,y
	def draw(self):
		x,y = self.pos
		self.graphics.drawPixel(x,y,self.color)

class Pong(object):
	def __init__(self):
		self.graphics = Graphics(matrix_width, matrix_height)
		self.controller = Controller("/dev/ttyACM0", baud=9600)
		self.paddle1 = Paddle((0,0), BLUE, self.controller, self.graphics)
		self.paddle2 = Paddle((0, matrix_height-1), BLUE, self.controller, self.graphics)
		self.ball = Ball((self.graphics.width/2, self.graphics.height/2), GREEN, self.graphics)
	
	def checkOnPaddle(self, paddle, ball):
		
		px,py = paddle.getPos()
		pwidth = paddle.getWidth()
		bx,by = ball.getPos()
		bsize = ball.getPos()
		
		if by == py and bx >= px and bx < px+pwidth:
			return True
		else:
			return False
	
	def process(self):
		self.ball.process()
		self.paddle1.process()
		self.paddle2.process()
		
		#if ball on paddle bounce it back.
		if self.checkOnPaddle(self.paddle1, self.ball):
			self.ball.setColliding(True)
		elif self.checkOnPaddle(self.paddle2, self.ball):
			self.ball.setColliding(True)
		else:
			self.ball.setColliding(False)
		#if ball beyond left or right limit something score ?
		#for now just reset
		bx,by = self.ball.getPos()
		if by < self.graphics.width-10 or by > self.graphics.height+10:
			self.ball.setPos((self.graphics.width/2, self.graphics.height/2))
	def handleInput(self):
		self.paddle1.handleInput()
		self.paddle2.handleInput()
	def draw(self):
		self.graphics.fill(BLACK)
		self.paddle1.draw()
		self.paddle2.draw()
		self.ball.draw()
	def generate(self):
		self.handleInput()
		self.process()
		self.draw()
		return self.graphics.getSurface()
