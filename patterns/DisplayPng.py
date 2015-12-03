from matrix import matrix_height, matrix_width, chunks
from Tools.Graphics import Graphics, BLACK
from PIL import Image


class DisplayPng(Graphics):
    def __init__(self, fname='Horseicon.thumbnail'):
        Graphics.__init__(self, width=matrix_width, height=matrix_height)
        self.fill(BLACK)

        image = Image.open(fname)
        colors = self.get_image_colors(image)
        p = 0
        for y in xrange(0, image.height):
            for x in xrange(0, image.width):
                self.draw_pixel(x, y, colors[p])
                p += 1

    def get_image_colors(self, image):
        image_colors = []
        image = image.tobytes()
        for data in chunks(image, 3):
            color = []
            for c in data:
                color.append(ord(c))
            image_colors.append(tuple(color))
        return image_colors

    def generate(self):
        pass
