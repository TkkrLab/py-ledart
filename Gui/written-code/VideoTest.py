from matrix import matrix_width, matrix_height
from Tools.Graphics import Surface
import time

import av

class VideoTest(Surface):
    def __init__(self):
        Surface.__init__(self, width=matrix_width, height=matrix_height)
        self.container = av.open('/home/robert/Videos/bad.mkv')
        self.video = next(s for s in self.container.streams if s.type == b'video')
        frame = self.generate_frame()
        self.draw_frame(frame)
    
    def generate_frame(self):
        data = []
        for packet in self.container.demux(self.video):
            for frame in packet.decode():
                f = frame.reformat(matrix_width, matrix_height, 'rgb24')
                data = []
                for row in f.to_nd_array():
                    data.extend(map(tuple, row))
                yield(data)
    
    def draw_frame(self, frame):
        # frame will be a generator be we just want to tackle this one generator at a time.
        for i, color in enumerate(frame.next()):
            self[i] = color
    
    def generate(self):
        frame = self.generate_frame()
        self.draw_frame(frame)
        # uh don't make it hang :D testing!
        time.sleep(20)