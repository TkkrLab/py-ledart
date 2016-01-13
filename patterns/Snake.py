from Tools.Graphics import Graphics, GREEN, BLUE, WHITE, BLACK
from Tools.Controllers import *
from matrix import matrix_width, matrix_height
import random
import time

select = 'Snake'

# for now the snakeController is a pygame controller.
class SnakeControllerXbox(PygameController, XboxController):
    def __init__(self, plugged=0):
        PygameController.__init__(self, plugged)

    def getUp(self):
        return self.getButtons(self.UP_DPAD)

    def getDown(self):
        return self.getButtons(self.DOWN_DPAD)

    def getLeft(self):
        return self.getButtons(self.LEFT_DPAD)

    def getRight(self):
        return self.getButtons(self.RIGHT_DPAD)


class SnakeControllerLogiTech(PygameController, LogiTechController):
    def __init__(self, plugged=0):
        PygameController.__init__(self, plugged)

    def getUp(self):
        return self.getButtons(self.BUTTON_UP)

    def getDown(self):
        return self.getButtons(self.BUTTON_DOWN)

    def getLeft(self):
        return self.getButtons(self.BUTTON_LEFT)

    def getRight(self):
        return self.getButtons(self.BUTTON_RIGHT)


controllers = [SnakeControllerXbox, SnakeControllerLogiTech]

class Food(object):
    def __init__(self, pos, color, game):
        self.pos = pos
        self.game = game
        self.color = color

    def setPos(self, pos):
        self.pos = pos

    def randPos(self):
        x = random.randint(0, matrix_width - 1)
        y = random.randint(0, matrix_height - 1)
        self.pos = x, y

    def randColor(self):
        r = random.randint(100, 255)
        g = random.randint(100, 255)
        b = random.randint(100, 255)
        self.color = (r, g, b)

    def draw(self):
        x, y = self.pos
        self.game.draw_pixel(x, y, self.color)


class Snake(Graphics):
    def __init__(self, speed=8, select=0):
        Graphics.__init__(self, matrix_width, matrix_height)

        self.controller = controllers[select]()

        self.body_color = GREEN
        self.head_color = BLUE

        x = random.randint(1, matrix_width - 1)
        y = random.randint(1, matrix_height - 1)
        self.pos = x, y
        self.original_speed = speed
        self.speed = speed
        self.previousTick = 0
        self.deltax, self.deltay = 0, 0

        self.body = []
        self.tailLen = 0
        self.food = Food((0, 0), WHITE, self)
        self.food.randPos()

        # add our head to our body :)
        self.body.append(self.pos)

    def inputHandling(self):
        if self.controller.getUp():
            self.deltax = 0
            self.deltay = -1
        if self.controller.getDown():
            self.deltax = 0
            self.deltay = 1
        if self.controller.getLeft():
            self.deltax = -1
            self.deltay = 0
        if self.controller.getRight():
            self.deltax = 1
            self.deltay = 0

    def update(self):
        x, y = self.pos
        # update position certain amount per second.
        if((time.time() - self.previousTick) >= 1. / self.speed):
            self.previousTick = time.time()
            x += self.deltax
            y += self.deltay
            # if the snake goes offscreen it appears on the other side.
            if x >= matrix_width:
                x = 0
                self.pos = x, y
            elif x < 0:
                x = matrix_width - 1
                self.pos = x, y
            elif y >= matrix_height:
                y = 0
                self.pos = x, y
            elif y < 0:
                y = matrix_height - 1
                self.pos = x, y
            else:
                self.pos = x, y

            if len(self.body) > self.tailLen:
                del self.body[0]
            self.body.append(self.pos)
            # and if we hit food increase tail length
            # also increase our speed
            if self.food.pos == self.pos:
                if self.tailLen > self.speed:
                    self.speed = self.tailLen * 2
                # while self.food.pos in self.body:
                self.food.randPos()
                self.food.randColor()
                self.tailLen += 1
            # look if our "tail is in the way" and only if we have a tail.
            if len(self.body) > 2:
                # check if head colides with body
                if len(self.body) != len(set(self.body)):
                    self.body = [self.pos]
                    self.tailLen = 0
                    self.speed = self.original_speed
                    self.deltax = 0
                    self.deltay = 0

    def draw(self):
        self.fill(BLACK)
        for i, (x, y) in enumerate(self.body):
            if i == self.tailLen:
                # draw our head a certain color
                self.draw_pixel(x, y, self.head_color)
            else:
                # else just draw our body this color
                # self.graphics.draw_pixel(x,y,Color.subtract(self.body_color, (int(255/(i+1)),)*3))
                self.draw_pixel(x, y, (255, 255, 255))
        self.food.draw()

    def generate(self):
        self.inputHandling()
        self.update()
        self.draw()
