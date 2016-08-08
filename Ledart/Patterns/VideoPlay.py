import time
import subprocess as sp
import pymouse
import shlex
import os, fcntl, sys

from Ledart.Tools.Graphics import Surface
from Ledart.matrix import matrix_width, matrix_height, chunks
from Ledart.ArgumentParser import get_args


class VideoPlay(Surface):
    def __init__(self, location='', center=True):
        Surface.__init__(self, width=matrix_width, height=matrix_height)
        args = get_args()

        # load in a image with ffmpeg and apply fps
        ffmpeg = "ffmpeg"
        fmtstr = "-vf \"scale=%d:%d\""
        fmt = (self.width, self.height)
        filteropts = fmtstr % (fmt)
        command = [ffmpeg,
                   '-loglevel', 'panic',
                   '-i', location,
                   filteropts,
                   '-f', 'image2pipe',
                   '-pix_fmt', 'rgb24',
                   '-vcodec', 'rawvideo',
                   '-']

        command = ' '.join(command)
        if args.debug:
            print("\ncommand: %s" % (command))
        self.pipe = sp.Popen(shlex.split(command), stdout=sp.PIPE)

    def generate(self):
        # read and turn all elements into int values.
        raw_image = self.pipe.stdout.read(self.width * self.height * 3)
        raw_image = map(ord, raw_image)
        # create an itterator
        it = iter(raw_image)
        # use the itterator to zip three following values together.
        self.surface = zip(it, it, it)

class CamCapture(Surface):
    def __init__(self, dev='/dev/video0'):
        Surface.__init__(self, width=matrix_width, height=matrix_height)
        args = get_args()

        ffmpeg = 'ffmpeg'
        scale = "scale=%d:%d" % (self.width, self.height)

        command = [ffmpeg,
                   '-loglevel', 'panic',
                   '-f', 'v4l2',
                   '-r', '1',
                   '-video_size', '160x120',
                   '-i', dev,
                   '-vf', scale,
                   '-f', 'image2pipe',
                   '-pix_fmt', 'rgb24',
                   '-vcodec', 'rawvideo',
                   '-']

        command = ' '.join(command)
        if args.debug:
            print("\ncommand: %s" % command)
        self.pipe = sp.Popen(shlex.split(command), stdout=sp.PIPE)

    def generate(self):
        # turn all elements into int values.
        raw_image = self.pipe.stdout.read(self.width * self.height * 3)
        raw_image = map(ord, raw_image)
        # create an itterator
        it = iter(raw_image)
        # use the itterator to zip three following values together.
        self.surface = zip(it, it, it)

class ScreenCapture(Surface):
    def __init__(self, screen_resolution=None, fullscreen=False, fps=None,
                 center=True):
        Surface.__init__(self, width=matrix_width, height=matrix_height)
        args = get_args()
        if screen_resolution is None:
            pm = pymouse.PyMouse()
            screen_resolution = pm.screen_size()
            if args.debug:
                print("selected resolution: " + str(screen_resolution))
        ffmpeg = "ffmpeg"
        display = os.getenv("DISPLAY")
        if fps == None:
            fps = get_args().fps
        if fullscreen:
            fmt = screen_resolution
            fmtstr = "%dx%d"
            screensize = fmtstr % fmt
            scale = "scale=%d:%d" % (self.width, self.height)
            command = [ffmpeg,
                       '-loglevel', 'panic',
                       '-video_size', screensize,
                       # '-framerate', '10.0',
                       '-f', 'x11grab',
                       '-i', display,
                       '-f', 'image2pipe',
                       '-pix_fmt', 'rgb24',
                       '-vcodec', 'rawvideo',
                       '-preset', 'ultrafast',
                       '-crf', '0',
                       '-vf', scale,
                       '-an', '-']
        else:
            fmt = (self.width, self.height)
            fmtstr = "%dx%d"
            screensize = fmtstr % fmt
            command = [ffmpeg,
                       '-loglevel', 'panic',
                       '-video_size', screensize,
                       # '-framerate', '10.0',
                       '-follow_mouse', 'centered',
                       '-draw_mouse', '0',
                       '-f', 'x11grab',
                       '-i', display,
                       '-f', 'image2pipe',
                       '-pix_fmt', 'rgb24',
                       '-vcodec', 'rawvideo',
                       '-preset', 'ultrafast',
                       '-crf', '0',
                       '-an', '-']

        command = ' '.join(command)
        if args.debug:
            print("\ncommand: %s" % (command))
        self.pipe = sp.Popen(shlex.split(command), stdout=sp.PIPE)

    def generate(self):
        # turn all elements into int values.
        raw_image = self.pipe.stdout.read(self.width * self.height * 3)
        raw_image = map(ord, raw_image)
        # create an itterator
        it = iter(raw_image)
        # use the itterator to zip three following values together.
        self.surface = zip(it, it, it)

# import av

# class VideoTest(Surface):
#     def __init__(self):
#         Surface.__init__(self, width=matrix_width, height=matrix_height)
#         self.container = av.open('/home/robert/Videos/bad.mkv')
#         self.video = next(s for s in self.container.streams if s.type == b'video')
#         frame = self.generate_frame()
#         self.draw_frame(frame)
    
#     def generate_frame(self):
#         data = []
#         for packet in self.container.demux(self.video):
#             for frame in packet.decode():
#                 f = frame.reformat(matrix_width, matrix_height, 'rgb24')
#                 data = []
#                 for row in f.to_nd_array():
#                     data.extend(map(list, row))
#                 yield(data)
    
#     def draw_frame(self, frame):
#         # frame will be a generator be we just want to tackle this one generator at a time.
#         for i, color in enumerate(frame.next()):
#             self[i] = color
    
#     def generate(self):
#         frame = self.generate_frame()
#         self.draw_frame(frame)
#         # we determine our own fps.
#         # actually better do this with a timer
#         # time.sleep(float(1./self.video.average_rate))
