from matrix import matrix_height, matrix_width
from Tools.Graphics import Graphics, BLACK
import png


def getPngPixelData(image):
    pngobj = png.Reader(image)
    data = pngobj.asRGBA8()
    palette = []
    for d in data[2]:
        palette.append(d)
    size = data[3]['size']
    colordata = []
    for color in palette:
        colordata.append(color[:3])
    return (colordata, size,)


class DisplayPng(Graphics):
    def __init__(self):
        # image = '/home/robert/py-artnet/hacked.png'
        # self.data = getPngPixelData(image)
        # self.pixeldata = self.data[0]
        Graphics.__init__(self, matrix_width, matrix_height)
        self.fill(BLACK)

    def generate(self):
        pass
