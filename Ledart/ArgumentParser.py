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

# enable alpha interactive editor.
parser.add_argument("--gui",          help="enables the graphical interface.",                                                              metavar="<enabled>",               nargs="?", default="disabled",          type=str)

# testing/debugging
parser.add_argument("--testing",      help="if enabled will run some tests and log to stdout.",                         action="store_true")
parser.add_argument("--list",         help="lists patterns with generate functions.",                                   action="store_true")
parser.add_argument("--debug",        help="enables patterns and other code to print debug information.",              action="store_true")


# tty controller
add_argument("--ttyport", type=str, default="USB0", help="select serial port", metavar="/dev/tty<port>")
add_argument("--ttybaud", type=int, default=115200, help="set serial baudrate", metavar="<baud>")
add_argument("--ttydebug", type=bool, default=False, help="enabled debugging output for serial.", metavar="<True, False>")

