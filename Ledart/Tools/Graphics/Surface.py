"""
    this object describes a surface object which has:
    width, height, size
    and points to which you can draw color data.
    like surface[i] or surface[(x, y)]
"""

class Surface(object):
    """ instantiate a new surface or make a copy"""
    def __init__(self, **kwargs):
        surface = kwargs.get('surface', None)
        if surface:
            self.width = int(surface.width)
            self.height = int(surface.height)
            self.d_offset = list(surface.d_offset)
            self.size = int(surface.size)
            self.color_rep = list(surface.color_rep)
            self.color_depth = int(surface.color_depth)
            self.indexes = dict(surface.indexes)
            self.surface = list(surface.surface)
        else:
            dims = kwargs.get('dims', [0, 0, 1, 1])
            x, y, self.width, self.height = dims
            self.d_offset = (x, y)

            self.size = self.width * self.height

            self.color_rep = [0, 0, 0]
            self.color_depth = 0xff

            """ map for points (x, y) to index int(index) """
            self.indexes = self.gen_indexes()
            """ empty list for the colors """
            self.surface = self.gen_surface()

    """ return a list of default, which if none is self.color_rep """
    def gen_surface(self, default=None):
        if default == None:
            default = self.color_rep

        return [default for i in range(self.size)]

    """ returns a dictionary that is a map of points (x, y) to indexes int(index)"""
    def gen_indexes(self):
        indexes = {}
        p = 0
        for y in range(0, self.height):
            for x in range(0, self.width):
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

    def close(self):
        pass

    def flatten(self):
        flattend_list = []
        for color in self:
            for c in color:
                flattend_list.append(c)
        return flattend_list

    """ allow to get/set value by point (x, y) or by index int(index) """
    def __getitem__(self, key):
        if type(key) == int:
            return self.surface[key]
        elif type(key) == slice:
            return self.surface[key.start:key.stop:key.step]
        elif type(key) == list:
            index = self.indexes[key]
            return self.surface[index]
        elif type(key) == tuple:
            index = self.indexes[key]
            return self.surface[index]
        else:
            raise(KeyError)

    def __setitem__(self, key, value):
        if type(value) != list:
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

    """ basic Surface representation and info. """
    def __repr__(self):
        fmtstr = "<Surface width=%d, height=%d, [%s, ... %s]>"
        fmt = (self.width, self.height,
               self.surface[0], self.surface[-1])
        return (fmtstr % fmt)

