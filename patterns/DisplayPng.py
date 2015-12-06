from matrix import matrix_height, matrix_width, chunks
from Tools.Graphics import Surface, Graphics, BLACK
from Tools.Graphics.RGBColorTools import ColorRGBOps
from PIL import Image


class ImageSurface(Graphics):
    def __init__(self, width, height, fname):
        if fname:
            Graphics.__init__(self, width=width, height=height)
            self.load_png(fname)
        else:
            raise(Exception("unable to load png: %s" % (fname)))

    def load_png(self, fname):
        self.image = Image.open(fname)
        imdata = self.image.getdata()
        p = 0
        for y in range(0, self.image.height):
            for x in range(0, self.image.width):
                point = (x, y)
                if len(imdata[p]) == 3:
                    color = imdata[p]
                else:
                    r, g, b, alpha = imdata[p]
                    color = (r, g, b)
                color = ColorRGBOps.darken(color, 220)
                self[point] = color
                p += 1
        return dict(self.surface)


# class DisplayPng(ImageSurface):
#     def __init__(self, fname='images/hue_alpha-min.png'):
#         ImageSurface.__init__(self, matrix_width, matrix_height, fname)

#     def generate(self):
#         pass

import glob
import natsort
import sys


frames = {}
frame_files = glob.glob('images/frames/*.png')
frame_files = natsort.natsorted(frame_files)
for i in range(0, len(frame_files)):
    frames[i] = frame_files[i]
num_frames = len(frame_files)


# class DisplayPng(ImageSurface):
#     def __init__(self):
#         ImageSurface.__init__(self, matrix_width, matrix_height, frames[0])
#         self.fcount = 0

#     def generate(self):
#         self.load_png(frames[self.fcount])
#         self.fcount += 1

class DisplayPng(ImageSurface):
    def __init__(self):
        ImageSurface.__init__(self, matrix_width, matrix_height, frames[0])
        self.fcount = 0
        self.frames = {}
        print("loading frames.")
        for i in range(0, num_frames):
            self.frames[i] = self.load_png(frames[i])
        print("done loading frames.")

    def generate(self):
        self.surface = self.frames[self.fcount]
        self.fcount += 1
