import argparse

def add_argument(argument, type=int, default=None, help="", metavar="<>"):
    parser.add_argument(argument, help=help, metavar=metavar, nargs="?", default=default, type=type)

def get_args():
    return parser.parse_args()

parser = argparse.ArgumentParser()

# job options
parser.add_argument("--fps",          help="control flow speed. if 0 fps is fastest possible.",                                             metavar="<fps>",                   nargs="?", default=25,                  type=float)
parser.add_argument("--config",       help="load config.",                                                                                  metavar="<config_conf.py>",        nargs="?", default="default_conf.py",   type=str)
parser.add_argument("--showFps",      help="prints out the actuall fps the program runs at",                                                metavar="<enabled>",               nargs="?", default="disabled",          type=str)
parser.add_argument("--sendOnChange", help="select sending on change.",                                                                     metavar="<disabled>",              nargs="?", default="disabled",          type=str)
parser.add_argument("--netProtocol",  help="select on which protocol to send. each keeps track how and what to send.",                      metavar="<artnet, lmcp>",          nargs="?", default="artnet",            type=str)

# send grayscale or not.
parser.add_argument("--color",        help="by default everything is grayscaled, if this option is enabled it will send in color.",         metavar="<enabled>",               nargs="?", default="disabled",          type=str)

# enable alpha interactive editor.
parser.add_argument("--gui",          help="enables the graphical interface.",                                                              metavar="<enabled>",               nargs="?", default="disabled",          type=str)

# testing/debugging
parser.add_argument("--testing",      help="if enabled will run some tests and log to stdout",                         action="store_true")
parser.add_argument("--list",         help="lists patterns with generate functions",                                   action="store_true")

# matrix simulator
parser.add_argument("--matrixSim",    help="turns on buildin matrix simulation",                                                            metavar="<enabled>",               nargs="?", default="disabled",          type=str)
parser.add_argument("--pixelSize",    help="sets the pixel size for the matrix sim",                                                        metavar="<PixelSize>",             nargs="?", default=10,                  type=int)
parser.add_argument("--netSilent",    help="if enabled won't send out udp packets anywhere",                                                metavar="<enabled>",               nargs="?", default="disabled",          type=str)
parser.add_argument("--fullscreen",   help="makes matrixsim go fullscreen (hides mouse pointer)",                                           metavar="<enabled>",               nargs="?", default="disabled",          type=str)
parser.add_argument("--simInterface", help="lets you choose the simulator drawing interface",                                               metavar="<pygame, opengl, dummy>", nargs="?", default="pygame",            type=str)


# tty controller
add_argument("--ttyport", type=str, default="USB0", help="select serial port", metavar="/dev/tty<port>")
add_argument("--ttybaud", type=int, default=115200, help="set serial baudrate", metavar="<baud>")
add_argument("--ttydebug", type=bool, default=False, help="enabled debugging output for serial.", metavar="<True, False>")