# import all patterns availble for use.
import os
from Ledart.Lmcp import *
from Ledart.Artnet import *
from Ledart.stripinfo import *
from Ledart.MatrixSim.MatrixScreen import MatrixScreen, interface_opts

pixelmatrix = '192.168.1.116'
dest = megamatrix

width, height = 17, 10
dims = matrix(x=0, y=0, width=width, height=height)
set_strip_dimensions(dims)
protocol = Pixelmatrix()

from Ledart.Patterns.Patterns import *

targets = {
    dest: Pong(speed=8, select=(0, 0)),
}
