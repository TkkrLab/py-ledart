# import all patterns availble for use.
from Ledart.Lmcp import *
from Ledart.Artnet import *
from Ledart.utils import *
from Ledart.MatrixSim.MatrixScreen import MatrixScreen, interface_opts

localhost = "atest"
dest = localhost

width, height = 32, 32
dims = matrix(0, 0, width, height)

# don't send out anything.
protocol = None
# start the simulator for a nice demo.
matrixsim = MatrixScreen(dims=dims,
                         pixelsize=7,
                         fullscreen=False,
                         interface=interface_opts["pygame"])

targets = {
    dest: PixelLife(dims=dims, color=(0, 0, 0xff)),
}
