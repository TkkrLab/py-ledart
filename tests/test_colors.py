import unittest
from Ledart.Tools.Graphics.Colors import *

class TestColors(unittest.TestCase):
    def test_colors(self):
        self.assertEqual(BLACK, [0, 0, 0])
        self.assertEqual(RED, [0xff, 0, 0])
        self.assertEqual(GREEN, [0, 0xff, 0])
        self.assertEqual(YELLOW, [0xff, 0xff, 0])
        self.assertEqual(BLUE, [0, 0, 0xff])
        self.assertEqual(PURPLE, [0xff, 0, 0xff])
        self.assertEqual(CYAN, [0, 0xff, 0xff])
        self.assertEqual(WHITE, [0xff, 0xff, 0xff])
        shouldbe_colors = [RED, GREEN, BLUE,
                           WHITE, BLACK, PURPLE,
                           YELLOW, CYAN]
        self.assertEqual(shouldbe_colors, COLORS)