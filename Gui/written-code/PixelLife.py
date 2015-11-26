from Tools.Graphics import Graphics, BLUE, BLACK, GREEN, RED, COLORS
# from Graphics.RGBColorTools import ColorRGBOps
from matrix import matrix_width, matrix_height
from patterns.Life.life import Life
import random

select = "BlueLife"

class RandomLife(object):
    def __init__(self):
        self.life = Life(matrix_width, matrix_height, 1, color=BLACK)
        self.graphics = Graphics(matrix_width, matrix_height)

    def pickRandomColor(self):
        color = random.randint(0, len(COLORS) - 1)
        # make sure that that color isn't black
        while(COLORS[color] == BLACK):
            color = random.randint(0, len(COLORS) - 1)
        return COLORS[color]

    def drawRandomColor(self):
        life_matrix = self.graphics.toMatrix(self.life.field,
                                             self.graphics.getSurfaceWidth())
        for y in self.graphics.heightRange:
            for x in self.graphics.widthRange:
                if life_matrix[y][x]:
                    color = self.pickRandomColor()
                    # give every lifing cell a random color
                    self.graphics.drawPixel(x, y, color)
                else:
                    self.graphics.drawPixel(x, y, BLACK)

    def draw(self):
        self.drawRandomColor()

    def generate(self):
        self.life.process()
        self.draw()
        return self.graphics.getSurface()


class MixedLife(object):
    def __init__(self):
        self.life = Life(matrix_width, matrix_height, 1, color=GREEN)
        self.graphics = Graphics(matrix_width, matrix_height)
        self.graphics.fill(BLACK)

    def draw(self):
        life_matrix = self.graphics.toMatrix(self.life.field, self.graphics.getSurfaceWidth())
        for y in self.graphics.heightRange:
            for x in self.graphics.widthRange:
                if life_matrix[y][x]:
                    color = GREEN
                else:
                    color = BLACK
                self.graphics.drawPixel(x, y, color)

    def generate(self):
        self.life.process()
        self.draw()
        return self.graphics.getSurface()


class BlueLife(object):
    def __init__(self):
        self.life = Life(matrix_width, matrix_height, 1, color=BLUE)
        self.graphics = Graphics(matrix_width, matrix_height)

    def draw(self):
        life_matrix = self.graphics.toMatrix(self.life.field, self.graphics.getSurfaceWidth())
        for y in self.graphics.heightRange:
            for x in self.graphics.widthRange:
                if life_matrix[y][x]:
                    color = BLUE
                else:
                    color = BLACK
                self.graphics.drawPixel(x, y, color)

    def generate(self):
        self.life.process()
        self.draw()
        return self.graphics.getSurface()


class GrayedLife(object):
    '''
    take the gray scales over every point and
    add or subtract depening on if alive or not
    '''
    def __init__(self):
        self.graphics = Graphics(matrix_width, matrix_height)
        self.graphics.fill(BLUE)

    def generate(self):
        return self.graphics.getSurface()
