from Tools.Graphics import Surface
from matrix import matrix_width, matrix_height, chunks
from ArgumentParser import get_args
import subprocess as sp
import pymouse
import shlex
import os


def load_rgb24(data, surface):
    p = 0
    indexes = surface.get_points()
    for c in chunks(data, 3):
        color = (ord(c[0]), ord(c[1]), ord(c[2]))
        point = indexes[p]
        surface[point] = color
        p += 1

class VideoPlay(Surface):
    def __init__(self, location='', fps=None, center=True):
        Surface.__init__(self, width=matrix_width, height=matrix_height)
        # load in a image with ffmpeg and apply fps
        ffmpeg = "ffmpeg"
        # # "fps=10.0, "
        if fps == None:
            fps = "fps=%d, " % float(get_args().fps)
        else:
            fps = "fps=%d, " % float(fps)
        fmtstr = "-vf \"%sscale=%d:%d\""
        fmt = (fps, self.width, self.height)
        filteropts = fmtstr % (fmt)
        command = [ffmpeg,
                   '-loglevel', 'panic',
                   '-i', location,
                   filteropts,
                   '-f', 'image2pipe',
                   '-pix_fmt', 'rgb24',
                   '-vcodec', 'rawvideo', '-']

        command = ' '.join(command)
        self.pipe = sp.Popen(shlex.split(command), stdout=sp.PIPE)

    def play_next_image(self):
        raw_image = self.pipe.stdout.read(self.width * self.height * 3)
        load_rgb24(raw_image, self)

    def generate(self):
        self.play_next_image()

class CamCapture(Surface):
    def __init__(self, dev='/dev/video0', fps=None):
        Surface.__init__(self, width=matrix_width, height=matrix_height)
        if fps == None:
            fps = str(get_args().fps)

        ffmpeg = 'ffmpeg'
        scale = "scale=%d:%d" % (self.width, self.height)

        command = [ffmpeg,
                   '-f', 'v4l2',
                   '-framerate', fps,
                   '-video_size', '160x120',
                   '-i', dev,
                   '-vf', scale,
                   '-f', 'image2pipe',
                   '-pix_fmt', 'rgb24',
                   '-vcodec', 'rawvideo',
                   '-']

        command = ' '.join(command)
        print("command: ", command)
        self.pipe = sp.Popen(shlex.split(command), stdout=sp.PIPE)

    def play_next_image(self):
        raw_image = self.pipe.stdout.read(self.width * self.height * 3)
        load_rgb24(raw_image, self)

    def generate(self):
        self.play_next_image()

class ScreenCapture(Surface):
    def __init__(self, screen_resolution=None, fullscreen=False, fps=None,
                 center=True):
        Surface.__init__(self, width=matrix_width, height=matrix_height)
        if screen_resolution is None:
            pm = pymouse.PyMouse()
            screen_resolution = pm.screen_size()
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
                       '-framerate', str(fps),
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
                       '-framerate', str(fps),
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
        print("using command: %s" % (command))
        self.pipe = sp.Popen(shlex.split(command), stdout=sp.PIPE)
        self.play_next_image()

    def play_next_image(self):
        raw_image = self.pipe.stdout.read(self.width * self.height * 3)
        load_rgb24(raw_image, self)

    def generate(self):
        self.play_next_image()
