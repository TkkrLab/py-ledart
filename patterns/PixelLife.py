from Tools.Graphics import Graphics, BLUE, BLACK, GREEN, RED, COLORS
from Tools.Graphics import ColorRGBOps
from matrix import matrix_width, matrix_height, to_matrix
from Life.life import Life
import random

selected = 'BlueLife'


class RandomLife(Graphics):
    def __init__(self):
        Graphics.__init__(self, matrix_width, matrix_height)
        self.life = Life(matrix_width, matrix_height, 1, color=BLACK)

    def pickRandomColor(self):
        color = random.randint(0, len(COLORS) - 1)
        # make sure that that color isn't black
        while(COLORS[color] == BLACK):
            color = random.randint(0, len(COLORS) - 1)
        return COLORS[color]

    def drawRandomColor(self):
        self.fill(BLACK)
        life_matrix = to_matrix(self.life.field, self.life.fieldWidth)
        for point in self.get_points():
                x, y = point
                if life_matrix[y][x]:
                    self.draw_pixel(x, y, self.pickRandomColor())

    def draw(self):
        self.drawRandomColor()

    def generate(self):
        self.life.process()
        self.draw()


class GreenLife(Graphics):
    def __init__(self):
        Graphics.__init__(self, matrix_width, matrix_height)
        self.life = Life(matrix_width, matrix_height, 1, color=GREEN)

    def draw(self):
        self.fill(BLACK)
        life_matrix = to_matrix(self.life.field, self.life.fieldWidth)
        for point in self.get_points():
                x, y = point
                if life_matrix[y][x]:
                    color = GREEN
                    self.draw_pixel(x, y, color)

    def generate(self):
        self.life.process()
        self.draw()


class BlueLife(Graphics):
    def __init__(self):
        Graphics.__init__(self, matrix_width, matrix_height)
        self.life = Life(matrix_width, matrix_height, 1, color=BLUE)

    def draw(self):
        self.fill(BLACK)
        life_matrix = to_matrix(self.life.field, self.life.fieldWidth)
        for point in self.get_points():
                x, y = point
                if life_matrix[y][x]:
                    color = BLUE
                    self.draw_pixel(x, y, color)

    def generate(self):
        self.life.process()
        self.draw()


class RedLife(Graphics):
    def __init__(self):
        Graphics.__init__(self, matrix_width, matrix_height)
        self.life = Life(matrix_width, matrix_height, 1, color=RED)

    def draw(self):
        self.fill(BLACK)
        life_matrix = to_matrix(self.life.field, self.life.fieldWidth)
        for point in self.get_points():
                x, y = point
                if life_matrix[y][x]:
                    color = RED
                    self.draw_pixel(x, y, color)

    def generate(self):
        self.life.process()
        self.draw()


class GrayedLife(Graphics):
    '''
    take the gray scales over every point and
    add or subtract depening on if alive or not
    '''
    def __init__(self):
        Graphics.__init__(self, matrix_width, matrix_height)
        self.fill(BLACK)

    def generate(self):
        pass


class MixedLife(Graphics):
    def __init__(self):
        Graphics.__init__(self, matrix_width, matrix_height)

        blue = ColorRGBOps.darken(BLUE, 128)
        green = ColorRGBOps.darken(GREEN, 128)
        red = ColorRGBOps.darken(RED, 128)

        self.life1 = Life(matrix_width, matrix_height, 1, color=blue)
        self.life2 = Life(matrix_width, matrix_height, 1, color=green)
        self.life3 = Life(matrix_width, matrix_height, 1, color=red)

        self.index = 0
    """
    this draw function manipulates the graphics surface directly.
    it's either elegent in one way.
    and really really ugly in another way.
    """
    def drawThreeAdded(self):
        pass
        # for index, cell in enumerate(self.life1.field):
        #   color = self.graphics.surface[index]
        #   if cell:
        #       color = ColorRGBOps.add(color, self.life1.cellColor)
        #   else:
        #       color = ColorRGBOps.subtract(color, BLUE)
        #   self.graphics.surface[index] = color

        # for index, cell in enumerate(self.life2.field):
        #   color = self.graphics.surface[index]
        #   if cell:
        #       color = ColorRGBOps.add(color, self.life2.cellColor)
        #   else:
        #       color = ColorRGBOps.subtract(color, GREEN)
        #   self.graphics.surface[index] = color

        # for index, cell in enumerate(self.life3.field):
        #   color = self.graphics.surface[index]
        #   if cell:
        #       color = ColorRGBOps.add(color, self.life3.cellColor)
        #   else:
        #       color = ColorRGBOps.subtract(color, RED)
        #   self.graphics.surface[index] = color
    def draw(self):
        self.drawThreeAdded()

    def generate(self):
        self.life1.process()
        self.life2.process()
        self.life3.process()
        self.draw()
