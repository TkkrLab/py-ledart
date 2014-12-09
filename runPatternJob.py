import argparse, socket, time
import imp, signal, sys

from artnet import buildPacket
from convert import convertSnakeModes

UDP_PORT = 6453

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--delay", help="controlle flow speed.", metavar="<delay>", nargs="?", default=0.15, type=float)
parser.add_argument("-c", "--config", help="load config.", metavar="<config_conf.py>", nargs="?", default="default_conf.py", type=str)
args = parser.parse_args()


#the bit below here allows loading of the config files specified by --config written by Duality
package = "configs"
fp, path, description = imp.find_module(package)
fp, path, description = imp.find_module(str(args.config)[:-3], [path])
config = imp.load_module("configuration", fp, path, description)
TARGETS = config.TARGETS
#---------

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)

def signal_handler(signal, frame):
	print "\nCaught Ctrl-C closing connections."
	sock.close()
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

while(True):
	for t in TARGETS:
		pattern = TARGETS[t]
		data = pattern.generate()
		data = convertSnakeModes(data)
		sock.sendto(buildPacket(0, data), (t, UDP_PORT))
	time.sleep(args.delay)
sock.close()
