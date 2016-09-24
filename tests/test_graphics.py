import unittest
from Ledart.Tools.Graphics import Graphics

class TestGraphics(unittest.TestCase):
    def setUp(self):
        self.width = 3
        self.height = 3
        self.pos = (0, 0)

        self.graphics = Graphics(width=self.width,
                                 height=self.height,
                                 offset=self.pos)

    def test_init(self):
        self.assertEquals(self.graphics.width, self.width, 'width set wrong')
