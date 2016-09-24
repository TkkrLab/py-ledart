import unittest
from Ledart.Tools.Graphics import Surface, WHITE, BLUE, BLACK

class TestSurface(unittest.TestCase):
    def setUp(self):
        self.width = 3
        self.height = 3
        self.pos = (0, 0)
        self.surface = Surface(width=self.width,
                               height=self.height,
                               offset=self.pos)

        self.test_bytes = bytearray(map(ord, "aandoenen"))
        self.test_string = self.test_bytes

    def test_init(self):
        self.assertEqual(self.surface.width, self.width, 'invalid width set')
        self.assertEqual(self.surface.height, self.height, 'invalid height set')
        self.assertEqual(self.surface.d_offset, self.pos, 'invalid position set')
        self.assertEqual(self.surface.size, self.width * self.height, 'invalid size')
        
        self.assertEqual(self.surface.color_rep, [0, 0, 0], 'invalid color representation')
        self.assertEqual(self.surface.color_depth, 0xFF, 'invalid color depth')

    def test_index_generation(self):
        for x in range(0, 3):
            for y in range(0, 3):
                point = (x, y)
                self.assertTrue(point in self.surface.indexes)

    def test_surface_generation(self):
        self.assertEqual(len(self.surface.surface), self.width * self.height)
        for c in self.surface.surface:
            self.assertEqual(c, BLACK, 'invalid default color')

    def test_surface_size(self):
        self.assertEqual(len(self.surface), self.width * self.height, 'object size wrong')

    def test_setgetitem_point_tuple(self):
        for i in range(0, 3):
            point = (i, i)
            self.surface[point] = WHITE
            self.assertEqual(self.surface[point], WHITE, 'failed to set color')
        self.assertEqual(len(self.surface), self.width * self.height, 'size changed during setting index')

        self.surface[(0, 0)] = BLUE
        self.assertEqual(self.surface[(0, 0)], BLUE, 'failed to set color')
        self.assertEqual(len(self.surface), self.width * self.height, 'size changed during setting index')

    def test_setgetitem_point_list(self):
        for i in range(0, 3):
            point = [i, i]
            self.surface[point] = WHITE
            self.assertEqual(self.surface[point], WHITE, 'failed to set color')
        self.assertEqual(len(self.surface), self.width * self.height, 'size changed during setting index')

        self.surface[(0, 0)] = BLUE
        self.assertEqual(self.surface[(0, 0)], BLUE, 'failed to set color')
        self.assertEqual(len(self.surface), self.width * self.height, 'size changed during setting index')

    def test_setgetitem_index(self):
        for i in range(0, self.width * self.height, 4):
            self.surface[i] = WHITE
        self.assertEqual(len(self.surface), self.width * self.height, 'size changed during setting index')

        for i in range(0, self.width * self.height, 4):
            self.assertEqual(self.surface[i], WHITE, 'failed to set color')
        self.assertEqual(len(self.surface), self.width * self.height, 'size changed during setting index')
        
        self.surface[0] = BLUE
        self.assertEqual(self.surface[0], BLUE, 'failed to set color')
        self.assertEqual(len(self.surface), self.width * self.height, 'size changed during setting index')

    def test_setgetitem_index_vs_point(self):
        for i in range(0, self.width * self.height, 4):
            self.surface[i] = WHITE
        self.assertEqual(len(self.surface), self.width * self.height, 'size changed during setting index')

        for i in range(0, 3):
            self.assertEqual(self.surface[(i, i)], WHITE, 'failed to get pixel from point')
        self.assertEqual(len(self.surface), self.width * self.height, 'size changed during setting index')

    def test_setgetitem_point_vs_index(self):
        for i in range(0, 3):
            self.surface[(i, i)] = WHITE
        self.assertEqual(len(self.surface), self.width * self.height, 'size changed during setting index')

        for i in range(0, self.width * self.height, 4):
            self.assertEqual(self.surface[i], WHITE, 'failed to get pixel from index')
        self.assertEqual(len(self.surface), self.width * self.height, 'size changed during setting index')

    def test_setgetitem_slice(self):
        for i in range(0, 3):
            self.surface[(i, i)] = WHITE
        
        sl1 = slice(0, 3)
        sl2 = slice(3, 6)
        sl3 = slice(6, 9)
        
        self.assertEqual(self.surface[sl1], [WHITE, BLACK, BLACK], 'failed to take right slice')
        self.assertEqual(self.surface[sl2], [BLACK, WHITE, BLACK], 'failed to take right slice')
        self.assertEqual(self.surface[sl3], [BLACK, BLACK, WHITE], 'failed to take right slice')

    def test_set_color(self):
        with self.assertRaises(ValueError):
            self.surface[0] = [-1, -1, -1]

        with self.assertRaises(ValueError):
            self.surface[0] = [-1]

        with self.assertRaises(ValueError):
            self.surface[0] = [0x100, 0x100, 0x100]

        with self.assertRaises(ValueError):
            self.surface[0] = [0x100]

        with self.assertRaises(ValueError):
            self.surface[0] = (0, 0, 0)

    def test_setitem(self):
        with self.assertRaises(KeyError):
            self.surface[-1] = WHITE

        with self.assertRaises(KeyError):
            self.surface[(-1, 0)] = WHITE

        with self.assertRaises(KeyError):
            self.surface[(0, -1)] = WHITE

        with self.assertRaises(KeyError):
            self.surface[2.0] = WHITE

    def test_get_color(self):
        with self.assertRaises(KeyError):
            color = self.surface[-1]

        with self.assertRaises(KeyError):
            color = self.surface[2.0]

        with self.assertRaises(KeyError):
            color = self.surface[(0, -1)]

        with self.assertRaises(KeyError):
            color = self.surface[(-1, 0)]

    def test_get_size(self):
        size = self.width * self.height
        self.assertEqual(size, self.surface.get_size(), 'size set wrongly in surface object')

    def test_get_width(self):
        self.assertEqual(self.width, self.surface.get_width(), 'width set wrongly in surface object')

    def test_get_height(self):
        self.assertEqual(self.height, self.surface.get_height(), 'height set wrongly in surface object')

    def test_get_points(self):
        for i in range(0, 3):
            self.surface[(i, i)] = WHITE
        
        test_points = {}
        i = 0
        for y in range(0, self.height):
            for x in range(0, self.width):
                point = (x, y)
                test_points[point] = i
                i += 1
        self.assertTrue(test_points == self.surface.get_points(), 'points are wrongly generated')

    def test_set_d_offset(self):
        new_offset = (10, 42)
        self.surface.set_d_offset(new_offset)
        self.assertTrue(self.surface.d_offset == new_offset, 'offset is not set correctly in surface object')

    def test_get_d_offset(self):
        self.assertTrue(self.surface.get_d_offset() == (0, 0), 'offset is not set correctly in surface object')

    def test_repr(self):
        for i in range(0, 3):
            self.surface[(i, i)] = WHITE
        fmtstr = "<Surface width=%d, height=%d, [%s, ... %s]>"
        fmt = (self.width, self.height, self.surface.surface[0], self.surface.surface[-1])
        what_it_is = repr(self.surface)
        what_it_shouldbe = (fmtstr % fmt)
        self.assertEqual(what_it_is, what_it_shouldbe, 'repr generated wrongly')

    """
        byte arrays and string arrays in python2.7 are the same.
        making different tests for them is thus difficult.
    """
    def test_bytes(self):
        for i, c in enumerate(self.test_bytes):
            self.surface[i] = [c, 0, 0]
        shouldbe = ''.join([chr(byte) for c in self.test_bytes for byte in [c, 0, 0]])
        self.assertEqual(bytes(self.surface), shouldbe, 'wrong byte generation')

    def test_string(self):
        for i, c in enumerate(self.test_string):
            self.surface[i] = [c, 1, 1]

        shouldbe = ''.join([chr(char) for c in self.test_string for char in [c, 1, 1]])
        self.assertEqual(str(self.surface), shouldbe, 'wrong string generation')
