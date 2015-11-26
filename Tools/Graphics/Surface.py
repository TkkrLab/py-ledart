class Surface(object):
    def __init__(self, surface=None, width=None, height=None):
        if surface:
            pass
        if width and height:
            self.width = width
            self.height = height
            self.size = self.width * self.height
            self.color_rep = (0, )
            self.color_depth = 0x7f
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


def main():
    from ledboard import netcon

    ledboard_width, ledboard_height = 96, 48
    ledboard = Surface(width=ledboard_width, height=ledboard_height)
    for i in range(0, ledboard_height, 1):
        pos = (i, i)
        ledboard[pos] = (0x7f, )
        pos = (i + ledboard_height, i)
        ledboard[pos] = (0x7f, )
    netcon.send_packet(ledboard)

if __name__ == "__main__":
    main()
