from Graphics import *
from Controllers.Controllers import *
import time

class SnakeController(PygameController, XboxController):
    def __init__(self, plugged=0):
        PygameController.__init__(self, plugged)
        self.UP = XboxController.UP_DPAD
        self.DOWN = XboxController.DOWN_DPAD
        self.LEFT = XboxController.LEFT_DPAD
        self.RIGHT = XboxController.RIGHT_DPAD
    def getUp(self):
        value = self.getButtons(self.UP)
        return value
    def getDown(self):
        value = self.getButtons(self.DOWN)
        return value
    def getLeft(self):
        value = self.getButtons(self.LEFT)
        return value
    def getRight(self):
        value = self.getButtons(self.RIGHT)
        return value

class Food(object):
    def __init__(self, pos, color, graphics):
        self.pos = pos
        self.graphics = graphics
        self.color = color
    def setPos(self, pos):
        self.pos = pos
    def randPos(self):
        x = random.randint(0, matrix_width-1)
        y = random.randint(0, matrix_height-1)
        self.pos = x,y
    def randColor(self):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        self.color = (r,g,b)
    def draw(self):
        x,y = self.pos
        self.graphics.drawPixel(x,y, self.color)



class Snake(object):
    def __init__(self, speed=17, plugged = 0):
        self.graphics = Graphics(matrix_width, matrix_height)
        
        self.controller = SnakeController(plugged)

        self.color = WHITE
        
        self.pos = random.randint(1,matrix_width-1), random.randint(1,matrix_height-1)
        self.speed = speed
        self.previousTick = 0
        self.deltax,self.deltay = 0,0
        
        self.body = []
        self.tailLen = 0
        self.food = Food((0,0), WHITE, self.graphics)
        self.food.randPos()
        
        #add our head to our body :)
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
            if self.food.pos == self.pos:
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
                    self.deltax = 0
                    self.deltay = 0
        
    def draw(self):
        for x,y in self.body:
            self.graphics.drawPixel(x,y,self.color)
        self.food.draw()
    def generate(self):
        self.graphics.fill(BLACK)
        self.inputHandling()
        self.update()
        self.draw()
        return self.graphics.getSurface()
