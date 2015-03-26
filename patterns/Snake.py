from Graphics.Graphics import Graphics, GREEN, BLUE, WHITE, BLACK
from matrix import matrix_width, matrix_height
from Controllers import PygameController, XboxController
import random
import time

# for now the snakeController is a pygame controller.
# class SnakeController(PygameController, XboxController):
#     def __init__(self, plugged=0):
#         PygameController.__init__(self, plugged)
#         self.UP = XboxController.UP_DPAD
#         self.DOWN = XboxController.DOWN_DPAD
#         self.LEFT = XboxController.LEFT_DPAD
#         self.RIGHT = XboxController.RIGHT_DPAD
#     def getUp(self):
#         value = self.getButtons(self.UP)
#         return value
#     def getDown(self):
#         value = self.getButtons(self.DOWN)
#         return value
#     def getLeft(self):
#         value = self.getButtons(self.LEFT)
#         return value
#     def getRight(self):
#         value = self.getButtons(self.RIGHT)
#         return value


class SnakeController(PygameController, XboxController):
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


class Food(object):
    def __init__(self, pos, color, graphics):
        self.pos = pos
        self.graphics = graphics
        self.color = color

    def setPos(self, pos):
        self.pos = pos

    def randPos(self):
        x = random.randint(0, matrix_width - 1)
        y = random.randint(0, matrix_height - 1)
        self.pos = x, y

    def randColor(self):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        self.color = (r, g, b)

    def draw(self):
        x, y = self.pos
        self.graphics.drawPixel(x, y, self.color)



class Snake(object):
    def __init__(self, speed=8, plugged=0):
        self.graphics = Graphics(matrix_width, matrix_height)

        self.controller = SnakeController(plugged)

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
        self.food = Food((0, 0), WHITE, self.graphics)
        self.food.randPos()

        # add our head to our body :)
        self.body.append(self.pos)

    def inputHandling(self):
        if self.controller.getUp() and self.deltax != -1:
            self.deltax = 1
            self.deltay = 0
        if self.controller.getDown() and self.deltax != 1:
            self.deltax = -1
            self.deltay = 0
        if self.controller.getLeft() and self.deltay != 1:
            self.deltax = 0
            self.deltay = -1
        if self.controller.getRight() and self.deltay != -1:
            self.deltax = 0
            self.deltay = 1

    def update(self):
        x,y = self.pos
        #update position certain amount per second.
        if( (time.time()-self.previousTick) >= 1./self.speed ):
            self.previousTick = time.time()
            x += self.deltax
            y += self.deltay
            #if the snake goes offscreen it appears on the other side.
            if x >= matrix_width:
                x = 0
                self.pos = x,y
            elif x < 0:
                x = matrix_width-1
                self.pos = x,y
            elif y >= matrix_height:
                y = 0
                self.pos = x,y
            elif y < 0:
                y = matrix_height-1
                self.pos = x,y
            else:
                self.pos = x,y

            if len(self.body) > self.tailLen:
                del self.body[0]
            self.body.append(self.pos)
            #and if we hit food increase tail length
            #also increase our speed
            if self.food.pos == self.pos:
                self.speed += 0.5
                while self.food.pos in self.body:
                    self.food.randPos()
                self.food.randColor()
                self.tailLen += 1
            #look if our "tail is in the way" and only if we have a tail.
            if len(self.body) > 2:
                #check if head colides with body
                if len(self.body) != len(set(self.body)):
                    self.body = [self.pos]
                    self.tailLen = 0
                    self.speed = self.original_speed
                    self.deltax = 0
                    self.deltay = 0
        
    def draw(self):
        for i,(x,y) in enumerate(self.body):
            if i == self.tailLen:
                #draw our head a certain color
                self.graphics.drawPixel(x,y, self.head_color)
            else:
                # else just draw our body this color
                # self.graphics.drawPixel(x,y,Color.subtract(self.body_color, (int(255/(i+1)),)*3))
                self.graphics.drawPixel(x, y, (255, 255, 255))
        self.food.draw()
    def generate(self):
        self.graphics.fill(BLACK)
        self.inputHandling()
        self.update()
        self.draw()
        return self.graphics.getSurface()
