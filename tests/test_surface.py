import unittest
from Ledart import Surface, WHITE, BLUE

class SurfaceTest(unittest.TestCase):
    def setUp(self):
        self.width = 3
        self.height = 3
        self.pos = (0, 0)
        self.surface = Surface(width=self.width,
                               height=self.height,
                               offset=self.pos)

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
            self.assertEqual(c, [0, 0, 0], 'invalid default color')

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
        pass