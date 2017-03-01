# import all patterns availble for use.
import os
from Ledart.Lmcp import *
from Ledart.Ffmpegstreamer import *
from Ledart.Artnet import *
from Ledart.utils import matrix
from Ledart.MatrixSim.MatrixScreen import MatrixScreen, interface_opts

pixelmatrix = "Arduino-42"
ledboard = 'ledboard'
minimatrix = 'minimatrix'
megamatrix = 'megamatrix'
localhost = "127.0.0.1"
bcast = '10.42.0.0'
moo = 'moo'

dest = minimatrix
# dest = localhost
# width, height = 17, 10
# width, height = 128, 64
width, height = 64, 32
# pixelsize = 1024 / 128
# height = (768 - 20) / pixelsize
# width, height = 256, 128
dims = matrix(x=0, y=0, width=width, height=height)

# protocol = LegacyLmcp(dispmode=grayscale)
# protocol = LegacyLmcp(dispmode=rgb24)
# protocol = StreamPlay(dims=dims)
protocol = Stream(dims=dims)

# matrixsim = MatrixScreen(dims=dims,
#                          pixelsize=8,
#                          fullscreen=False,
#                          interface=interface_opts["pygame"])

targets = {
    # dest: MetaBalls(dims=dims)
    # dest: Ca(dims=dims),
    # dest: MixedLife(dims=dims),
    # dest: ProgressedLife(dims=dims, decay=5),
    # dest: CProgressedLife(dims=dims, decay=1),
    dest: PixelLife(dims=dims, color=(0, 0, 0xFF)),
    # dest: RandomLife(dims=dims),

    # dest: Mandelbrot(dims=dims),
    # dest: Sim(dims=dims),
    
    # dest: SuperPixelBros(dims=dims),
    # dest: Tron(dims=dims),
    # dest: Snake(dims=dims, speed=17),
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
    
    # dest: AliasedFire(dims=dims),
    # dest: MiniFire(dims=dims),
    # dest: Smolders(dims=dims),
    # dest: FireOne(dims=dims),
    # dest: FireTwo(dims=dims),
    # dest: FireThree(dims=dims),
    
    # dest: RainbowEffect(dims=dims),
    # dest: ColorFade(dims=dims),
    
    # dest: Plasma(dims=dims),
    # dest: RevolvingCircle(dims=dims),

    # dest: RainPattern(dims=dims, chance=0.7, color=(40, 60, 255)),

    # dest: GraphicsCircleTest(dims=dims),
    # dest: GraphicsRectTest(dims=dims),
    # dest: GraphicsLineTest(dims=dims),
    # dest: GraphicsPixelTest(dims=dims),
    # dest: GraphicsDotTest(dims=dims),
    # dest: GraphicsLineScroll(dims=dims),
    # dest: FillTest(dims=dims),
    
    # dest: SpiroGraph(dims=dims, mode=0),
    # dest: SpiroGraph(dims=dims, mode=1),
    # dest: SpiroGraph(dims=dims, mode=2),
    # dest: MetaBalls(dims=dims),

    # dest: VUmeter(dims=dims, mode=0),
    # dest: VUmeter(dims=dims, mode=1),
    # dest: VUmeter(dims=dims, mode=2),
    # dest: VUmeter(dims=dims, mode=3),
    
    # dest: RandomWalker(dims=dims),
    # dest: PerlinTest(dims=dims),

    # dest: Fft(dims=dims, mode=1),
    # dest: Fft(dims=dims, mode=2),
    # dest: Fft(dims=dims, mode=3),
    # dest: Fft(dims=dims, mode=4),

    # 1: Fft(dims=matrix(0, 0, 64, 32), mode=1),
    # 2: Fft(dims=matrix(0, 32, 64, 32), mode=2),
    # 3: Fft(dims=matrix(64, 0, 64, 32), mode=3),
    # 4: Fft(dims=matrix(64, 32, 64, 32), mode=4),
}
