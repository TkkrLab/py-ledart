from Ledart.Tools.Graphics import Graphics, BLUE, BLACK, WHITE
from Ledart.stripinfo import strip_width, strip_height
from Ledart.Tools.Timing import Timer
import random
import time

class Ca(Graphics):
    def __init__(self, **kwargs):
        Graphics.__init__(self, width=strip_width, height=strip_height)
        self.rule = kwargs.get("rule", random.randint(0, 0xff))
        self.scrolling = kwargs.get("scrolling", True)
        self.refresh_time = kwargs.get("refreshtime", 6.0)
        self.color = kwargs.get("color", BLUE)

        # start scan at second line. since we scan what's above it.
        self.hpos = 1
        self.height_range = range(1, self.height)
        # seed first line
        self.create_random_row(0)
        # timer for refreshing the screen.
        self.refresh_timer = Timer(self.refresh_time)

    def create_random_row(self, row):
        """ creates a row of random pixels at <row> """
        for x in range(0, self.width):
            r, g, b = 0, 0, random.randrange(0, 2) * 0xFF
            self[x, row] = [r, g, b]

    def count(self, x, row):
        """ counts cells above a cell at <x> on row <row> """
        count = 0
        row = row - 1
        # cell offsets
        top_opts = (-1, 0, 1)
        for i, xp in enumerate(top_opts):
            xp = (x + xp + self.width) % self.width
            # binary counting for top cells.
            if self[xp, row] != BLACK:
                count += 1 << i
        return count

    def apply_rule(self, rule, row):
        """ transforms cell depending on <rule> and on <row>"""
        for x in range(0, self.width):
            c = self.count(x, row)
            if (1 << c) & rule:
                self.draw_pixel(x, row, self.color)
            else:
                self.draw_pixel(x, row, BLACK)

    def generate_scrolling(self):
        """ displays the picuture as it's generated. """
        self.apply_rule(self.rule, self.hpos)
        self.hpos += 1
        if self.hpos > self.height:
            self.hpos = 1
            self.fill(BLACK)
            self.create_random_row(0)
            self.rule = random.randint(0, 0xff)

    def generate_whole(self):
        """ generates a whole picture and then displays it. """
        if self.refresh_timer.valid():
            self.rule = random.randint(0, 0xff)
            self.create_random_row(0)
            for i in range(1, self.height):
                self.apply_rule(self.rule, i)

    def generate(self):
        if self.scrolling:
            self.generate_scrolling()
        elif not self.scrolling:
            self.generate_whole()
