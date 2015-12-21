# raindrop by Duality

from matrix import matrix_width, matrix_height, matrix_size
from Tools.Graphics import Graphics, Surface, BLACK, RED, YELLOW, BLUE
from Tools.Timing import Timer
import colorsys
import operator

import random
from math import sin, cos, radians

select = "Smolders"


class RainDrop(object):
    def __init__(self, color=(100, 255, 100)):
        self.color = color
        self.y = 0
        self.x = random.randint(0, matrix_width)
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

def xfrange(start, stop, step):
    while start < stop:
        yield start
        start += step

class Fire(Surface):
    """
        this pattern displays a fire.
        like of pattern.
        
        based upon: http://lodev.org/cgtutor/fire.html
    """
    def __init__(self):
        """ create a surface and a buffer to keep changes in."""
        Surface.__init__(self, width=matrix_width, height=matrix_height)
        self.buffer = Surface(width=matrix_width, height=matrix_height)
        self.bottom_points = [x for x in range(0, self.width)]
    
    def randomize_bottom(self):
        """
            create a random underground for the fire to rise from.
            do it with hls as described on the fire.html,
            but instead of a palette generate the correct colors right away
        """
        for x in self.bottom_points:
            point = (x, self.height - 1)
            h = random.random()
            s = random.random()
            l = random.random()
            r, g, b = colorsys.hls_to_rgb(h / 7, min(0.5, l * 2), 1.0)
            r, g, b = (int(r * 0xff), int(g * 0xff), int(b * 0xff))
            self.buffer[point] = (r, g, b)

    def process(self):
        self.randomize_bottom()
        """
            for every point check certain points relating to it,
            change the colors acordingly and save te change.
        """
        w, h = self.width, self.height
        for y in range(0, h - 1):
            for x in range(0, w):
                p1 = self[((x - 1 + w) % w, (y + 1) % h)]
                p2 = self[((x) % w, (y + 1) % h)]
                p3 = self[((x + 1) % w, (y + 1) % h)]
                p4 = self[((x) % w, (y + 2) % h)]
                color = []
                for i in range(0, 3):
                    c = abs(int((p1[i] + p2[i] + p3[i] - p4[i]) * random.randint(0, 105) / random.randint(50, 600)))
                    color.append(min(c, 0xff))
                color = tuple(color)
                point = (x, y)
                self.buffer[point] = color
    
    def draw(self):
        """ swap out the buffer to see what changed."""
        for point in self.get_points():
            self[point] = self.buffer[point]
    
    def generate(self):
        self.process()
        self.draw()


class Smolders(Surface):
    """
        this pattern displays a fire.
        like of pattern.
        
        based upon: http://lodev.org/cgtutor/fire.html
    """
    def __init__(self):
        """ create a surface and a buffer to keep changes in."""
        Surface.__init__(self, width=matrix_width, height=matrix_height)
        self.buffer = Surface(width=matrix_width, height=matrix_height)
        self.bottom_points = [x for x in range(0, self.width)]
    
    def randomize_bottom(self):
        """
            create a random underground for the fire to rise from.
            do it with hls as described on the fire.html,
            but instead of a palette generate the correct colors right away
        """
        for x in self.bottom_points:
            point = (x, self.height - 1)
            s = 1.0
            h = random.random()
            l = random.random()
            r, g, b = colorsys.hls_to_rgb(h/3.5, min(0.5, l * 2), s)
            r, g, b = (int(r * 0xff), int(g * 0xff), int(b * 0xff))
            self.buffer[point] = (r, g, b)

    def process(self):
        self.randomize_bottom()
        """
            for every point check certain points relating to it,
            change the colors acordingly and save te change.
        """
        w, h = self.width, self.height
        for y in range(0, h - 1):
            for x in range(0, w):
                p1 = self[((x - 1 + w) % w, (y + 1) % h)]
                p2 = self[((x) % w, (y + 1) % h)]
                p3 = self[((x + 1) % w, (y + 1) % h)]
                p4 = self[((x) % w, (y + 2) % h)]
                color = []
                for i in range(0, 3):
                    c = abs(int((p1[i] + p2[i] + p3[i] - p4[i]) * random.randint(0, 150) / random.randint(50, 600)))
                    color.append(min(c, 0xff))
                color = tuple(color)
                point = (x, y)
                self.buffer[point] = color
    
    def draw(self):
        """ swap out the buffer to see what changed."""
        for point in self.get_points():
            self[point] = self.buffer[point]
    
    def generate(self):
        self.process()
        self.draw()


class FireThree(Surface):
    """
        this pattern displays a fire.
        like of pattern.
        
        based upon: http://lodev.org/cgtutor/fire.html
    """
    def __init__(self):
        """ create a surface and a buffer to keep changes in."""
        Surface.__init__(self, width=matrix_width, height=matrix_height)
        self.buffer = Surface(width=matrix_width, height=matrix_height)
        self.bottom_points = [x for x in range(0, self.width)]
    
    def randomize_bottom(self):
        """
            create a random underground for the fire to rise from.
            do it with hls as described on the fire.html,
            but instead of a palette generate the correct colors right away
        """
        for x in self.bottom_points:
            point = (x, self.height - 1)
            h = random.random()
            s = random.random()
            l = random.random()
            r, g, b = colorsys.hls_to_rgb(h / 4., min(0.5, l * 2), 1.0)
            r, g, b = (int(r * 0xff), int(g * 0xff), int(b * 0xff))
            self.buffer[point] = (r, g, b)

    def process(self):
        self.randomize_bottom()
        """
            for every point check certain points relating to it,
            change the colors acordingly and save te change.
        """
        w, h = self.width, self.height
        for y in range(0, h - 1):
            for x in range(0, w):
                p1 = self[((x - 1 + w) % w, (y + 1) % h)]
                p2 = self[((x) % w, (y + 1) % h)]
                p3 = self[((x + 1) % w, (y + 1) % h)]
                p4 = self[((x) % w, (y + 2) % h)]
                color = []
                for i in range(0, 3):
                    c = abs(int((p1[i] + p2[i] + p3[i] + p4[i]) * random.randint(0, 110) / random.randint(200, 300)))
                    color.append(min(c, 0xff))
                color = tuple(color)
                point = (x, y)
                self.buffer[point] = color
    
    def draw(self):
        """ swap out the buffer to see what changed."""
        for point in self.get_points():
            self[point] = self.buffer[point]
    
    def generate(self):
        self.process()
        self.draw()

class FireTwo(Surface):
    """
        this pattern displays a fire.
        like of pattern.
        
        based upon: http://lodev.org/cgtutor/fire.html
    """
    def __init__(self):
        """ create a surface and a buffer to keep changes in."""
        Surface.__init__(self, width=matrix_width, height=matrix_height)
        self.buffer = Surface(width=matrix_width, height=matrix_height)
        self.bottom_points = [x for x in range(0, self.width)]
    
    def randomize_bottom(self):
        """
            create a random underground for the fire to rise from.
            do it with hls as described on the fire.html,
            but instead of a palette generate the correct colors right away
        """
        for x in self.bottom_points:
            point = (x, self.height - 1)
            h = random.random()
            s = random.random()
            l = random.random()
            r, g, b = colorsys.hls_to_rgb(h / 4., min(0.5, l * 2), 1.0)
            r, g, b = (int(r * 0xff), int(g * 0xff), int(b * 0xff))
            self.buffer[point] = (r, g, b)

    def process(self):
        self.randomize_bottom()
        """
            for every point check certain points relating to it,
            change the colors acordingly and save te change.
        """
        w, h = self.width, self.height
        for y in range(0, h - 1):
            for x in range(0, w):
                p1 = self[((x - 1 + w) % w, (y + 1) % h)]
                p2 = self[((x) % w, (y + 1) % h)]
                p3 = self[((x + 1) % w, (y + 1) % h)]
                p4 = self[((x) % w, (y + 2) % h)]
                color = []
                for i in range(0, 3):
                    c = abs(int((p1[i] + p2[i] + p3[i] + p4[i]) * random.randint(64, 96) / random.randint(300, 400)))
                    color.append(min(c, 0xff))
                color = tuple(color)
                point = (x, y)
                self.buffer[point] = color
    
    def draw(self):
        """ swap out the buffer to see what changed."""
        for point in self.get_points():
            self[point] = self.buffer[point]
    
    def generate(self):
        self.process()
        self.draw()

class FireOne(Surface):
    """
        this pattern displays a fire.
        like of pattern.
        
        based upon: http://lodev.org/cgtutor/fire.html
    """
    def __init__(self):
        """ create a surface and a buffer to keep changes in."""
        Surface.__init__(self, width=matrix_width, height=matrix_height)
        self.buffer = Surface(width=matrix_width, height=matrix_height)
        self.bottom_points = [x for x in range(0, self.width)]
    
    def randomize_bottom(self):
        """
            create a random underground for the fire to rise from.
            do it with hls as described on the fire.html,
            but instead of a palette generate the correct colors right away
        """
        for x in self.bottom_points:
            point = (x, self.height - 1)
            h = random.random()
            s = random.random()
            l = random.random()
            r, g, b = colorsys.hls_to_rgb(h / 4., min(0.5, l * 2), 1.0)
            r, g, b = (int(r * 0xff), int(g * 0xff), int(b * 0xff))
            self.buffer[point] = (r, g, b)

    def process(self):
        self.randomize_bottom()
        """
            for every point check certain points relating to it,
            change the colors acordingly and save te change.
        """
        w, h = self.width, self.height
        for y in range(0, h - 1):
            for x in range(0, w):
                p1 = self[((x - 1 + w) % w, (y + 1) % h)]
                p2 = self[((x) % w, (y + 1) % h)]
                p3 = self[((x + 1) % w, (y + 1) % h)]
                p4 = self[((x) % w, (y + 2) % h)]
                color = []
                for i in range(0, 3):
                    c = abs(int((p1[i] + p2[i] + p3[i] + p4[i]) * 32 / 129))
                    color.append(min(c, 0xff))
                color = tuple(color)
                point = (x, y)
                self.buffer[point] = color
    
    def draw(self):
        """ swap out the buffer to see what changed."""
        for point in self.get_points():
            self[point] = self.buffer[point]
    
    def generate(self):
        self.process()
        self.draw()

class RainPattern(Graphics):
    """
        rain pattern implementation by Duality
        will call 2.0 :D
    """
    def __init__(self, color=(80, 255, 100), chance=0.04):
        Graphics.__init__(self, width=matrix_width, height=matrix_height)
        self.color = color
        self.chance = chance
        # insert single drop for testing
        self.drops = [RainDrop(color)]

    def generate(self):
        self.fill(BLACK)
        # put drop in data and increment it's position
        for drop in self.drops:
            # calculate where to put it
            index = ((drop.y - 1) * matrix_width + drop.x) - 1
            # put drop oN matrix screen
            if index >= 0:
                self.draw_pixel(drop.x, drop.y - 1, drop.color)
            # increment it's height
            drop.incrementHeight()
            # if it falls of the screen remove it.
            if drop.getHeight() > matrix_height:
                self.drops.remove(drop)
        # add a random chance for drops to appear.
        if(random.random() < self.chance):
            raindrop = RainDrop(self.color)
            self.drops.append(raindrop)


# class RainPattern_original:
#     # Falling drops, default color white/blue-ish
#     def __init__(self, color=(100, 255, 100), chance=0.04):
#         # Init empty data list
#         self.color = color
#         self.chance = chance
#         self.data = []
#         for i in xrange(matrix_size):
#             self.data.insert(0, (0, 0, 0))  # black/off

#     def generate(self):
#         # Pop 7 times to move one line down
#         for i in xrange(matrix_width):
#             self.data.pop()
#             if (random.random() < self.chance):  # random chance of raindrop
#                 self.data.insert(0, self.color)
#             else:
#                 self.data.insert(0, (0, 0, 0))  # black/off
#         return self.data
