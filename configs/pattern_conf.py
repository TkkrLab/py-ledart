#import all patterns availble for use.
from patterns.Patterns import *

pixelMatrix = "pixelmatrix"
michiel_laptop = "10.42.4.12"
local_host = "127.0.0.1"

TARGETS = {
	#pixelMatrix:OldTron(),
	#pixelMatrix:Tron(),
	
	#local_host:MixedLife(),
	#local_host:RandomLife(),
	#local_host:BlueLife(),
	
	pixelMatrix:Pong(),
	#pixelMatrix:BlueLife(),
	
	#local_host:FallingStar(chance=0.2),
	#local_host:RainPattern(chance=0.2),
	
	#pixelMatrix:GraphicsCircleTest(),
	#pixelMatrix:GraphicsRectTest(),
	#pixelMatrix:GraphicsLineTest(),
	#pixelMatrix:GraphicsPixelTest(),
}
