# import all patterns availble for use.
from patterns.Patterns import *

pixelMatrix = "pixelmatrix"
raspberrypi = "192.168.2.42"
michiel_laptop = "192.168.1.199"
local_host = "127.0.0.1"
broadcast = "10.42.255.255"
matrix = "10.42.4.139"
dest = local_host

TARGETS = {
    # dest: FillTest(),
    # dest: Sven(),
    # dest: BarberpolePattern(),
    # dest: OldTron(),
    # dest: Tron(),
    # dest: Snake(speed=17),
    # # MixedLife() doesn't work atm but will be fixed
    # dest: MixedLife(),
    # dest: RandomLife(),
    # dest: RedLife(),
    # dest: BlueLife(),
    # dest: GreenLife(),
    # dest: SuperPixelBros(),
    # dest: Pong(speed=5),
    # dest: Pong(bcolor=(0, 0, 255), speed=3, port="USB", plugged=0),
    # dest: Pong(speed=8),
    # # needs images. wip still.
    # dest: DisplayPng(),

    dest: RainbowEffect(),
    # dest: ColorFade(),
    # dest: PlasmaFifth(),
    # dest: PlasmaFourth(),
    # dest: PlasmaFirst(),
    # dest: PlasmaSecond(),
    # dest: PlasmaThird(),
    # dest: RevolvingCircle(),
    # dest: RainPattern(chance=0.5, color=(255, 255, 255)),
    # dest: GraphicsCircleTest(),
    # dest: GraphicsRectTest(),
    # dest: GraphicsLineTest(),
    # dest: GraphicsPixelTest(),
    # dest: GraphicsDotTest(),
    # dest: VUmeterThree(),
}
