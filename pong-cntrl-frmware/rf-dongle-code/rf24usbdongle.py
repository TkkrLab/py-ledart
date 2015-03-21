"""
basicly some code that lets you send stuff to the dongle on the pi.
"""
import time
import random
import serial
ser = serial.Serial("/dev/ttyACM1", 115200)
speed = 1
xpos = 0
nextpos = 128
current = time.clock()
previous = 0
# interval in seconds
interval = 0.005
while(True):
    if ser.inWaiting() and (ser.read(1) == 'n'):
        ser.write(chr(xpos)+chr(128))
        current = time.clock()
        if((current - previous) >= interval):
            previous = current
            if xpos != nextpos:
                if xpos < nextpos:
                    xpos += speed
                elif xpos > nextpos:
                    xpos -= speed
            elif xpos == nextpos:
                nextpos = random.randint(0, 0xFF)
            print("next: %s Current: %s" % (nextpos, xpos))
    else:
        ser.flush()
