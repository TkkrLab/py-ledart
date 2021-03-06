"""
implementations of device abstractions like networking (sockets)
or theoretically serial or any other way for communicating with your
led/lighting devices.
"""

import socket
import select
import numpy


class TcpSocket(object):
    """
    Future definition. place holder to save idea.
    """
    def __init__(self, port=1337):
        pass

    def open(self):
        pass

    def bcast(self):
        pass

    def transmit(self, data, dest):
        pass

    def send(self, data, dest):
        pass

    def close(self):
        pass


class UdpSocket(object):
    """
    A standard not mandatory Interface
    Which currently only implements an abstraction for socket.
    That makes it a bit easier to implement Network based communication.
    """
    def __init__(self, port=1337):
        self.port = port

    def open(self):
        """
        opens a socket for communication
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('', self.port))

    def bcast(self, data):
        """
        broadcasts data over network.
        """
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.transmit(data, '255.255.255.255')

    def transmit(self, data, dest):
        """
        Transmit (data) byte stream to dest.
        """
        target = (dest, self.port)
        data = numpy.array(data, dtype='uint8')
        self.sock.sendto(data, target)

    def send(self, data, dest):
        """
        Possibly override this function to implement device and protocol specifics.
        """
        self.transmit(data, dest)

    def close(self):
        self.sock.close()
