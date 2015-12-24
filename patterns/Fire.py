"""
    author: Duality
    pattern: Fire
    creates fire like patterns or smolderings.

    inspiration:
    http://lodev.org/cgtutor/fire.html
"""

from Tools.Graphics import Surface
from matrix import matrix_width, matrix_height
import random
import colorsys

select = 'AliasedWPlasma'


def xfrange(start, stop, step):
    while start < stop:
        yield start
        start += step


class MiniFire(Surface):
    """
        this pattern displays a fire.
        like of pattern.
        based upon: http://lodev.org/cgtutor/fire.html
        this effect works well on smaller matrices.
    """
    def __init__(self, width=matrix_width, height=matrix_height):
        """ create a surface and a buffer to keep changes in."""
        Surface.__init__(self, width=width, height=height)
        self.buffer = Surface(width=width, height=height)
        self.bottom_points = [x for x in range(0, self.width)]
        # self.bottom_points = [random.randint(0, self.width) for x in range(0, self.width)]

    def randomize_bottom(self):
        """
            create a random underground for the fire to rise from.
            do it with hls as described on the fire.html,
            but instead of a palette, generate the correct colors right away
        """
        for x in self.bottom_points:
            point = (x, self.height - 1)
            h = random.random()
            s = 1.0
            l = random.random()
            r, g, b = colorsys.hls_to_rgb(h / 7, min(0.5, l * 2), s)
            r, g, b = (int(r * 0xff), int(g * 0xff / 8), int(b * 0xff))
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
                    c = abs(int((p1[i] + p2[i] + p3[i] - p4[i]) *
                                random.randint(0, 200) /
                                random.randint(50, 600)))
                    if c < 100:
                        c = 0
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


class AliasedFire(Surface):
    def __init__(self):
        Surface.__init__(self, width=matrix_width, height=matrix_height)
        self.fire = MiniFire(self.width*2, self.height*2)

    def generate(self):
        self.fire.generate()
        for y in range(0, self.fire.height, 2):
            for x in range(0, self.fire.width, 2):
                point_self = (x/2, y/2)
                c1 = self.fire[(x/2, y/2)]
                c2 = self.fire[(x/2 + 1, y/2)]
                c3 = self.fire[(x/2, y/2 + 1)]
                c4 = self.fire[(x/2 + 1, y/2 + 1)]
                r = (c1[0] + c2[0] + c3[0] + c4[0]) / 4
                g = (c1[1] + c2[1] + c3[1] + c4[1]) / 4
                b = (c1[2] + c2[2] + c3[2] + c4[2]) / 4
                color = (r, g, b)
                self[point_self] = color


class WeirdPlasmaLike(Surface):
    """
        this pattern displays a fire.
        like of pattern.
        based upon: http://lodev.org/cgtutor/fire.html
        this effect works well on smaller matrices.
    """
    def __init__(self, width=matrix_width, height=matrix_height):
        """ create a surface and a buffer to keep changes in."""
        Surface.__init__(self, width=width, height=height)
        self.buffer = Surface(width=width, height=height)
        self.bottom_points = range(0, self.width)
        # self.bottom_points = [random.randint(0, self.width) for x in range(0, self.width)]
        self.randomize_bottom()

    def randomize_bottom(self):
        """
            create a random underground for the fire to rise from.
            do it with hls as described on the fire.html,
            but instead of a palette, generate the correct colors right away
        """
        for x in self.bottom_points:
            point = (x, self.height - 1)
            h = random.random()
            s = 0.8
            l = random.random()
            r, g, b = colorsys.hls_to_rgb(h * 0.33 , min(1.0, l * 2), s)
            r, g, b = (int(r * 0xff), int(g * 0xff), int(b * 0xff))
            self.buffer[point] = (r, g, b)

    def process(self):
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
                    c = abs(int(p1[i] - p2[i] + p3[i] + p4[i]) * 31 / 80)
                    color.append(min(c, 0xff))
                color = tuple(color)
                point = (x, y)
                self.buffer[point] = color
        self.randomize_bottom()

    def draw(self):
        """ swap out the buffer to see what changed."""
        for point in self.get_points():
            self[point] = self.buffer[point]

    def generate(self):
        self.process()
        self.draw()


class AliasedWPlasma(Surface):
    def __init__(self):
        Surface.__init__(self, width=matrix_width, height=matrix_height)
        self.effect = WeirdPlasmaLike(self.width * 2, self.height * 2)

    def generate(self):
        self.effect.generate()
        for y in range(0, self.effect.height, 2):
            for x in range(0, self.effect.width, 2):
                point_self = (x / 2, y / 2)
                c1 = self.effect[(x / 2, y / 2)]
                c2 = self.effect[(x / 2 + 1, y / 2)]
                c3 = self.effect[(x / 2, y / 2 + 1)]
                c4 = self.effect[(x / 2 + 1, y / 2 + 1)]
                r = (c1[0] + c2[0] + c3[0] + c4[0]) / 4
                g = (c1[1] + c2[1] + c3[1] + c4[1]) / 4
                b = (c1[2] + c2[2] + c3[2] + c4[2]) / 4
                color = (r, g, b)
                self[point_self] = color


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
            r, g, b = colorsys.hls_to_rgb(h / 3.5, min(0.5, l * 2), s)
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
                    c = abs(int((p1[i] + p2[i] + p3[i] - p4[i]) *
                                random.randint(0, 150) /
                                random.randint(50, 600)))
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
                p4 = self[((x) % w, (y + 1) % h)]
                color = []
                for i in range(0, 3):
                    c = abs(int((p1[i] + p2[i] + p3[i] + p4[i]) *
                                random.randint(0, 110) /
                                random.randint(200, 300)))
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
                    c = abs(int((p1[i] + p2[i] + p3[i] + p4[i]) *
                                random.randint(64, 96) /
                                random.randint(300, 400)))
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
            s = 1.0
            l = random.random()
            r, g, b = colorsys.hls_to_rgb(h / 4., min(0.5, l * 2), s)
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
                p4 = self[((x) % w, (y + 1) % h)]
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
