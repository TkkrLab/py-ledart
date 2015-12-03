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
        indexes = []
        for y in range(0, self.height):
            for x in range(0, self.width):
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

    def __getitem__(self, key):
        if isinstance(key, slice):
            return self.get_list_rep()[key.start:key.stop:key.step]
        else:
            return self.surface[key]

    def __setitem__(self, key, value):
        self.surface[key] = value

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
