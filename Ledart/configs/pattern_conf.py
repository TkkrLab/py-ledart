# import all patterns availble for use.
import os
from Ledart.Lmcp import *
from Ledart.Artnet import *
from Ledart.utils import matrix
from Ledart.Patterns.Patterns import *
from Ledart.MatrixSim.MatrixScreen import MatrixScreen, interface_opts

pixelmatrix = "Arduino-42"
ledboard = 'ledboard'
minimatrix = 'minimatrix'
megamatrix = 'megamatrix'
localhost = "127.0.0.1"
bcast = '10.42.0.0'
moo = 'moo'

dest = megamatrix
# width, height = 17, 10
width, height = 128, 64
dims = matrix(x=0, y=0, width=width, height=height)

# protocol = LegacyLmcp(dispmode=grayscale)
# protocol = LegacyLmcp(dispmode=rgb24)

matrixsim = MatrixScreen(dims=dims,
                         pixelsize=7,
                         fullscreen=False,
                         interface=interface_opts["pygame"])

targets = {
    # dest: Ca(dims=dims),
    # dest: FillTest(dims=dims),
    # dest: Tron(dims=dims),
    # dest: Snake(dims=dims, speed=17),
    # dest: MixedLife(dims=dims),
    # dest: ProgressedLife(dims=dims, decay=30),
    # dest: GraphicsLineScroll(dims=dims),
    # dest: RandomLife(dims=dims),
    # dest: Mandelbrot(dims=dims),
    # dest: Sim(dims=dims),
    # dest: PixelLife(dims=dims, color=(0, 0, 0xFF)),
    # dest: SuperPixelBros(dims=dims),
    # dest: Pong(dims=dims, speed=5),
    # dest: Pong(dims=dims, speed=8),
    # dest: ScreenCapture(dims=dims, fullscreen=True),
    # dest: ScreenCapture(dims=dims, fullscreen=False),
    # dest: DisplayImage(dims=dims, fname='/home/duality/Pictures/tkkrlab.png'),
    # dest: DisplayImage(dims=dims, fname='/home/duality/Pictures/System-Shock-2.jpg'),
    # dest: VideoPlay(dims=dims, fname='/home/duality/Videos/bad-noshadow.mp4'),
    # dest: VideoPlay(dims=dims, fname='/home/duality/Videos/bad.mkv'),
    # dest: CamCapture(dims=dims),
    # dest: Water(dims=dims),
    # dest: AliasedWPlasma(dims=dims),
    # dest: AliasedFire(dims=dims),
    # dest: MiniFire(dims=dims),
    # dest: TestPlasma(dims=dims),
    # dest: Smolders(dims=dims),
    # dest: FireOne(dims=dims),
    # dest: FireTwo(dims=dims),
    # dest: FireThree(dims=dims),
    # dest: RainbowEffect(dims=dims),
    # dest: ColorFade(dims=dims),
    # dest: PlasmaFirst(dims=dims),
    # dest: PlasmaSecond(dims=dims),
    # dest: PlasmaThird(dims=dims),
    # dest: RevolvingCircle(dims=dims),
    # dest: RainPattern(dims=dims, chance=0.7, color=(40, 60, 255)),
    # dest: GraphicsCircleTest(dims=dims),
    # dest: GraphicsRectTest(dims=dims),
    # dest: GraphicsLineTest(dims=dims),
    # dest: GraphicsPixelTest(dims=dims),
    # dest: GraphicsDotTest(dims=dims),
    # dest: VUmeter(dims=dims)
    dest: Fft(dims=dims)
}