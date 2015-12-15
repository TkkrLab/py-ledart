from Tools.Graphics import Surface
from matrix import matrix_width, matrix_height, chunks
import subprocess as sp


def load_rgb24(data, surface):
    p = 0
    indexes = surface.get_points()
    for c in chunks(data, 3):
        color = (ord(c[0]), ord(c[1]), ord(c[2]))
        point = indexes[p]
        surface[point] = color
        p += 1


class VideoPlay(Surface):
    def __init__(self, location=None, fps=18, center=True):
        Surface.__init__(self, width=matrix_width, height=matrix_height)
        # load in a image with ffmpeg and apply fps
        ffmpeg = "ffmpeg"
        # "fps=10.0, "
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
        self.pipe = sp.Popen(command, shell=True, stdout=sp.PIPE,
                             bufsize=10 ** 8)
        self.play_next_image()

    def play_next_image(self):
        raw_image = self.pipe.stdout.read(self.width * self.height * 3)
        load_rgb24(raw_image, self)

    def generate(self):
        self.play_next_image()


class ScreenCapture(Surface):
    def __init__(self, fps=10, center=True):
        Surface.__init__(self, width=matrix_width, height=matrix_height)
        ffmpeg = "ffmpeg"

        command = [ffmpeg,
                   '-loglevel', 'panic',
                   '-video_size', '96x48',
                   '-framerate', str(fps),
                   '-follow_mouse', '1',
                   '-f', 'x11grab',
                   '-i', ':0.0',
                   '-f', 'image2pipe',
                   '-pix_fmt', 'rgb24',
                   '-vcodec', 'rawvideo', '-']

        command = ' '.join(command)
        self.pipe = sp.Popen(command, shell=True, stdout=sp.PIPE,
                             bufsize=10 ** 8)
        self.play_next_image()

    def play_next_image(self):
        raw_image = self.pipe.stdout.read(self.width * self.height * 3)
        load_rgb24(raw_image, self)

    def generate(self):
        self.play_next_image()
