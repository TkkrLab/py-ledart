from Ledart.Tools.Graphics import Graphics, WHITE, BLUE, BLACK, GREEN, RED, COLORS
from Ledart.Tools.Graphics import ColorRGBOps
from Ledart.utils import to_matrix
from Life.life import Life
import random
import colorsys


class RandomLife(Graphics):
    def __init__(self, **kwargs):
        Graphics.__init__(self, **kwargs)
        self.life = Life(self.width, self.height, 1, color=BLACK)

    def pickRandomColor(self):
        color = random.randint(0, len(COLORS) - 1)
        # make sure that that color isn't black
        while(COLORS[color] == BLACK):
            color = random.randint(0, len(COLORS) - 1)
        return COLORS[color]

    def drawRandomColor(self):
        self.fill(BLACK)
        life_strip = to_matrix(self.life.field, self.life.fieldWidth)
        for point in self.get_points():
                x, y = point
                if life_strip[y][x]:
                    self.draw_pixel(x, y, self.pickRandomColor())

    def draw(self):
        self.drawRandomColor()

    def generate(self):
        self.life.process()
        self.draw()


class PixelLife(Graphics):
    def __init__(self, **kwargs):
        Graphics.__init__(self, **kwargs)
        self.life = Life(self.width, self.height, 1)
        self.color = kwargs.get('color', BLUE)

    def draw(self):
        self.fill(BLACK)
        life_strip = to_matrix(self.life.field, self.life.fieldWidth)
        for point in self.get_points():
                x, y = point
                if life_strip[y][x]:
                    self.draw_pixel(x, y, self.color)

    def generate(self):
        self.life.process()
        self.draw()


class ProgressedLife(Graphics):
    '''
    brighten spots with prolonged cell life,
    while darken spots where there is less cell life
    '''
    def __init__(self, **kwargs):
        Graphics.__init__(self, **kwargs)
        self.life = Life(self.width, self.height, 1, WHITE)
        self.step = kwargs.get('decay', 4)
        self.color_step = (self.step, self.step, self.step)
        self.fill(WHITE)

    def draw(self):
        for i, point in enumerate(self.get_points()):
            color = self[point]
            if self.life.field[i]:
                color = ColorRGBOps.brighten(color, self.step)
            else:
                color = ColorRGBOps.darken(color, self.step)
            self[point] = color

    def generate(self):
        self.life.process()
        self.draw()

class CProgressedLife(Graphics):
    '''
    brighten spots with prolonged cell life,
    while darken spots where there is less cell life
    and color it accordingly 
    '''
    def __init__(self, **kwargs):
        Graphics.__init__(self, **kwargs)
        self.background = Graphics(**kwargs)

        self.life = Life(self.width, self.height, 1, WHITE)
        self.step = kwargs.get('decay', 4)
        self.color_step = (self.step, self.step, self.step)
        
        self.fill(WHITE)

    def draw(self):
        for i, point in enumerate(self.background.get_points()):
            color = self.background[point]
            if self.life.field[i]:
                color = ColorRGBOps.brighten(color, self.step)
            else:
                color = ColorRGBOps.darken(color, self.step)
            self.background[point] = color
            shade = color[0] / 256.
            color = [int(c * 0xff) for c in colorsys.hsv_to_rgb(1 - shade, 1, shade)]
            self[point] = color

    def generate(self):
        self.life.process()
        self.draw()

class MixedLife(Graphics):
    def __init__(self, **kwargs):
        Graphics.__init__(self, **kwargs)

        blue = ColorRGBOps.darken(BLUE, 128)
        green = ColorRGBOps.darken(GREEN, 128)
        red = ColorRGBOps.darken(RED, 128)

        self.life1 = Life(self.width, self.height, 1, color=BLUE)
        self.life2 = Life(self.width, self.height, 1, color=green)
        self.life3 = Life(self.width, self.height, 1, color=red)

        self.step = int(0xff/10)

        self.step_red = (self.step, 0, 0)
        self.step_green = (0, self.step, 0)
        self.step_blue = (0, 0, self.step)

        self.index = 0
    """
    this draw function manipulates the graphics surface directly.
    it's either elegent in one way.
    and really really ugly in another way.
    """
    def drawThreeAdded(self):
        points = self.get_points()
        for i, point in enumerate(points):
            color = self[point]
            # check for first life field.
            if self.life1.field[i]:
                color = ColorRGBOps.add(color, self.step_blue)
            else:
                color = ColorRGBOps.subtract(color, self.step_blue)
            # check seconds
            if self.life2.field[i]:
                color = ColorRGBOps.add(color, self.step_green)
            else:
                color = ColorRGBOps.subtract(color, self.step_green)
            # check third
            if self.life3.field[i]:
                color = ColorRGBOps.add(color, self.step_red)
            else:
                color = ColorRGBOps.subtract(color, self.step_red)
            
            self[point] = color
    def draw(self):
        self.drawThreeAdded()

    def generate(self):
        self.life1.process()
        self.life2.process()
        self.life3.process()
        self.draw()

