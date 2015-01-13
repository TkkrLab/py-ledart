#import patters here if they are in a different file.

#ohm led poles.
from PolicePattern import PolicePattern
from BarberpolePattern import BarberpolePattern
from ColorFadePattern import ColorFadePattern

#for ledmatrix
#patterns that don't use pygame

from RainPattern import *
from PixelLife import *
from FallingStar import *
from Plasma import *

try:
    from DisplayPng import *
except Exception, e:
    print e

#patterns that do use pygame
try:
    from Pong import *
except Exception, e:
    print e
try:
    from Tron import *
    from Snake import *
except Exception, e:
    print e