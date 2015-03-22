"""
basicly some code that lets you send stuff to the dongle on the pi.
"""
import random
import serial

ser = serial.Serial("/dev/ttyACM1", 115200, interCharTimeout=0.009)
speed = 6
xpos = 0
nextpos = 128

while(True):
    # ser.write(chr(128))
    if ser.inWaiting():
        if ser.read() == 'n':
            if xpos > 0xFF:
                xpos = 0xFF
            if xpos < 0:
                xpos = 0
            ser.write(chr(xpos))
            if (xpos == nextpos or xpos == nextpos+random.randint(0, speed+1) or xpos == nextpos-random.randint(0, speed+1)):
                nextpos = random.randint(0, 0xFF)
            elif xpos != nextpos:
                if xpos < nextpos:
                    xpos += speed
                elif xpos > nextpos:
                    xpos -= speed
            print("Next: %s Current: %s" % (nextpos, xpos))
