import time
import subprocess as sp
import pymouse
import shlex
import os, fcntl, sys

from Ledart.Tools.Graphics import Surface
from Ledart.utils import chunks
from Ledart.ArgumentParser import get_args


class VideoPlay(Surface):
    def __init__(self, **kwargs):
        Surface.__init__(self, **kwargs)
        args = get_args()

        self.location = kwargs.get('location', None)
        center = kwargs.get('center', True)
        if self.location == None:
            return

        # load in a image with ffmpeg and apply fps
        ffmpeg = "ffmpeg"
        fmtstr = "-vf \"scale=%d:%d\""
        fmt = (self.width, self.height)
        filteropts = fmtstr % (fmt)
        command = [ffmpeg,
                   '-loglevel', 'panic',
                   '-i', self.location,
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
        if self.location == None:
            return

        # read and turn all elements into int values.
        raw_image = self.pipe.stdout.read(self.width * self.height * 3)
        raw_image = map(ord, raw_image)
        # create an itterator
        it = iter(raw_image)
        # use the itterator to zip three following values together.
        self.surface = [list(c) for c in zip(it, it, it)]

class CamCapture(Surface):
    # def __init__(self, dev='/dev/video0'):
    def __init__(self, **kwargs):
        Surface.__init__(self, **kwargs)
        dev = kwargs.get('dev', '/dev/video0')
        args = get_args()

        ffmpeg = 'ffmpeg'
        scale = "scale=%d:%d" % (self.width, self.height)

        command = [ffmpeg,
                   '-loglevel', 'panic',
                   '-f', 'v4l2',
                   '-r', '30',
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
        # read and turn all elements into int values.
        raw_image = self.pipe.stdout.read(self.width * self.height * 3)
        raw_image = map(ord, raw_image)
        # create an itterator
        it = iter(raw_image)
        # use the itterator to zip three following values together.
        self.surface = [list(c) for c in zip(it, it, it)]

class ScreenCapture(Surface):
    def __init__(self, **kwargs):
        Surface.__init__(self, **kwargs)
        screen_resolution = kwargs.get('screen_resolution', None)
        fullscreen = kwargs.get('fullscreen', False)
        fps = kwargs.get('fps', None)
        center = kwargs.get('center', True)

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
                       '-r', '30',
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
                       '-r', '30',
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
        # read and turn all elements into int values.
        raw_image = self.pipe.stdout.read(self.width * self.height * 3)
        # raw_image = map(ord, raw_image)
        # create an itterator
        it = iter(raw_image)
        # use the itterator to zip three following values together.
        self.surface = [list(c) for c in zip(it, it, it)]
