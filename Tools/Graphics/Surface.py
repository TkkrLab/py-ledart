"""
    this object describes a surface object which has:
    width, height, size
    and points to which you can draw color data.
    like surface[i] or surface[(x, y)]
"""

class Surface(object):
    """ instantiate a new surface or make a copy"""
    def __init__(self, surface=None, **kwargs):
        if surface:
            self.width = int(surface.width)
            self.height = int(surface.height)
            self.d_offset = tuple(surface.d_offset)
            self.size = int(surface.size)
            self.color_rep = tuple(surface.color_rep)
            self.color_depth = int(surface.color_depth)
            self.indexes = dict(surface.indexes)
            self.surface = list(surface.surface)
        else:
            self.width = kwargs.get('width', 1)
            self.height = kwargs.get('height', 1)
            self.d_offset = kwargs.get('offset', (0, 0))

            self.size = self.width * self.height
            self.color_rep = (0, 0, 0)
            self.color_depth = 0xff

            """ map for points (x, y) to index int(index) """
            self.indexes = self.gen_indexes()
            """ empty list for the colors """
            self.surface = self.gen_surface()

    """ return a list of default, which if none is self.color_rep """
    def gen_surface(self, default=None):
        if default == None:
            default = self.color_rep

        return [default for i in xrange(self.size)]

    """ returns a dictionary that is a map of points (x, y) to indexes int(index)"""
    def gen_indexes(self):
        indexes = {}
        p = 0
        for y in xrange(0, self.height):
            for x in xrange(0, self.width):
                pos = (x, y)
                indexes[pos] = p
                p += 1

        return indexes

    """ getter setter functions. """
    def get_size(self):
        return self.size

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_points(self):
        return self.indexes

    def set_d_offset(self, pos):
        self.d_offset = pos

    def get_d_offset(self):
        return self.d_offset

    """ allow to get/set value by point (x, y) or by index int(index) """
    def __getitem__(self, key):
        if type(key) == int:
            return self.surface[key]
        elif type(key) == slice:
            return self.surface[key.start:key.stop:key.step]
        elif type(key) == tuple:
            index = self.indexes[key]
            return self.surface[index]
        else:
            raise(KeyError)

    def __setitem__(self, key, value):
        if type(value) != tuple:
            raise(ValueError)

        if type(key) == int:
            self.surface[key] = value
        elif type(key) == tuple:
            index = self.indexes[key]
            self.surface[index] = value
        else:
            raise(KeyError)

    def __len__(self):
        return self.size

    """ function returns a list of bytes. """
    def __bytes__(self):
        __str = [chr(c) for color in self.surface for c in color]
        return bytearray(__str)

    """ function returns a list of bytes. (python2.7 strings) """
    def __str__(self):
        __str = [chr(c) for color in self.surface for c in color]
        return ''.join(__str)

    """ basic Surface representation and info. """
    def __repr__(self):
        fmtstr = "<Surface width=%d, height=%d, [%s, ... %s]>"
        fmt = (self.width, self.height,
               self.surface[0], self.surface[-1])
        return (fmtstr % fmt)

