from Ledart.matrix import matrix_width, matrix_height, chunked
from Ledart.Tools.Graphics import Graphics, BLUE, WHITE, BLACK

import alsaaudio, time, audioop

# while True:
#     # Read data from device
#     l,data = inp.read()
#     if l:
#         # Return the maximum of the absolute value of all samples in a fragment.
#         print audioop.max(data, 2)
#     time.sleep(.001)

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

class VUmeter(Graphics):
    def __init__(self):
        Graphics.__init__(self, matrix_width, matrix_height)
        self.inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK)
        self.inp.setchannels(1)
        self.inp.setrate(4000)
        self.inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        self.period = self.width
        self.inp.setperiodsize(self.period)

    def generate(self):
        self.fill(BLACK)
        l, data = self.inp.read()
        if l:
            for x, chunk in chunked(data, len(data) / self.period):
                h = int(audioop.avg(chunk, 1))
                c1 = h * 4
                c = [min(0xff, c1), 0xff - min(0xff, c1), 0]

                self.draw_line(x, self.height, x, self.height - h, c)
        # for x in range(0, self.width):
        #     if l:
        #         self.h = audioop.max(data, 2) / 4
        #     self.draw_line(x, self.height, x, self.height - self.h, BLUE)