import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--fps",          help="control flow speed. if 0 fps is fastest possible.",   metavar="<fps>",                   nargs="?", default=15,                  type=float)
parser.add_argument("--config",       help="load config.",                                        metavar="<config_conf.py>",        nargs="?", default="default_conf.py",   type=str)
parser.add_argument("--snakeMode",    help="flips every x amount of data",                        metavar="<enabled>",               nargs="?", default="disabled",          type=str)
parser.add_argument("--matrixSim",    help="turns on buildin matrix simulation",                  metavar="<enabled>",               nargs="?", default="disabled",          type=str)
parser.add_argument("--pixelSize",    help="sets the pixel size for the matrix sim",              metavar="<PixelSize>",             nargs="?", default=30,                  type=int)
parser.add_argument("--netSilent",    help="if enabled won't send out udp packets anywhere",      metavar="<enabled>",               nargs="?", default="disabled",          type=str)
parser.add_argument("--showFps",      help="prints out the actuall fps the program runs at",      metavar="<enabled>",               nargs="?", default="disabled",          type=str)
parser.add_argument("--fullscreen",   help="makes matrixsim go fullscreen (hides mouse pointer)", metavar="<enabled>",               nargs="?", default="disabled",          type=str)
parser.add_argument("--gui",          help="enables the graphical interface.",                    metavar="<enabled>",               nargs="?", default="disabled",          type=str)
parser.add_argument("--simInterface", help="lets you choose the simulator drawing interface",     metavar="<pygame, opengl, dummy>", nargs="?", default="pygame",            type=str)
parser.add_argument("--testing",      help="if enabled will run some tests and log to term",      action="store_true")
parser.add_argument("--list",         help="lists patterns with generate functions",              action="store_true")


def get_args():
    return parser.parse_args()
