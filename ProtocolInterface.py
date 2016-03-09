"""
    this file implements a abstraction layer for the network interface,
    of protocols, and also a 'interface' so that implementing protocols like
    artnet or lmcp or any costum protoc becomes easier.
"""

import socket
import select

class Interface(object):
    def __init__(self, args, port=1337):
        self.port = port
        self.open()

    def set_port(self, port):
        self.port = port
        self.open()

    def get_port(self):
        return self.port

    def open(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setblocking(0)

    def transmit(self, data, ip):
        target = (ip, self.port)
        readable, writable, exceptional = select.select([self.sock],
                                                        [self.sock],
                                                        [self.sock])
        for w in writable:
            w.sendto(data, target)
        # self.sock.sendto(data, target)

    def send(self, data, ip):
        """
            overide this function so that you can compress or pack,
            your data correctly, and/or add header data.
        """
        self.transmit(str(data), ip)

    def close(self):
        self.sock.close()
