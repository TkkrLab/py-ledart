import png
from matrix import *

def getPngPixelData(image):
    pngObj = png.Reader(image)
    data = pngObj.asRGBA8()
    palette = data[3]['palette']
    size = data[3]['size']
    colorData = []
    for color in palette:
        colorData.append(color[:3])
    return (colorData, size,)

class DisplayPng(object):
    def __init__(self):
        image = '/home/robert/py-art-net/patterns/Graphics/resize.png'
        self.data = getPngPixelData(image)
        self.pixeldata = self.data[0]
    def generate(self):
        return self.pixeldata