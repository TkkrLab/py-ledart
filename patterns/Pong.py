from Graphics import *
from Controllers import *
import serial, sys, time


class PongController(PygameController, MegaController):
    def __init__(self, plugged=0):
        PygameController.__init__(self, plugged)
    def getPos(self, button):
        value = PygameController.getAxis(self, button)
        value = translate(value, 1.0,-1.0, 0, 10.1)
        value = int(round(value))
        print value
        return value

class Paddle(object):
    def __init__(self, pos, color, controller, controller_in, graphics):
        self.pos = pos
        self.paddle_width = 3
        self.side = pos[1]
        
        self.score = 0
        
        self.color = color
        
        self.controller = controller
        self.controller_in = controller_in
        
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
        self.inputValue = self.controller.getPos(self.controller_in)
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
        
        self.tail = []
        self.tail_lim = 3
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
        #do boundery checking
        if x >= self.graphics.width-1:
            x = self.graphics.width-1
            self.dx *= -1
        elif x <= 0:
            x = 0
            self.dx *= -1
        
        #the pong game will let us know when the ball is colliding with a paddle
        if self.colliding:
            self.dy *= -1
        
        #add deltas to cordinates to get movement.
        x += self.dx
        y += self.dy
        
        #save our new cordinates
        self.pos = x,y
    def draw(self):
        x,y = self.pos
        self.graphics.drawPixel(x,y,self.color)

class Pong(object):
    def __init__(self, speed = matrix_height/2):
        self.graphics = Graphics(matrix_width, matrix_height)
        
        self.controller = PongController(plugged = 0)#Controller("/dev/ttyACM1", baud=9600)
        
        self.paddle1 = Paddle((0,0), BLUE, self.controller, self.controller.THROTTLE_Y, self.graphics)
        self.paddle2 = Paddle((0, matrix_height-1), BLUE, self.controller, self.controller.JOY_Y, self.graphics)
        
        self.ball = Ball((self.graphics.width/2, self.graphics.height/2),GREEN, self.graphics)
        #timing variables used to controle the speed of the ball
        self.start_speed = speed
        self.speed = speed #speed = pixels/s
        self.previous = 0
        
        self.print_score = False
    def checkOnPaddle(self, paddle, ball):
        
        px,py = paddle.getPos()
        pwidth = paddle.getWidth()
        bx,by = ball.getPos()
        bsize = ball.getPos()
        
        if by+ball.dy == py and bx >= px and bx < px+pwidth:
            return True
        else:
            return False
    
    def getRandomDir(self):
        direction = 0
        #don't want dir to be 0
        while not direction:
            direction = random.randint(-1,1)
        return direction
    
    def process(self):
        self.paddle1.process()
        self.paddle2.process()
        #only move ball x amount per second.
        if( (time.time()-self.previous) >= 1./self.speed ):
            self.previous = time.time()
            self.ball.process()
        
        #if ball on paddle bounce it back.
        if self.checkOnPaddle(self.paddle1, self.ball) or \
            self.checkOnPaddle(self.paddle2, self.ball):
            self.ball.setColliding(True)
            self.speed += 0.3
        else:
            self.ball.setColliding(False)
        
        #if ball beyond left or right limit something score ?
        #for now just reset
        bx,by = self.ball.getPos()
        lim = 2 #so lim(it) pixel out it resets
        if by < -lim or by > self.graphics.height+lim:
            if by < -lim:
                self.paddle1.score += 1
            if by > self.graphics.height+lim:
                self.paddle2.score += 1
            #print score shows it works!
            if self.print_score:
                print "player1 score: %d"%(self.paddle1.score)
                print "player2 score: %d"%(self.paddle2.score)
            self.ball.setPos((self.graphics.width/2, self.graphics.height/2))
            self.ball.dx = self.getRandomDir()
            self.ball.dy = self.getRandomDir()
            self.speed = self.start_speed
    def handleInput(self):
        self.paddle1.handleInput()
        self.paddle2.handleInput()
    def draw(self):
        self.graphics.fill(BLACK)
        self.ball.draw()
        self.paddle1.draw()
        self.paddle2.draw()
    def generate(self):
        self.handleInput()
        self.process()
        self.draw()
        return self.graphics.getSurface()
