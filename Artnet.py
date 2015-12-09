#!/usr/bin/python

# 2013-09-02 Aprogas

import socket

ARTNET_PORT = 6454

UNIVERSE = 0

artnet_sock = None


class Artnet(object):
    def __init__(self, args):
        self.args = args


def buildPacket(universe, dmxdata):
    # Stolen from fire-ohmlogo.py by OHM2013
    size = len(dmxdata) * 3
    #              01234567   8   9   a   b   c   d   e   f   10  11
    #                         op-code protver seq phy universe len
    data = bytearray("Art-Net\x00\x00\x50\x00\x0e\x00\x00")
    data += chr(int(universe % 256))
    data += chr(int(universe / 256))
    data += chr(int(size / 256))
    data += chr(int(size % 256))
    data += str(dmxdata)
    return data


def open():
    global artnet_sock
    artnet_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def send(data, ip):
    if artnet_sock is None:
        raise(Exception("Socket not created. "))
    artnet_sock.sendto(buildPacket(UNIVERSE, data), (ip, ARTNET_PORT))


def set_universe(universe):
    global UNIVERSE
    UNIVERSE = universe


def set_port(port):
    global ARTNET_PORT
    ARTNET_PORT = port


def close():
    artnet_sock.close()
