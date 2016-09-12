from Ledart.Tools.Graphics import Graphics
from Ledart.Tools.Graphics import BLUE, BLACK
from Ledart.Tools.Timing import Timer
from Ledart.stripinfo import strip_width, strip_height
import random


class Ripple(object):
    def __init__(self, pos, color, graphics):
        self.pos = pos
        self.speed = random.random() * 2
        self.radius = 1
        self.color = color
        self.graphics = graphics
    
    def process(self):
        self.radius += self.speed
        if self.radius > max(self.graphics.width, self.graphics.height):
            self.pos = (random.randint(0, strip_width), random.randint(0, strip_height))
            self.radius = 0
    
    def draw(self):
        x, y = self.pos
        self.graphics.draw_circle(x, y, self.radius, self.color)


class Water(Graphics):
    def __init__(self):
        Graphics.__init__(self, width=strip_width, height=strip_height)
        self.ripples = []
        for i in range(0, 4):
            x, y = random.randint(0, strip_width), random.randint(0, strip_height)
            self.ripples.append(Ripple((x, y), BLUE, self))
    
    def generate(self):
        self.fill(BLACK)
        for ripple in self.ripples:
            ripple.process()
            ripple.draw()