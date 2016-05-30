"""
    author: Duality
    protocol author: Jawsper
    https://github.com/jawsper

    this file describes a protocol that implements,
    part of the documented lcmp protocol,
    because only part is needed for the working of
    py-ledart software.

"""
from ProtocolInterface import Interface


def chunked(data, chunksize):
    """ yield sections 'chunks' of data, with iteration count."""
    chunk = []
    it = 0
    while(it < (len(data) / chunksize)):
        index = (it * chunksize)
        chunk = data[index:(index + chunksize)]
        yield (it, chunk)
        it += 1


class Lmcp(Interface):
    def __init__(self, args, port=1337):
        Interface.__init__(self, args, port)
        self.send_limit = 1024 - 5

        self.writeout = chr(0x01)
        self.draw_rows = chr(0x10)
        self.draw_image = chr(0x11)
        self.clear = chr(0x02)
        self.draw_rows_rgb = chr(0x30)
        self.draw_image_rgb = chr(0x31)
        self.cleared = False
        self.grayscaling = (self.args.color != "enabled")

    def compress(self, data):
        # print(type(data))
        compressed = []
        for color in data:
            if self.grayscaling:
                compressed.append(chr((int(color[0])+ int(color[1])+ int(color[2]))/3))
            else:
                # compressed.append(chr((int(color[0]) + int(color[1]) + int(color[2])) ))
                for c in color:
                    compressed += chr(int(c))

        return ''.join(compressed)

    def send(self, data, ip):
        if self.grayscaling:
            draw_image = self.draw_image
        else:
            draw_image = self.draw_image_rgb
        (x, y), width, height = data.d_offset, data.width, data.height
        size = self.send_limit / data.width
        chunksize = size * data.width
        for i, chunk in chunked(data, chunksize):
            packet = (draw_image + chr(x) + chr(y + size * i) +
                      chr(data.width) + chr(size))
            packet += self.compress(chunk)
            self.transmit(packet, ip)
        # then if any data remains over, transmit that to the last bit.
        # recalculate the new rectangle to write to.
        remains = data.height % size
        if remains:
            y = data.height - remains
            chunksize = data.width * remains
            chunk = data[-chunksize:]
            packet = (draw_image + chr(x) + chr(y) +
                      chr(data.width) + chr(remains))
            packet += self.compress(chunk)
            self.transmit(packet, ip)
        self.transmit(self.writeout, ip)
