#import all patterns availble for use.
from patterns.Patterns import *

pixelMatrix = "pixelmatrix"
raspberrypi = "192.168.2.42"
michiel_laptop = "10.42.4.12"
local_host = "127.0.0.1"
broadcast = "10.42.255.255"

TARGETS = {
    #local_host:BarberpolePattern(),
    #pixelMatrix:OldTron(),
    #pixelMatrix:Tron(),
    
    #local_host:MixedLife(),
    #local_host:RandomLife(),
    #local_host:BlueLife(),
    #raspberrypi:BlueLife(),
    
    local_host:Pong(speed=5),
    pixelMatrix:Pong(speed=5),
    #pixelMatrix:Pong(speed=8),
    #pixelMatrix:Snake(),
    #pixelMatrix:BlueLife(),
    
    #local_host:FallingStar(chance=0.2),
    #local_host:RainPattern(chance=0.2),
    
    #pixelMatrix:GraphicsCircleTest(),
    #pixelMatrix:GraphicsRectTest(),
    #pixelMatrix:GraphicsLineTest(),
    #local_host:GraphicsPixelTest(),
    #local_host:GraphicsDotTest(),
}
