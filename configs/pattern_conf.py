#import all patterns availble for use.
from patterns.Patterns import *

pixelMatrix = "pixelmatrix"
raspberrypi = "192.168.2.42"
michiel_laptop = "192.168.1.199"
local_host = "127.0.0.1"
broadcast = "10.42.255.255"

TARGETS = {
    # local_host:BarberpolePattern(),
    # pixelMatrix:OldTron(),
    # pixelMatrix:Tron(),
    # local_host:Snake(speed=17),
    
    # local_host:MixedLife(),
    # local_host:RandomLife(),
    # local_host:BlueLife(),
    # raspberrypi:BlueLife(),
    
    # local_host:SuperPixelBros(),
    # local_host:Pong(speed=5),
    # pixelMatrix:Pong(speed=3),
    # pixelMatrix:Pong(speed=8),
    # pixelMatrix:Snake(),
     local_host:BlueLife(),
    # #needs images. wip still.
    # # pixelMatrix:DisplayPng(),
    # pixelMatrix:PlasmaFirst(),
    # pixelMatrix:PlasmaSecond(),
    # michiel_laptop:PlasmaSecond(),
    # pixelMatrix:PlasmaThird(),
    
    # #this one is broken somehow. not even half the code there? that was there?
    # # local_host:FallingStar(color=(255,255,255), chance=0.2),
    
    # local_host:RainPattern(chance=0.2),
    
    # pixelMatrix:GraphicsCircleTest(),
    # pixelMatrix:GraphicsRectTest(),
    # pixelMatrix:GraphicsLineTest(),
    # local_host:GraphicsPixelTest(),
    # local_host:GraphicsDotTest(),
}
