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

""" Flattenc returns a dimension less list of characters."""
def flattenc(l):
  return [chr(y) for x in l for y in x]

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

        self.debug = False

    """ Send_clear sends a clear command to clear the ledboard."""
    def send_clear(self):
        self.bcast(self.clear)

    def grayscale(self, c):
        return chr((int(c[0])+ int(c[1]) + int(c[2])) / 3)

    def compress(self, data):
        compressed = []
        if self.grayscaling:
            # compressed = map(lambda x: chr(sum(x) / 3), data)
            compressed = map(self.grayscale, data)
        else:
            compressed = flattenc(data)
            # print compressed

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
            if(self.debug):
                print("packet len: %d" % len(packet))
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
            if(self.debug):
                print("packet len: %d" % len(packet))
        self.transmit(self.writeout, ip)

    def close(self):
        self.send_clear()
        Interface(self).close()