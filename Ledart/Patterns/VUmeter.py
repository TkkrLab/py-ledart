from Ledart.utils import chunked
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
    def __init__(self, **kwargs):
        Graphics.__init__(self, **kwargs)
        self.stream = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK)
        self.stream.setchannels(2)
        self.stream.setrate(8000)
        self.stream.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        self.stream.setperiodsize(self.width)

    def generate(self):
        self.fill(BLACK)
        l, data = self.stream.read()
        h = 0
        if l:
            for x, data in chunked(data, len(data) / self.width):
                # try:
                if not (len(data) & 1):
                    h = audioop.max(data, 2) / 100
                # except Exception as e:
                #     # print(e)
                #     pass
                color = [min(h, 0xff), max(0xff - h, 0), 0]
                self.draw_line(x, self.height, x, self.height - h, color)
            # print((audioop.max(data, 2) / 100) * "*")
        # self.draw_line(0, 0, self.width, 0, BLUE)