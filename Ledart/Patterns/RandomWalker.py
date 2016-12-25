from Ledart import Graphics, BLACK, GREEN
from Ledart import constrain
from Ledart import Vector

from colorsys import hsv_to_rgb
import random

class Walker(object):
    def __init__(self, g, x, y, mode, stepsize=random.randint(1, 11)):
        self.pos = Vector(x=x, y=y)
        self.mode = mode
        self.stepsize = stepsize
        self.numsteps = 1
        self.previous = 0
        self.g = g

    def rightangle_choice(self):
        choice = random.randint(0, 4)
        if(choice == 0):
            self.pos.x += self.stepsize
        elif(choice == 1):
            self.pos.x -= self.stepsize
        elif(choice == 2):
            self.pos.y += self.stepsize
        elif(choice == 3):
            self.pos.y -= self.stepsize

    def anydir_choice(self):
        self.xdir = random.randint(-1, 1) * self.stepsize
        self.ydir = random.randint(-1, 1) * self.stepsize
        self.pos += Vector(x=self.xdir, y=self.ydir)

    def walk(self):
        self.previous = Vector(x=self.pos.x, y=self.pos.y)
        
        if(self.mode == 'rightangle'):
            self.rightangle_choice()
        if(self.mode == 'anydir'):
            self.anydir_choice()

        self.handle_collision()

        self.color = [min(int(0xff * c), 0xff) for c in hsv_to_rgb(self.numsteps / float(0xfff), 1, 1)]
        self.numsteps += 1

    def handle_collision(self):
        self.pos.x = constrain(self.pos.x, 0, self.g.width)
        self.pos.y = constrain(self.pos.y, 0, self.g.height)

    def draw(self):
        self.g.draw_line(self.pos.x, self.pos.y, self.previous.x, self.previous.y, self.color)

class RandomWalker(Graphics):
    def __init__(self, **kwargs):
        Graphics.__init__(self, **kwargs)
        mode = kwargs.get('mode', 'anydir')
        self.walker = Walker(self, self.width/2, self.height/2, mode)

    def generate(self):
        # self.fill(BLACK)
        self.walker.walk()
        self.walker.draw()