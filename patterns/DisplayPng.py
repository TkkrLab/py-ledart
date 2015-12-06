from matrix import matrix_height, matrix_width, chunks
from Tools.Graphics import Surface, Graphics, BLACK
from PIL import Image


class ImageSurface(Surface):
    def __init__(self, width, height, fname):
        Surface.__init__(self, width=width, height=height)
        if fname:
            self.image = Image.open(fname)
            self.load_png()

    def load_png(self):
        imdata = self.image.getdata()
        p = 0
        for y in range(0, self.image.height):
            for x in range(0, self.image.width):
                point = (x, y)
                if len(imdata[p]) == 3:
                    color = imdata[p]
                else:
                    alpha = imdata[p][3]
                    color = (imdata[p][0] & alpha,
                             imdata[p][1] & alpha,
                             imdata[p][2] & alpha)
                self[point] = color
                p += 1


# class DisplayPng(ImageSurface):
#     def __init__(self, fname='images/hue_alpha-min.png'):
#         ImageSurface.__init__(self, matrix_width, matrix_height, fname)

#     def generate(self):
#         pass

import glob
import natsort


frames = {}
frame_files = glob.glob('images/frames/*.png')
frame_files = natsort.natsorted(frame_files)
for i in range(0, len(frame_files)):
    frames[i] = frame_files[i]


class DisplayPng(ImageSurface):
    def __init__(self):
        ImageSurface.__init__(self, matrix_width, matrix_height, frames[100])
        self.fcount = 0

    def generate(self):
        ImageSurface.__init__(self, matrix_width, matrix_height,
                              frames[self.fcount])
        self.fcount += 1
