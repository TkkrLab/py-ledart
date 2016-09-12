# import all patterns availble for use.
from Ledart.Lmcp import *
from Ledart.Artnet import *
from Ledart.stripinfo import *
from Ledart.MatrixSim.MatrixScreen import MatrixScreen, interface_opts

localhost = "localhost"
dest = localhost

width, height = 32, 32
set_strip_dimensions(matrix(0, 0, width, height))

# don't send out anything.
protocol = None
# start the simulator for a nice demo.
matrixsim = MatrixScreen(width=width,
                         height=height,
                         pixelsize=10,
                         fullscreen=False,
                         interface=interface_opts["pygame"])

from Ledart.Patterns.Patterns import *

targets = {
    dest: PixelLife(color=(0, 0, 0xff)),
}
