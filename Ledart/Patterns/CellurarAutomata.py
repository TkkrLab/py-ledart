from Ledart.Tools.Graphics import Graphics, BLUE, BLACK, WHITE
from Ledart.stripinfo import strip_width, strip_height
from Ledart.Tools.Timing import Timer
import random
import time

class CaTest(Graphics):
    def __init__(self, scrolling=True, refresh_time=6.0, scroll_time=0.06):
        Graphics.__init__(self, width=strip_width, height=strip_height)
        self.rule = random.randint(0, 0xff)
        self.color = BLUE
        self.hpos = 1
        self.height_range = range(1, self.height)
        self.scrolling = scrolling
        # self.create_random_row(0)
        self.draw_pixel(0, 0, self.color)
        self.refresh_timer = Timer(refresh_time)
        self.scroll_timer = Timer(scroll_time)

    def create_random_row(self, row):
        for x in range(0, self.width):
            r, g, b = 0, 0, random.randrange(0, 2) * 0xFF
            self[x, row] = [r, g, b]

    def create_row(self, row):
        for x in range(0, self.width):
            self[x, row] = self.color

    def count(self, x, row):
        c = 0
        row = row - 1
        top_opts = (-1, 0, 1)
        for i, xp in enumerate(top_opts):
            xp = (x + xp + self.width) % self.width
            if self[xp, row] != BLACK:
                c += 1 << i
        return c

    def apply_rule(self, rule, row):
        for x in range(0, self.width):
            c = self.count(x, row)
            if (1 << c) & rule:
                self.draw_pixel(x, row, self.color)
            else:
                self.draw_pixel(x, row, BLACK)

    def generate_scrolling(self):
        if self.scroll_timer.valid():
            self.apply_rule(self.rule, self.hpos)
            self.hpos += 1
            if self.hpos > (self.height - 1):
                self.hpos = 1
                self.create_random_row(0)
                self.rule = random.randint(0, 0xff)

    def generate_whole(self):
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
