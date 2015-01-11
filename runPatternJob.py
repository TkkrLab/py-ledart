import argparse, socket, time
import imp, signal, sys

from artnet import buildPacket
from matrix import *

UDP_PORT = 6454

parser = argparse.ArgumentParser()
parser.add_argument("--delay", help="controlle flow speed.", metavar="<delay>", nargs="?", default=0.15, type=float)
parser.add_argument("--config", help="load config.", metavar="<config_conf.py>", nargs="?", default="default_conf.py", type=str)
parser.add_argument("--snakeMode", help="flips every x amount of data", nargs="?", default=None, type=str)
parser.add_argument("--matrixSim", help="turns on buildin matrix simulation", nargs="?", default=None, type=str)
parser.add_argument("--pixelSize", help="sets the pixel size for the matrix sim", nargs="?", default=30, type=int)
parser.add_argument("--netSilent", help="if enabled won't send out udp packets anywhere", nargs="?", default=None, type=str)
#parser.add_argument("--matrixSize", help="set the width and hight of matrix for exampel: --matrixSize=10,17", nargs="+", type=int)
args = parser.parse_args()

if args.matrixSim:
	from MatrixSim.MatrixScreen import *

#the bit below here allows loading of the config files specified by --config written by Duality
package = "configs"
fp, path, description = imp.find_module(package)
fp, path, description = imp.find_module(str(args.config)[:-3], [path])
config = imp.load_module("configuration", fp, path, description)
TARGETS = config.TARGETS
#---------

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setblocking(False)
#sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)

def signal_handler(signal, frame):
	print "\nCaught Ctrl-C closing connections."
	sock.close()
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

#setup a screen if matrixSim argument was set.
if args.matrixSim:
	matrixscreen = MatrixScreen(matrix_width, matrix_height, args.pixelSize)

while(True):
	for t in TARGETS:
		pattern = TARGETS[t]
		data = pattern.generate()
		#convert the data for the special matrix layout.
		if args.snakeMode == "enabled":
			data = convertSnakeModes(data)
		#if this is a simulation draw it to the matrixscreen else 
		#send it out over the network.
		if not args.netSilent:
			sock.sendto(buildPacket(0, data), (t, UDP_PORT))
		if args.matrixSim:
			if args.snakeMode:
				matrixscreen.process(convertSnakeModes(data))
			else:
				matrixscreen.process(data)
	time.sleep(args.delay)
sock.close()
