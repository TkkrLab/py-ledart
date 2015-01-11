#import patters here if they are in a different file.

#ohm led poles.
from PolicePattern import PolicePattern
from BarberpolePattern import BarberpolePattern
from ColorFadePattern import ColorFadePattern

#for ledmatrix
#patterns that don't use pygame

from RainPattern import RainPattern
from PixelLife import *
from FallingStar import FallingStar

#patterns that do use pygame
try:
	from Tron import Tron
	from Snake import Snake
	from Pong import Pong
except Exception, e:
	print e