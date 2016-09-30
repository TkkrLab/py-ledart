# raindrop by Duality

from Ledart.Tools.Graphics import Graphics, BLACK
import random


class RainDrop(object):
    def __init__(self, game, color=(100, 255, 100)):
        self.color = color
        self.y = 0
        self.x = random.randint(0, game.width)
        self.pos = (self.x, self.y)
        self.height = self.y

    def getPos(self):
        return self.pos

    def setHeight(self, height):
        self.height = height

    def getHeight(self):
        return self.height

    def incrementHeight(self):
        self.height += 1
        self.y = self.height
        self.pos = (self.x, self.y)


class RainPattern(Graphics):
    """
        rain pattern implementation by Duality
        will call 2.0 :D
    """
    def __init__(self, **kwargs):
        Graphics.__init__(self, **kwargs)
        self.color = kwargs.get('color', (80, 255, 100))
        self.chance = kwargs.get('chance', 0.04)
        # insert single drop for testing
        self.drops = [RainDrop(self, self.color)]

    def generate(self):
        self.fill(BLACK)
        # put drop in data and increment it's position
        for drop in self.drops:
            # calculate where to put it
            index = ((drop.y - 1) * self.width + drop.x) - 1
            # put drop oN strip screen
            if index >= 0:
                self.draw_pixel(drop.x, drop.y - 1, drop.color)
            # increment it's height
            drop.incrementHeight()
            # if it falls of the screen remove it.
            if drop.getHeight() > self.height:
                self.drops.remove(drop)
        # add a random chance for drops to appear.
        if(random.random() < self.chance):
            raindrop = RainDrop(self.color)
            self.drops.append(raindrop)
