from Graphics.Graphics import Graphics, GREEN, BLUE
from Controllers import ttyController, PongTtyController
from matrix import *
import time


# this controller class if for the wireless pong controllers.
# with the 2.4 GHz nrf's inside.
class PongController(ttyController, PongTtyController):
    def __init__(self, plugged=0, baud=115200, port="ACM", debug=False):
        ttyController.__init__(self, plugged, baud, port, debug)

    def getPos(self, button):
        value = ttyController.getPos(self, button)
        value = translate(value, 0, 255, 0, 10)
        return int(value)


# this controller is really simple it plays against it's self.
class PongControllerAuto(ttyController, PongTtyController):
    def __init__(self, plugged=0, ball=None):
        self.ball = ball

    def getPos(self, button):
        return self.ball.pos[0]

# class PongController(DummyController, XboxController):
#     def __init__(self, plugged=0):
#         DummyController.__init__(self, plugged)
#         self.time = time.time
#         self.tick = 0.01
#         self.previousTick = 0
#         self.pos = 0
#     def getPos(self, button):
#         millis = self.time()
#         if(millis - self.previousTick > self.tick):
#             self.previousTick = millis
#             self.pos  = DummyController.getValue(self)
#             #print self.pos
#         return int(translate(self.pos, 0, 1023, 0, 10.1))

# class PongController(PygameController, XboxController):
#    def __init__(self, plugged = 0):
#        PygameController.__init__(self, plugged)
#    def getPos(self, button):
#        value = PygameController.getAxis(self, button)
#        value = translate(value, 1.0, -1.0, 0, 10.1)
#        value = int(round(value))
#        return value

# class PongController(PygameController, MegaController):
#     def __init__(self, plugged=0):
#         PygameController.__init__(self, plugged)
#     def getPos(self, button):
#         value = PygameController.getAxis(self, button)
#         value = translate(value, 1.0,-1.0, 0, 10.1)
#         value = int(round(value))
#         print value
#         return value


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
        x, y = self.pos
        # offset make it go a bit into the screen on one side
        x = self.inputValue - 1
        # boundery check make it only go one block in at the other end though.
        if x >= self.graphics.width - 2:
            x = self.graphics.width - 2
        self.pos = x, self.side

    def handleInput(self):
        self.inputValue = self.controller.getPos(self.controller_in)

    def draw(self):
        x, y = self.pos
        self.graphics.drawLine(x, y, x + self.paddle_width - 1, y, self.color)

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
    """
    Pong game
    """
    def __init__(self, speed=matrix_height/2):
        self.graphics = Graphics(matrix_width, matrix_height)

        # create a ball. multiple balls should be possible :)
        self.ball = Ball((self.graphics.width/2, self.graphics.height/2),
                         GREEN, self.graphics)

        # try to use the tty controller.
        # but if it's not available use the automatic one.
        try:
            self.controller = PongController(plugged=0, baud=9600, port="ACM")
        except Exception, e:
            print "unable to find controllers playing on automatic\n>> "+str(e)
            self.controller = PongControllerAuto(plugged=0, ball=self.ball)
        
        #create two paddles
        paddle1_pos = (0, 0)
        self.paddle1 = (Paddle(paddle1_pos, BLUE, self.controller,
                        self.controller.POT1, self.graphics))
        paddle2_pos = (0, matrix_height-1)
        self.paddle2 = (Paddle(paddle2_pos, BLUE, self.controller,
                        self.controller.POT2, self.graphics))

        #timing variables used to controle the speed of the ball
        self.start_speed = speed
        self.speed = speed #speed = pixels/s
        self.previous = 0
        
        self.print_score = False
    #returns True on hit, and False otherwise.
    def checkOnPaddle(self, paddle, ball):
        #get all the attributes in a convenient form
        px,py = paddle.getPos()
        pwidth = paddle.getWidth()
        bx,by = ball.getPos()
        bsize = ball.getPos()
        
        #check wheter the ball hit the paddle
        if by+ball.dy == py and bx >= px and bx < px+pwidth:
            return True
        else:
            return False
    
    #returns a random number suited to be used for
    #a random direction the ball moves in
    #when the game starts.
    def getRandomDir(self):
        direction = 0
        #don't want dir to be 0
        while not direction:
            direction = random.randint(-1,1)
        return direction
    #main processing function that calls all the processing functions.
    #besides that checks if the ball hit a paddle and lets 
    #the ball now it collided.
    #further it allso controlles the speed of the ball.
    #and allso score is tracked from here.
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
            self.speed += 0.4
        else:
            self.ball.setColliding(False)
        
        #if ball beyond left or right limit set score
        #and reset the ball with a random direction, and orignal speed.
        bx,by = self.ball.getPos()
        lim = 2 #so lim(it) pixel out, it resets
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
    #calls the handling processes for
    #all the objects that need it.
    def handleInput(self):
        self.paddle1.handleInput()
        self.paddle2.handleInput()
    #draw all the thing that need to be draw.
    #draw the ball and paddles.
    def draw(self):
        self.graphics.fill(BLACK)
        self.ball.draw()
        self.paddle1.draw()
        self.paddle2.draw()
    #returns the generated pattern for displaying.
    def generate(self):
        self.handleInput()
        self.process()
        self.draw()
        return self.graphics.getSurface()
