import subprocess as sp
from DeviceInterfaces import BaseInterface


class Stream(BaseInterface):
    def __init__(self, dims=[0, 0, 128, 64], dest="10.42.11.153", port="12345"):
        self.dest_size = "%dx%d" % (dims[2], dims[3])
        self.dest_ip = dest
        self.dest_port = port

        self.command_fmt = (self.dest_size, self.dest_ip, self.dest_port)
        self.command_str = "ffmpeg -loglevel panic -framerate 1000 -video_size %s -f rawvideo -pixel_format rgb24 -i - -an -f mpegts -c:v libx264rgb -preset ultrafast -crf 0 -pix_fmt bgr24 -g 1 udp://%s:%s"
        self.command = self.command_str % self.command_fmt

        print("\n%s\n" % self.command)

        self.pipe = sp.Popen(self.command, shell=True, stdin=sp.PIPE)

    def send(self, data, dest):
        try:
            self.pipe.stdin.write(str(data))
        except:
            raise KeyboardInterrupt

    def close(self):
        self.pipe.stdin.write(buffer([0] * self.dims[2] * self.dims[3] * 3))
        self.pipe.terminate()



class StreamPlay(BaseInterface):
    def __init__(self, dims=[0, 0, 128, 64]):
        self.dims = dims
        size = "%dx%d" % (dims[2], dims[3])
        self.command = "ffmpeg -loglevel panic -g 1 -r 1000 -s " + size + " -f rawvideo -pixel_format rgb24 -i - -an -f mpegts -c:v libx264 -preset ultrafast -crf 0 pipe:1 | ffplay -loglevel panic -vf \"scale=iw*4:-1:flags=neighbor\" -i -"
        self.pipe = sp.Popen(self.command, shell=True, stdin=sp.PIPE)

    def send(self, data, dest):
        try:
            self.pipe.stdin.write(str(data))
        except:
            raise KeyboardInterrupt

    def close(self):
        self.pipe.terminate()
