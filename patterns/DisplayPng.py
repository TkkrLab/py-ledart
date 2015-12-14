from matrix import matrix_height, matrix_width
from Tools.Graphics import Graphics, RED, BLACK
from Tools.Graphics import ImageSurface

import glob
import natsort


def create_frames(location):
    frames = {}
    frame_files = glob.glob(location + '*.png')
    frame_files = natsort.natsorted(frame_files)
    for i in range(0, len(frame_files)):
        frames[i] = frame_files[i]
    return dict(frames)


class DisplayPng(ImageSurface):
    def __init__(self, fname='images/sisters-sprites.png'):
        ImageSurface.__init__(self, fname)

    def generate(self):
        pass


class VideoPlay(ImageSurface):
    def __init__(self, location='images/videos/star-field/', center=True):
        self.frames = create_frames(location)
        ImageSurface.__init__(self, self.frames[0])
        if center:
            imwidth = self.get_width()
            left_over = matrix_width - imwidth
            x_offset = left_over / 2
            self.set_d_offset((x_offset, 0))
        self.fcount = 0

    def generate(self):
        self.load_png(self.frames[self.fcount])
        self.fcount += 1
        if(self.fcount == len(self.frames)):
            raise(Exception("Done playing."))


class RectTest(Graphics):
    def __init__(self):
        Graphics.__init__(self, matrix_width, matrix_height)
        self.fill(BLACK)

    def generate(self):
        pass
