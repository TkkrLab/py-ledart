import png


def getPngPixelData(image):
    pngobj = png.Reader(image)
    data = pngobj.asRGBA8()
    palette = data[3]['palette']
    size = data[3]['size']
    colordata = []
    for color in palette:
        colordata.append(color[:3])
    return (colordata, size,)


class DisplayPng(object):
    def __init__(self):
        image = '/home/robert/py-art-net/hacked.png'
        self.data = getPngPixelData(image)
        self.pixeldata = self.data[0]

    def generate(self):
        return self.pixeldata
