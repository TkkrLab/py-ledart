from Tools.Graphics import Graphics, WHITE, BLUE, BLACK, GREEN, RED, COLORS
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


class ProgressedLife(Graphics):
    '''
    brighten spots with prolonged cell life,
    while darken spots where there is less cell life
    '''
    def __init__(self, decay=4):
        Graphics.__init__(self, matrix_width, matrix_height)
        self.life = Life(matrix_width, matrix_height, 1, WHITE)
        self.step = decay
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


class MixedLife(Graphics):
    def __init__(self):
        Graphics.__init__(self, matrix_width, matrix_height)

        blue = ColorRGBOps.darken(BLUE, 128)
        green = ColorRGBOps.darken(GREEN, 128)
        red = ColorRGBOps.darken(RED, 128)

        self.life1 = Life(matrix_width, matrix_height, 1, color=BLUE)
        self.life2 = Life(matrix_width, matrix_height, 1, color=green)
        self.life3 = Life(matrix_width, matrix_height, 1, color=red)

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

