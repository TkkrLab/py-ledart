"""
basicly some code that lets you send stuff to the dongle on the pi.
"""
import random
import serial
ser = serial.Serial("/dev/ttyACM1", 115200, interCharTimeout=0.009)
speed = 1
xpos = 0
nextpos = 128
while(True):
    ser.write(chr(xpos))
    if xpos != nextpos:
        if xpos < nextpos:
            xpos += speed
        elif xpos > nextpos:
            xpos -= speed
    elif xpos == nextpos:
        nextpos = random.randint(0, 0xFF)
