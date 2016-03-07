"""
    this file descibes surface types.
"""

from PIL import Image


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

    """
        setting and getting display offsets.
        these are in surface because a surface can have a offset.
    """
    def set_d_offset(self, pos):
        self.d_offset = pos

    def get_d_offset(self):
        return self.d_offset

    def __getitem__(self, key):
        if type(key) == int:
            point = self.indexes[key]
            return self.surface[point]
        elif isinstance(key, slice):
            return self.get_list_rep()[key.start:key.stop:key.step]
        else:
            return self.surface[key]

    def __setitem__(self, key, value):
        self.surface[key] = value

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


class ImageSurface(Surface):
    def __init__(self, width, height, fname, thumbnail=False):
        self.image = Image.open(fname)
        self.imtype = self.determine_type(fname)
        if self.imtype is None:
            raise(Exception("Couldn't load image."))

        if (self.image.width > width) or (self.image.height > height):
            if thumbnail:
                self.image.thumbnail((width, height))
            else:
                self.image = self.image.resize((width, height))

        # create the surface to draw the image on.
        Surface.__init__(self, width=self.image.width,
                         height=self.image.height)

        if self.imtype == "png":
            self.load_png(self.image)
        elif self.imtype == "jpg":
            self.load_jpg(self.image)

    def determine_type(self, image):
        png = ["png"]
        jpg = ["jpg", "jpeg"]

        imtype = None
        for n in png:
            if n in image.lower():
                imtype = "png"
        for n in jpg:
            if n in image.lower():
                imtype = "jpg"
        return imtype

    def load_jpg(self, image, invert=False):
        imdata = self.image.getdata()

        for i, point in enumerate(self.get_points()):
            if len(imdata[i]) == 3:
                color = imdata[i]
            else:
                raise(Exception("No valid image data found"))
            self[point] = color

    def load_png(self, image, invert=False):
        imdata = self.image.getdata()
        p = 0
        for y in range(0, self.image.height):
            for x in range(0, self.image.width):
                point = (x, y)
                if len(imdata[p]) == 3:
                    color = imdata[p]
                elif len(imdata[p]) == 4:
                    pass
                    r, g, b, alpha = imdata[p]
                    color = (alpha, alpha, alpha)
                if invert:
                    r, g, b = color
                    color = (0xff - r, 0xff - g, 0xff - b)
                self[point] = color
                p += 1
