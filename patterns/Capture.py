# from pymouse import PyMouse
# import pyscreenshot as ImageGrab

# from Tools.Graphics import ImageSurface
# from matrix import matrix_height, matrix_width


# class Capture(ImageSurface):
#     def __init__(self, invert=False, pos=None, size=None):
#         im = ImageGrab.grab(bbox=(0, 0, matrix_width, matrix_height),
#                             backend='wx')
#         ImageSurface.__init__(self, im)
#         self.invert = invert
#         self.mouse = PyMouse()

#     def generate(self):
#         x, y = self.mouse.position()
#         # center around the mouse
#         center_x = x - (matrix_width / 2)
#         center_y = y - (matrix_height / 2)
#         offset_x = x + matrix_width
#         offset_y = y + matrix_height
#         rect = (center_x, center_y, offset_x, offset_y)
#         image = ImageGrab.grab(bbox=(rect), backend='wx')
#         self.load_png(image, self.invert)
