"""
basicly some code that lets you send stuff to the dongle on the pi.
"""
import random
import serial

ser = serial.Serial("/dev/ttyACM0", 115200, interCharTimeout=0.009)
speed = 10
xpos = 0
nextpos = 128

while(True):
    if ser.inWaiting():
        ser.write(chr(xpos))
        if (xpos == nextpos or xpos == nextpos+random.randint(0, speed+1) or xpos == nextpos-random.randint(0, speed+1)):
            nextpos = random.randint(0, 0xFF)
        elif xpos != nextpos:
            if xpos < nextpos:
                xpos += speed
            elif xpos > nextpos:
                xpos -= speed
        if xpos > 0xFF:
            xpos = 0xFF
        if xpos < 0:
            xpos = 0
