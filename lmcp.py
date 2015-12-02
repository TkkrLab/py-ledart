import socket
import time

LMCP_PORT = 1337

lmcp_sock = None

writeout = chr(0x01)
draw = chr(0x10)
draw_image = chr(0x11)

send_timeout = 0.00


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


def send_packet(data=None, pos=(0, 0), target=None):
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
