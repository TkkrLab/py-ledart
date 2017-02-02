"""
author: Duality
protocol author: Jawsper
https://github.com/jawsper

this file describes a protocol that implements,
part of the documented lcmp protocol,
because only part is needed for the working of
py-ledart software.

"""

from DeviceInterfaces import UdpSocket
from utils import chunked

def rgb24(colordata):
    """ 
    Take color input, and flattens the input.
    returns raw rgb24
    """
    return ''.join([chr(y) for x in colordata for y in x])

def grayscale(colordata, cache=[]):
    """
    Grayscale data input.
    return every 3 bytes averaged (r, g, b)
    """

    # averages a triplet of [r, g, b]
    def avgtri(c):
        return chr((c[0]+ c[1] + c[2]) / 3)
    return ''.join([avgtri(c) for c in colordata])


class LegacyLmcp(UdpSocket):
    """
    Legacy Lmcp has the ability to either transmit full color image.
    or to transmit a grayscalled image, for which also could be set a
    color overlay.
    """
    def __init__(self, dispmode=grayscale, port=1337):
        UdpSocket.__init__(self, port)
        self.send_limit = 1024 - 5

        self.writeout = chr(0x01)
        self.draw_rows = chr(0x10)
        self.draw_image = chr(0x11)
        self.clear = chr(0x02)
        self.draw_rows_rgb = chr(0x30)
        self.draw_image_rgb = chr(0x31)
        self.cleared = False
        # dictates how data is displayed
        self.dispmode = dispmode

        self.debug = False

    def send_clear(self):
        self.bcast(self.clear)

    def send(self, data, dest):
        """
        Calculates (data) chunks based on max data size allowed per packet.
        Then transmit and draws those blocks to dest.
        """
        if self.dispmode == grayscale:
            draw_image = self.draw_image
        else:
            draw_image = self.draw_image_rgb
        (x, y), width, height = data.d_offset, data.width, data.height
        size = self.send_limit / width
        chunksize = size * width
        for i, chunk in chunked(data, chunksize):
            packet = (draw_image + chr(x) + chr(y + size * i) +
                      chr(width) + chr(size))
            packet += self.dispmode(chunk)
            self.transmit(packet, dest)
            if(self.debug):
                print("packet len: %d" % len(packet))
        # then if any data remains over, transmit that to the last bit.
        # recalculate the new rectangle to write to.
        remains = data.height % size
        if remains:
            y = data.height - remains
            chunksize = width * remains
            chunk = data[-chunksize:]
            packet = (draw_image + chr(x) + chr(y) +
                      chr(width) + chr(remains))
            packet += self.dispmode(chunk)
            self.transmit(packet, dest)
            if(self.debug):
                print("packet len: %d" % len(packet))
        self.transmit(self.writeout, dest)


    def close(self):
        self.send_clear()
        UdpSocket(self).close()


class Lmcp(LegacyLmcp):
    """
    New Lmcp implementation doesn't have grayscaling.
    so no need for selecting a mode.

    for now it's just legacy.
    """
    def __init__(self, port=1337):
        LegacyLmcp.__init__(self, dispmode=grayscale, port=port)


class TestLmcp(LegacyLmcp):
    def __init__(self, port=1337):
        LegacyLmcp.__init__(self, port)

    def make_header(self, *args):
        header = []
        for c in args:
            if not isinstance(c, str):
                header.append(chr(c))
            else:
                header.append(c)
        return ''.join(header)
    
    def send(self, data, dest):
        draw_image = self.draw_image_rgb
        (x, y), width, height = data.d_offset, data.width, data.height
        packet = self.make_header(draw_image, x, y, width, height)
        packet += str(data)
        self.transmit(packet, dest)
        self.transmit(self.writeout, dest)
