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
interval = 0.05
while(True):
    current = time.clock()
    if((current - previous) >= interval):
        ser.write(chr(xpos))
        previous = current
        if xpos != nextpos:
            if xpos < nextpos:
                xpos += speed
            elif xpos > nextpos:
                xpos -= speed
        elif xpos == nextpos:
            nextpos = random.randint(0, 0xFF)
        print("next: %s Current: %s" % (nextpos, xpos))
