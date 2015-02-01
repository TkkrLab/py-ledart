#import patters here if they are in a different file.

#ohm led poles.
from PolicePattern import PolicePattern
from BarberpolePattern import BarberpolePattern
from ColorFadePattern import ColorFadePattern

#for ledmatrix
#patterns that don't use pygame

from RainPattern import *
from PixelLife import *
from Plasma import *

#uses pygame for testing.
try:
	from SuperPixelBros import *
except Exception, e:
	print "PixelBros>>"+str(e)
#this one uses a library png so try to load.
#but if not installed pass.
try:
    from DisplayPng import *
except Exception, e:
    print "DisplayPng>>"+str(e)

#patterns that do use pygame
try:
	from Pong import *
except Exception, e:
    print "Pong>>"+str(e)

try:
    from Tron import *
except Exception, e:
	print "Tron>>"+str(e)
try:
    from Snake import *
except Exception, e:
    print "snake>>"+str(e)
