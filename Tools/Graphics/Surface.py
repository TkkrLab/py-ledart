"""
    this file descibes surface types.
"""
from operator import itemgetter

class Surface(object):
    def __init__(self, surface=None, **kwargs):
        if surface:
            self.width = int(surface.width)
            self.height = int(surface.height)
            self.d_offset = tuple(surface.d_offset)
            self.size = int(surface.size)
            self.color_rep = tuple(surface.color_rep)
            self.color_depth = int(surface.color_depth)
            self.indexes = list(surface.indexes)
            self.surface = dict(surface.surface)
        else:
            self.width = kwargs.get('width', 1)
            self.height = kwargs.get('height', 1)
            self.d_offset = kwargs.get('offset', (0, 0))
            self.size = self.width * self.height
            # represent r, g, b can be set of needed.
            self.color_rep = (0, 0, 0)
            # represent the max value a color can be.
            self.color_depth = 0xff
            # represent the indexes as x, y. for x, y, z
            # you could set the pos_rep to 3
            self.indexes = self.gen_indexes()
            self.surface = self.gen_surface()

    """
        generate a dictionary as surface that has,
        positional keys, and pixel data as value.
    """
    def gen_surface(self, default=None):
        if default:
            value = default
        else:
            value = self.color_rep

        surface = {}
        for index in self.indexes:
            surface[index] = value
        return surface

    """
        generate a list of x, y pairs that correspond to
        positional values.
    """
    def gen_indexes(self):
<<<<<<< HEAD
        indexes = []
        for y in range(0, self.height):
            for x in range(0, self.width):
=======
        indexes = {}
        p = 0
        for y in xrange(0, self.height):
            for x in xrange(0, self.width):
>>>>>>> newsurfaceimp
                pos = (x, y)
                indexes.append(pos)
        return indexes

    """
        getter method's.
        for getting the surface atributes.
    """
    def get_size(self):
        return self.size

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_points(self):
        return self.indexes

    def get_list_rep(self):
        surface_list = []
        for index in self.indexes:
            surface_list.append(self.surface[index])
        return surface_list

    """
        setting and getting display offsets.
        these are in surface because a surface can have a offset.
    """
    def set_d_offset(self, pos):
        self.d_offset = pos

    def get_d_offset(self):
        return self.d_offset

    def __getitem__(self, key):
<<<<<<< HEAD
        if isinstance(key, int):
            point = self.indexes[key]
            return self.surface[point]
        elif isinstance(key, slice):
            return self.get_list_rep()[key.start:key.stop:key.step]
        elif isinstance(key, tuple):
            return self.surface[key]
=======
        if type(key) == int:
            return self.surface[key]
        elif type(key) == slice:
            return self.surface[key.start:key.stop:key.step]
        elif type(key) == tuple:
            index = self.indexes[key]
            return self.surface[index]
>>>>>>> newsurfaceimp
        else:
            raise(KeyError)

    def __setitem__(self, key, value):
<<<<<<< HEAD
        if isinstance(key, int):
=======
        if type(value) != tuple:
            raise(ValueError)

        if type(key) == int:
            self.surface[key] = value
        elif type(key) == tuple:
>>>>>>> newsurfaceimp
            index = self.indexes[key]
            self.surface[index] = value
            # print("index, key, value", index, key, value)
        elif isinstance(key, tuple):
            self.surface[key] = value
        else:
            print("unknown type(key: %s)" % (str(type(key))))
            raise("unknown type(key: %s)" % (str(type(key))))

    def __eq__(self, other):
        if self.size != other.size:
            return False
        for index in self.indexes:
            if other[index] != self.surface[index]:
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __len__(self):
        return len(self.indexes)

    def __str__(self):
        data = ''
        indexes = self.gen_indexes()
        for index in indexes:
            color = self.surface[index]
            for c in color:
                data += chr(c)
        return data

    def __repr__(self):
        return str(dict(self.surface))
