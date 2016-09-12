from Ledart.Tools.Graphics import Graphics, GREEN, BLUE, BLACK
from Ledart.Tools.Controllers import *
from Ledart.stripinfo import strip_width, strip_height
from itertools import count
import time
import random


# this controller class is for the wireless pong controllers.
# with the 2.4 GHz nrf's inside.
class PongControllerTty(ttyController, PongTtyController):
    def __init__(self, plugged=0):
        ttyController.__init__(self, plugged)

    def getPos(self, button):
        value = ttyController.getPos(self, button)
        value = translate(value, 0, 255, 10, 0)
        value = int(round(value))
        return value

class PongControllerLogiTech(PygameController, LogiTechController):
    def __init__(self, plugged=0, **kwargs):
        PygameController.__init__(self, plugged)

    def getPos(self, button):
        value = PygameController.getAxis(self, button)
        value = translate(value, 1.0, -1.0, 0, 10.1)
        value = int(round(value))
        return value

class PongControllerPiranha(PygameController, PiranhaController):
    def __init__(self, plugged=0, **kwargs):
        PygameController.__init__(self, plugged)

    def getPos(self, button):
        value = PygameController.getAxis(self, button)
        value = translate(value, 1.0, -1.0, 0, 10.1)
        value = int(round(value))
        return value

class PongControllerAuto(LogiTechController):
    def __init__(self, plugged=0, ball=None):
        self.ball = ball

    def found(self):
        return True

    def getPos(self, button):
        return self.ball.pos[0]

class PongControllerXbox(PygameController, XboxController):
   def __init__(self, plugged = 0):
       PygameController.__init__(self, plugged)
   def getPos(self, button):
       value = PygameController.getAxis(self, button)
       value = translate(value, 1.0, -1.0, 0, 10.1)
       value = int(round(value))
       return value

class PongControllerMC(PygameController, MegaController):
    def __init__(self, plugged=0):
        PygameController.__init__(self, plugged)
    def getPos(self, button):
        value = PygameController.getAxis(self, button)
        value = translate(value, 1.0,-1.0, 0, 10.1)
        value = int(round(value))
        return value

controllers = []
controllers.append(PongControllerTty)
controllers.append(PongControllerLogiTech)
controllers.append(PongControllerPiranha)
controllers.append(PongControllerXbox)
controllers.append(PongControllerMC)
controllers.append(PongControllerAuto)

ttycontroller = 0
logitechcontroller = 1
piranhacontroller = 2
xboxcontroller = 3
megacontroller = 4
autocontroller = 5


class Paddle(object):
    def __init__(self, pos, color, controller, controller_in, game):
        self.pos = pos
        self.paddle_width = 1
        self.paddle_height = 3
        self.side = pos[1]
        self.score = 0
        self.color = color
        self.controller = controller
        self.controller_in = controller_in
        self.game = game
        self.inputValue = 0

    def getPos(self):
        return self.pos

    def getWidth(self):
        return self.paddle_width

    def getHeight(self):
        return self.paddle_height

    def process(self):
        x, y = self.pos
        # offset make it go a bit into the screen on one side
        y = self.inputValue - 1
        # boundery check make it only go one block in at the other end though.
        if y >= self.game.get_height() - 2:
            y = self.game.get_height() - 2
        self.pos = self.side, y

    def handleInput(self):
        self.inputValue = self.controller.getPos(self.controller_in)

    def draw(self):
        x, y = self.pos
        self.game.draw_line(x, y, x, y + self.paddle_height - 1, self.color)


class Ball(object):
    def __init__(self, pos, color, game):
        self.game = game
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
        x, y = self.pos
        # do boundery checking
        if y >= self.game.get_height() - 1:
            y = self.game.get_height() - 1
            self.dy *= -1
        elif y <= 0:
            y = 0
            self.dy *= -1

        # the pong game will let us know when the ball is
        # colliding with a paddle
        if self.colliding:
            self.dx *= -1

        # add deltas to cordinates to get movement.
        x += self.dx
        y += self.dy

        # save our new cordinates
        self.pos = x, y

    def draw(self):
        x, y = self.pos
        self.game.draw_pixel(x, y, self.color)

class Pong(Graphics):
    """
    Pong game
    """
    def __init__(self, bcolor=GREEN, pcolor=BLUE,
                 speed=strip_height / 2, select=(autocontroller, autocontroller)):
        Graphics.__init__(self, strip_width, strip_height)

        # create a ball. multiple balls should be possible :)
        self.ball = Ball((self.get_width() / 2,
                          self.get_height() / 2),
                         bcolor, self)

        # try to use the controller.
        # but if it's not available use the automatic one.
        s1, s2 = select
        try:
            firstcontroler = controllers[s1]
            self.controller1 = firstcontroler(plugged=s1, ball=self.ball)
            secondcontroler = controllers[s2]
            self.controller2 = secondcontroler(plugged=s2, ball=self.ball)

        except Exception as e:
            fmt = (e, )
            fmtstr = "unable to find controllers playing on automatic\n>> %s\n"
            print(fmtstr % fmt)
            self.controller1 = PongControllerAuto(plugged=s1, ball=self.ball)
            self.controller2 = PongControllerAuto(plugged=s2, ball=self.ball)

        # create two paddles
        paddle1_pos = (0, 0)
        self.paddle1 = (Paddle(paddle1_pos, pcolor, self.controller1,
                        self.controller1.LTHUMB_X, self))
        paddle2_pos = (0, strip_width - 1)
        self.paddle2 = (Paddle(paddle2_pos, pcolor, self.controller2,
                        self.controller2.RTHUMB_X, self))

        # timing variables used to controle the speed of the ball
        self.start_speed = speed
        # speed = pixels/s
        self.speed = speed
        self.previous = 0
        self.print_score = False

        self.count = count(0, 1)

    def checkOnPaddle(self, paddle, ball):
        # returns True on hit, and False otherwise.
        # get all the attributes in a convenient form
        px, py = paddle.getPos()
        pwidth = paddle.getWidth()
        pheight = paddle.getHeight()
        bx, by = ball.getPos()

        # check wheter the ball hit the paddle
        inybound = (by >= py and by <= py + pheight)
        inxbound = ((bx == (px + pwidth)) or (bx == (px - pwidth)))
        if inxbound and inybound:
            return True
        else:
            return False

    def getRandomDir(self):
        # returns a random number suited to be used for
        # a random direction the ball moves in
        # when the game starts.

        direction = 0
        # don't want dir to be 0
        while not direction:
            direction = random.randint(-1, 1)
        return direction

    def process(self):
        # main processing function that calls all the processing functions.
        # besides that checks if the ball hit a paddle and lets
        # the ball now it collided.
        # further it allso controlles the speed of the ball.
        # and allso score is tracked from here.
        self.paddle1.process()
        self.paddle2.process()
        # only move ball x amount per second.
        if((time.time() - self.previous) >= 1. / self.speed):
            self.previous = time.time()
            self.ball.process()

        # if ball on paddle bounce it back.
        onleftpaddle = self.checkOnPaddle(self.paddle1, self.ball)
        onrightpaddle = self.checkOnPaddle(self.paddle2, self.ball)
        if onleftpaddle or onrightpaddle:
            self.ball.setColliding(True)
            self.speed += 0.4
        else:
            self.ball.setColliding(False)

        # if ball beyond left or right limit set score
        # and reset the ball with a random direction, and orignal speed.
        bx, by = self.ball.getPos()
        # so lim(it) pixel out of screen, it resets
        lim = 2
        if bx < -lim or bx > self.get_width() + lim:
            if bx < -lim:
                self.paddle1.score += 1
            if by > self.get_width() + lim:
                xelf.paddle2.score += 1
            # print score shows it works!
            if self.print_score:
                print("player1 score: %d" % (self.paddle1.score))
                print("player2 score: %d" % (self.paddle2.score))
            ballpos = (self.get_width() / 2, self.get_height() / 2)
            self.ball.setPos(ballpos)
            self.ball.dx = self.getRandomDir()
            self.ball.dy = self.getRandomDir()
            self.speed = self.start_speed
    # calls the handling processes for
    # all the objects that need it.

    def handleInput(self):
        self.paddle1.handleInput()
        self.paddle2.handleInput()

    def draw(self):
        # draw all the thing that need to be drawn.
        # draw the ball and paddles.
        self.fill(BLACK)
        self.ball.draw()
        self.paddle1.draw()
        self.paddle2.draw()

    def generate(self):
        # returns the generated pattern for displaying.
        self.handleInput()
        self.process()
        self.draw()


# class TtyPong(Graphics):
#     """
#     Pong game
#     """
#     def __init__(self, bcolor=GREEN, pcolor=BLUE,
#                  speed=strip_height / 2, port="ACM", plugged=0):
#         Graphics.__init__(self, strip_width, strip_height)

#         # create a ball. multiple balls should be possible :)
#         self.ball = Ball((self.get_width() / 2,
#                           self.get_height() / 2),
#                          bcolor, self)

#         # try to use the tty controller.
#         # but if it's not available use the automatic one.
#         try:
#             self.controller = PongController(plugged=plugged, port=port)
#         except Exception as e:
#             fmt = (e, )
#             fmtstr = "unable to find controllers playing on automatic\n>> %s"
#             print(fmtstr % fmt)
#             self.controller = PongControllerAuto(plugged=plugged, ball=self.ball)

#         # create two paddles
#         paddle1_pos = (0, 0)
#         self.paddle1 = (Paddle(paddle1_pos, pcolor, self.controller,
#                         self.controller.POT1, self))
#         paddle2_pos = (0, strip_height - 1)
#         self.paddle2 = (Paddle(paddle2_pos, pcolor, self.controller,
#                         self.controller.POT2, self))

#         # timing variables used to controle the speed of the ball
#         self.start_speed = speed
#         # speed = pixels/s
#         self.speed = speed
#         self.previous = 0
#         self.print_score = False

#     def checkOnPaddle(self, paddle, ball):
#         # returns True on hit, and False otherwise.
#         # get all the attributes in a convenient form
#         px, py = paddle.getPos()
#         pwidth = paddle.getWidth()
#         bx, by = ball.getPos()

#         # check wheter the ball hit the paddle
#         if by + ball.dy == py and bx >= px and bx < px + pwidth:
#             return True
#         else:
#             return False

#     def getRandomDir(self):
#         # returns a random number suited to be used for
#         # a random direction the ball moves in
#         # when the game starts.

#         direction = 0
#         # don't want dir to be 0
#         while not direction:
#             direction = random.randint(-1, 1)
#         return direction

#     def process(self):
#         # main processing function that calls all the processing functions.
#         # besides that checks if the ball hit a paddle and lets
#         # the ball now it collided.
#         # further it allso controlles the speed of the ball.
#         # and allso score is tracked from here.
#         self.paddle1.process()
#         self.paddle2.process()
#         # only move ball x amount per second.
#         if((time.time() - self.previous) >= 1. / self.speed):
#             self.previous = time.time()
#             self.ball.process()

#         # if ball on paddle bounce it back.
#         onleftpaddle = self.checkOnPaddle(self.paddle1, self.ball)
#         onrightpaddle = self.checkOnPaddle(self.paddle2, self.ball)
#         if onleftpaddle or onrightpaddle:
#             self.ball.setColliding(True)
#             self.speed += 0.4
#         else:
#             self.ball.setColliding(False)

#         # if ball beyond left or right limit set score
#         # and reset the ball with a random direction, and orignal speed.
#         bx, by = self.ball.getPos()
#         # so lim(it) pixel out of screen, it resets
#         lim = 2
#         if by < -lim or by > self.get_height() + lim:
#             if by < -lim:
#                 self.paddle1.score += 1
#             if by > self.get_height() + lim:
#                 self.paddle2.score += 1
#             # print score shows it works!
#             if self.print_score:
#                 print("player1 score: %d" % (self.paddle1.score))
#                 print("player2 score: %d" % (self.paddle2.score))
#             ballpos = (self.get_width() / 2, self.get_height() / 2)
#             self.ball.setPos(ballpos)
#             self.ball.dx = self.getRandomDir()
#             self.ball.dy = self.getRandomDir()
#             self.speed = self.start_speed
#     # calls the handling processes for
#     # all the objects that need it.

#     def handleInput(self):
#         self.paddle1.handleInput()
#         self.paddle2.handleInput()

#     def draw(self):
#         # draw all the thing that need to be drawn.
#         # draw the ball and paddles.
#         self.fill(BLACK)
#         self.ball.draw()
#         self.paddle1.draw()
#         self.paddle2.draw()

#     def generate(self):
#         # returns the generated pattern for displaying.
#         self.handleInput()
#         self.process()
#         self.draw()
