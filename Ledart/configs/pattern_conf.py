# import all patterns availble for use.
import os
from Ledart.Lmcp import *
from Ledart.Artnet import *
from Ledart.stripinfo import *
from Ledart.MatrixSim.MatrixScreen import MatrixScreen, interface_opts

pixelmatrix = "Arduino-42"
ledboard = 'ledboard'
minimatrix = 'minimatrix'
megamatrix = 'megamatrix'
localhost = "127.0.0.1"
bcast = '10.42.0.0'
moo = 'moo'
dest = megamatrix
width, height = 128, 64
# width, height = 128, 64
dims = matrix(x=0, y=0, width=width, height=height)
# dims = matrixstrip(x=0, y=0, width=32, height=32)
set_strip_dimensions(dims)
# protocol = LegacyLmcp(dispmode=grayscale)
protocol = LegacyLmcp(dispmode=rgb24)

"""
matrixsim = MatrixScreen(width=width,
                         height=height,
                         pixelsize=2,
                         fullscreen=False,
                         interface=interface_opts["opengl"])
"""
from Ledart.Patterns.Patterns import *

targets = {
    # dest: FillTest(),
    # dest: Sven(),
    # dest: OldTron(),
    # dest: Tron(),
    # dest: Snake(speed=17),
    # dest: MixedLife(),
    # dest: ProgressedLife(decay=30),
    # dest: GraphicsLineScroll(),
    # dest: RandomLife(),
    # dest: Mandelbrot(),
    # dest: Sim(),
    # dest: PixelLife(color=(0, 0, 0xFF)),
    # dest: SuperPixelBros(),
    # dest: Pong(speed=5),
    # dest: Pong(speed=8),
    # dest: ScreenCapture(fullscreen=True),
    # dest: ScreenCapture(fullscreen=False),
    # dest: DisplayImage(basedir + '/images/tkkrlab.png'),
    dest: DisplayImage('/home/duality/System-Shock-2.jpg'),
    # dest: DisplayGif('/home/robert/1353.gif'),
    # dest: VideoPlay('/home/robert/Videos/bad-noshadow.mp4'),
    # dest: VideoPlay('/home/robert/Videos/bad.mkv'),
    # dest: VideoTest(),
    # dest: CamCapture(),
    # dest: Water(),
    # dest: AliasedWPlasma(),
    # dest: AliasedFire(),
    # dest: MiniFire(),
    # dest: TestPlasma(),
    # dest: Smolders(),
    # dest: FireOne(),
    # dest: FireTwo(),
    # dest: FireThree(),
    # dest: RectTest(),

    # dest: RainbowEffect(),
    # dest: ColorFade(),
    # dest: PlasmaFifth(),
    # dest: PlasmaFourth(),
    # dest: PlasmaFirst(),
    # dest: PlasmaSecond(),
    # dest: PlasmaThird(),
    
    # dest: RevolvingCircle(),
    # dest: RainPattern(chance=0.7, color=(40, 60, 255)),

    # dest: GraphicsCircleTest(),
    # dest: GraphicsRectTest(),
    # dest: GraphicsLineTest(),
    # dest: GraphicsPixelTest(),
    # dest: GraphicsDotTest(),
    # dest: VUmeter(),
}
