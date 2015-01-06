import argparse, socket, time
import imp, signal, sys, os

#first things first make sure we are able to find the necesary files we need.
cwd = os.getcwd()
sys.path.append(cwd)
sys.path.append(cwd+"/patterns/Graphics/")

from artnet import buildPacket
from convert import convertSnakeModes
from MatrixSim.MatrixScreen import *

UDP_PORT = 6453

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--delay", help="controlle flow speed.", metavar="<delay>", nargs="?", default=0.15, type=float)
parser.add_argument("-c", "--config", help="load config.", metavar="<config_conf.py>", nargs="?", default="default_conf.py", type=str)
parser.add_argument("--snakeMode", help="flips every x amount of data", nargs="?", default=None, type=str)
parser.add_argument("--matrixSim", help="turns on buildin matrix simulation", nargs="?", default=None, type=str)
args = parser.parse_args()


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
	matrixscreen = MatrixScreen(matrix_width, matrix_height, 30)

while(True):
	for t in TARGETS:
		pattern = TARGETS[t]
		data = pattern.generate()
		#convert the data for the special matrix layout.
		if args.snakeMode == "enabled":
			data = convertSnakeModes(data)
		#if this is a simulation draw it to the matrixscreen else 
		#send it out over the network.
		if args.matrixSim:
			matrixscreen.process(data)
		sock.sendto(buildPacket(0, data), (t, UDP_PORT))
	time.sleep(args.delay)
sock.close()
