from matrix import matrix_height, matrix_width
from Tools.Graphics import Surface, Graphics, WHITE
from Tools.Graphics import ColorRGBOps
from PIL import Image

import glob
import natsort


class ImageSurface(Surface):
    def __init__(self, fname):
        if fname:
            self.image = Image.open(fname)
            Surface.__init__(self, width=self.image.width, height=self.image.height)
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
                self[point] = color
                p += 1
        return dict(self.surface)


def create_frames(location):
    frames = {}
    frame_files = glob.glob(location + '*.png')
    frame_files = natsort.natsorted(frame_files)
    for i in range(0, len(frame_files)):
        frames[i] = frame_files[i]
    return dict(frames)


class DisplayPng(ImageSurface):
    def __init__(self, fname):
        ImageSurface.__init__(self, fname)

    def generate(self):
        pass


class VideoPlay(ImageSurface):
    def __init__(self, location, center=True):
        self.frames = create_frames(location)
        ImageSurface.__init__(self, self.frames[0])
        if center:
            self.set_d_offset((10, 0))
        self.fcount = 0

    def generate(self):
        self.load_png(self.frames[self.fcount])
        self.fcount += 1
        if(self.fcount == len(self.frames)):
            raise(Exception("Done playing."))


class RectTest(Graphics):
    def __init__(self):
        Graphics.__init__(self, 10, 10)
        self.fill(WHITE)

    def generate(self):
        pass
