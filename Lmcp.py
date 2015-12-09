"""
    author: Duality
    protocol author: Jawsper
    https://github.com/jawsper

    this file describes a protocol that implements,
    part of the documented lcmp protocol,
    because only part is needed for the working of
    py-ledart software.

    notice though that sending packets to ledboard,
    is slow. because we have to keep in mind,
    that the ledboard has to process them.
    thus sending is limited.

"""
import socket
import time
from matrix import matrix_size

LMCP_PORT = 1337

lmcp_sock = None

writeout = chr(0x01)
draw = chr(0x10)
draw_image = chr(0x11)

send_timeout = 0.0


def chunk_is_empty(chunk):
    for color in chunk:
        for c in color:
            if c != 0x00:
                return False
    return True


def chunked(data, chunksize):
    """ yield sections 'chunks' of data, with iteration count."""
    chunk = []
    it = 0
    while(it < (len(data) / chunksize)):
        index = (it * chunksize)
        chunk = data[index:(index + chunksize)]
        yield (it, chunk)
        it += 1


class Lmcp(object):
    def __init__(self, args, port=1337):
        self.args = args
        self.port = port
        self.max_send_size = 1024
        self.writeout = chr(0x01)
        self.draw = chr(0x10)
        self.draw_image = chr(0x11)
        self.open()

    def open(self):
        self.lmcp_socket = socket.socket(socket.AF_INET,
                                         socket.SOCK_DGRAM)

    def set_port(self, port):
        self.port = port
        self.open()

    def close(self):
        self.lmcp_socket.close()

    def compress(self, data):
        compressed = ''
        for color in data:
            compressed += chr(sum(color) / 3)
        return compressed

    def transmit(self, packet, target):
        self.lmcp_socket.sendto(packet, target)

    def send_packet(self, data, target):
        if data.get_size() == matrix_size:
            """ send the whole surface in chunks of matrix_width * 8"""
            for (row, chunk) in chunked(data, data.get_width() * 8):
                # if not chunk_is_empty(chunk):
                    packet = self.draw + chr(row) + self.compress(chunk)
                    self.lmcp_socket.sendto(packet, target)
            self.lmcp_socket.sendto(self.writeout, target)
        else:
            x, y = data.get_d_offset()
            width = data.get_width()
            height = data.get_height()
            size = data.size
            """ check if we can send it all at once."""
            if size < 1020:
                packet = (self.draw_image + chr(x) + chr(y) +
                          chr(width) + chr(height))
                packet += self.compress(data)
                self.lmcp_sock.sendto(packet, target)
                self.lmcp_sock.sendto(writeout, target)
                return

            """ else chunk it up and send in chunks."""
            if height < 8:
                chunkheight = height
            elif not (height % 8) and not (width % 8):
                chunkheight = 8
            else:
                chunkheight = height / 8

            for (i, chunk) in chunked(data, width * chunkheight):
                packet = (self.draw_image + chr(x) +
                          chr((y + i) * chunkheight) +
                          chr(width) + chr(0x01 * chunkheight))
                packet += self.compress(chunk)
                self.lmcp_socket.sendto(packet, target)
            self.lmcp_socket.sendto(writeout, target)

    def send(self, data, ip):
        target = (ip, self.port)
        self.send_packet(data, target)


def compress(data):
    """ 'compress' a list of data in to a single string of bytes."""
    compressed = ''
    average = 0
    for i, value in enumerate(data):
        average = 0
        for c in value:
            average += c
        average = average / 3
        compressed += chr(average)
    return compressed


def _send_packet(data=None, target=None):
        """ send the whole surface in chunks of matrix_width * 8"""
        for (row, chunk) in chunked(data, data.get_width() * 8):
            # if not chunk_is_empty(chunk):
                packet = draw + chr(row) + compress(chunk)
                lmcp_sock.sendto(packet, target)
        lmcp_sock.sendto(writeout, target)


def send_packet(data=None, target=None):
    """ if the surface is as big as the matrix we can send it all at once."""
    if data.get_size() == matrix_size:
        _send_packet(data, target)
    else:
        x, y = data.get_d_offset()
        width = data.get_width()
        height = data.get_height()
        size = data.size
        """ check if we can send it all at once."""
        if size < 1020:
            packet = (draw_image + chr(x) + chr(y) +
                      chr(width) + chr(height))
            packet += compress(data)
            lmcp_sock.sendto(packet, target)
            time.sleep(send_timeout)
            lmcp_sock.sendto(writeout, target)
            time.sleep(send_timeout)
            return

        """ else chunk it up and send in chunks."""
        if height < 8:
            chunkheight = height
        elif not (height % 8) and not (width % 8):
            chunkheight = 8
        else:
            chunkheight = height / 8

        for (i, chunk) in chunked(data, width * chunkheight):
            packet = (draw_image + chr(x) + chr((y + i) * chunkheight) +
                      chr(width) + chr(0x01 * chunkheight))
            packet += compress(chunk)
            lmcp_sock.sendto(packet, target)
        lmcp_sock.sendto(writeout, target)


def open():
    global lmcp_sock
    lmcp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def send(data, ip):
    if lmcp_sock is None:
        raise(Exception("Socket not created. "))
    send_packet(data=data, target=(ip, LMCP_PORT))


def set_port(port):
    global LMCP_PORT
    LMCP_PORT = port


def close():
    lmcp_sock.close()
