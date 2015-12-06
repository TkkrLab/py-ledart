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

send_timeout = 0.000


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


def chunked(data, chunksize):
    """ yield sections 'chunks' of data, with iteration count."""
    chunk = []
    it = 0
    while(it < (len(data) / chunksize)):
        index = (it * chunksize)
        chunk = data[index:(index + chunksize)]
        yield (it, chunk)
        it += 1


def chunk_is_empty(chunk):
    for color in chunk:
        for c in color:
            if c != 0x00:
                return False
    return True


def _send_packet(data=None, target=None):
        """ this function sends 8 vertical lines at ones."""
        for (row, chunk) in chunked(data, data.get_width() * 8):
            if not chunk_is_empty(chunk):
                packet = draw + chr(row) + compress(chunk)
                lmcp_sock.sendto(packet, target)
                time.sleep(send_timeout)
        time.sleep(send_timeout)
        lmcp_sock.sendto(writeout, target)


def send_packet(data=None, pos=(0, 0), target=None):
    """ this functon sends every vertical line. """
    if data.get_size() == matrix_size:
        _send_packet(data, target)
    else:
        x, y = pos
        width = data.get_width()
        # draw in chunks
        for (i, chunk) in chunked(data, width):
            packet = (draw_image + chr(x) + chr(y + i) +
                      chr(width) + chr(0x01))
            packet += compress(chunk)
            lmcp_sock.sendto(packet, target)
            time.sleep(send_timeout)
        time.sleep(send_timeout)
        lmcp_sock.sendto(writeout, target)


def open():
    global lmcp_sock
    lmcp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def send(data, ip):
    if lmcp_sock is None:
        raise(Exception("Socket not created. "))
    send_packet(data=data, pos=(0, 0), target=(ip, LMCP_PORT))


def set_port(port):
    global LMCP_PORT
    LMCP_PORT = port


def close():
    lmcp_sock.close()
