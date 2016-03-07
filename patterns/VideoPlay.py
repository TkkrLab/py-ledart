from Tools.Graphics import Surface
from matrix import matrix_width, matrix_height, chunks
from ArgumentParser import get_args, add_argument
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
    def __init__(self, location='', fps=18.4, center=True):
        Surface.__init__(self, width=matrix_width, height=matrix_height)
        # load in a image with ffmpeg and apply fps
        ffmpeg = "ffmpeg"
        # # "fps=10.0, "
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

class ScreenCapture(Surface):
    def __init__(self, fps=10.0, screen_resolution=None, fullscreen=False,
                 center=True):
        Surface.__init__(self, width=matrix_width, height=matrix_height)
        add_argument("--test", type=str, default="a", help="<testing>", metavar="<testing>")
        args = get_args()
        print(args.test)
        if screen_resolution is None:
            pm = pymouse.PyMouse()
            screen_resolution = pm.screen_size()
            print(screen_resolution)
        ffmpeg = "ffmpeg"
        display = os.getenv("DISPLAY")
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
                       '-an', '-']

        command = ' '.join(command)
        self.pipe = sp.Popen(shlex.split(command), stdout=sp.PIPE)
        self.play_next_image()

    def play_next_image(self):
        raw_image = self.pipe.stdout.read(self.width * self.height * 3)
        load_rgb24(raw_image, self)

    def generate(self):
        self.play_next_image()
