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


import sys


class Lmcp(Interface):
    def __init__(self, args, port=1337):
        Interface.__init__(self, args, port)
        self.send_limit = 1024 - 5

        self.writeout = chr(0x01)
        self.draw = chr(0x10)
        self.draw_image = chr(0x11)

    def compress(self, data):
        compressed = ''
        for color in data:
            compressed += chr(sum(color) / 3)
        return compressed

    def send(self, data, ip):
        if type(data) == str:
            return
        else:
            (x, y), width, height = data.d_offset, data.width, data.height
            if data.size <= self.send_limit:
                packet = (self.draw_image + chr(x) + chr(y) +
                          chr(width) + chr(height))
                packet += self.compress(data)
                self.transmit(packet, ip)
                self.transmit(self.writeout, ip)
            else:
                # figure out how many rows you can send withing the limit
                # and transmit that.
                size = self.send_limit / data.width
                chunksize = size * data.width
                for i, chunk in chunked(data, chunksize):
                    packet = (self.draw_image + chr(x) + chr(y + size * i) +
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
                    packet = (self.draw_image + chr(x) + chr(y) +
                              chr(data.width) + chr(remains))
                    packet += self.compress(chunk)
                    self.transmit(packet, ip)
                self.transmit(self.writeout, ip)
