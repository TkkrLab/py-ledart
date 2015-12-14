from matrix import matrix_height, matrix_width
from matrix import chunks
from Tools.Graphics import Graphics, RED
from Tools.Graphics import ImageSurface

import glob
import natsort
import subprocess as sp
import os


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


class VideoPlay(Graphics):
    def __init__(self, location=None, center=True):
        Graphics.__init__(self, width=matrix_width, height=matrix_height)
        # load in a image with ffmpeg
        FFMPEG_BIN = "ffmpeg"
        fmtstr = "-vf \"fps=10.0, scale=%d:%d\""
        fmt = (self.width, self.height)
        filteropts = fmtstr % (fmt)
        command = [FFMPEG_BIN,
                   '-loglevel', 'panic',
                   '-i', location,
                   filteropts,
                   '-f', 'image2pipe',
                   '-pix_fmt', 'rgb24',
                   '-vcodec', 'rawvideo', '-']
        command = ' '.join(command)
        self.pipe = sp.Popen(command, shell=True, stdout=sp.PIPE, bufsize=10 ** 8)
        raw_image = self.pipe.stdout.read(self.width * self.height * 3)
        # self.fill(RED)
        self.load_rgb24(raw_image)

    def play_next_image(self):
        raw_image = self.pipe.stdout.read(self.width * self.height * 3)
        self.load_rgb24(raw_image)

    def load_rgb24(self, data):
        p = 0
        indexes = self.get_points()
        for c in chunks(data, 3):
            color = (ord(c[0]), ord(c[1]), ord(c[2]))
            point = indexes[p]
            self[point] = color
            p += 1

    def generate(self):
        self.play_next_image()


# class VideoPlay(ImageSurface):
#     def __init__(self, location='images/videos/star-field/', center=True):
#         self.frames = create_frames(location)
#         ImageSurface.__init__(self, self.frames[0])
#         if center:
#             imwidth = self.get_width()
#             left_over = matrix_width - imwidth
#             x_offset = left_over / 2
#             self.set_d_offset((x_offset, 0))
#         self.fcount = 0

#     def generate(self):
#         self.load_png(self.frames[self.fcount])
#         self.fcount += 1
#         if(self.fcount == len(self.frames)):
#             raise(Exception("Done playing."))


class RectTest(Graphics):
    def __init__(self):
        Graphics.__init__(self, 10, 10)
        self.set_d_offset((56 - 10, 32 - 10))
        self.fill(RED)

    def generate(self):
        pass
