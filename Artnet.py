#!/usr/bin/python

# 2013-09-02 Aprogas

# 2015-12-12 Duality:
# class struckture introduced for easy implentation of other
# protocols, and abstraction of sockets.


from ProtocolInterface import Interface


class Artnet(Interface):
    def __init__(self, args, universe=0, port=6454):
        Interface.__init__(self, args, port=port)
        self.universe = universe

    def build_packet(self, universe, dmxdata):
        # based on fire-ohmlogo.py by OHM 2013
        # 3 * 1024 because r + g + b == 3 colors
        size = len(dmxdata) * 3
        if size >= (1024 - 18):
            raise(Exception("dmxdata to big to fit packet."))
        #              01234567   8   9   a   b   c   d   e   f   10  11
        #                         op-code protver seq phy universe len
        data = bytearray("Art-Net\x00\x00\x50\x00\x0e\x00\x00")
        data += chr(int(universe % 256))
        data += chr(int(universe / 256))
        data += chr(int(size / 256))
        data += chr(int(size % 256))
        data += str(dmxdata)
        return data

    def send(self, data, ip):
        data = self.build_packet(self.universe, data)
        self.transmit(data, ip)