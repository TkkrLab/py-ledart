from Ledart.Tools.Graphics import Graphics, BLACK, RED, BLUE, GREEN
from Ledart.Tools.Controllers import PygameController, XboxController
from Ledart.matrix import matrix_width, matrix_height, matrix_size

c = BLACK
r = RED
g = GREEN
b = BLUE

level1 = [c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c,
          c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c,
          c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c,
          c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c,
          c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c, c,
          g, g, g, g, g, g, g, g, g, g, g, g, g, g, g, g, g,
          g, g, g, g, g, g, g, g, g, g, g, g, g, g, g, g, g,
          g, g, g, g, g, g, g, g, g, g, g, g, g, g, g, g, g,
          g, g, g, g, g, g, g, g, g, g, g, g, g, g, g, g, g,
          g, g, g, g, g, g, g, g, g, g, g, g, g, g, g, g, g]

level = [BLUE] * matrix_size


class PixelBrosController(PygameController, XboxController):
    def __init__(self, plugged=0):
        PygameController.__init__(self, plugged)

    def getDpad(self, button):
        return PygameController.getButtons(self, button)


class TilePixel(object):
    """Tile class holds info on individual Tiles"""
    def __init__(self, pos, color, game):
        self.color = color
        self.game = game
        self.pos = (pos[1], pos[0])

    def draw(self):
        x, y = self.pos
        self.game.draw_pixel(self.game.get_width() - x - 1, y, self.color)

    def setPos(self, pos):
        self.pos = (pos[1], pos[0])

    def getPos(self):
        return (self.pos[1], self.pos[0])


class Player(TilePixel):
    """Player class handles how to player acts."""
    def __init__(self, pos, color, game):
        TilePixel.__init__(self, pos, color, game)
        self.controller = PixelBrosController(0)
        self.game = game
        self.dx = 0
        self.dy = 0

    def handleInput(self):
        if self.controller.getDpad(self.controller.UP_DPAD):
            self.dy = -1
        elif self.controller.getDpad(self.controller.DOWN_DPAD):
            self.dy = 1
        else:
            self.dy = 0

        if self.controller.getDpad(self.controller.LEFT_DPAD):
            self.dx = -1
        elif self.controller.getDpad(self.controller.RIGHT_DPAD):
            self.dx = 1
        else:
            self.dx = 0

    def process(self):
        x, y = self.getPos()
        y += self.dy
        x += self.dx
        pos = x, y
        self.setPos(pos)


class SuperPixelBros(Graphics):
    """
    SuperPixelBros is a class that hanles function calling and processing.
    makes sure the level is generated.
    makes sure the player get the right data.

    """
    def __init__(self):
        Graphics.__init__(self, matrix_width, matrix_height)

        self.players = []
        self.player = Player((9, 7), BLUE, self)

        self.level = level1

    def handleInput(self):
        self.player.handleInput()

    def process(self):
        self.player.process()

    def draw(self):
        self.fill(BLACK)
        # draw the map.
        surfaceheight = self.get_height()
        level_matrix = self.toMatrix(self.level, surfaceheight)
        for y in range(0, self.get_height()):
            for x in range(0, self.get_width()):
                tile = level_matrix[x][y]
                # draw the map flipped
                self.draw_pixel(self.get_width() - x - 1, y, tile)

        # draw the player.
        self.player.draw()

    def generate(self):
        # self.handleInput()
        # self.process()
        # self.draw()
        pass
