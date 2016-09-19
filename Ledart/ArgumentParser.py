import argparse

def add_argument(argument, type=int, default=None, help="", metavar="<>"):
    parser.add_argument(argument, help=help, metavar=metavar, nargs="?", default=default, type=type)

def get_args():
    return parser.parse_args()

parser = argparse.ArgumentParser()

# job options
parser.add_argument("--fps",
                    help="control flow speed. if 0 fps is fastest possible.",
                    metavar="<fps>",
                    nargs="?",
                    default=25,
                    type=float)

parser.add_argument("--config",
                    help="load config.",
                    metavar="<pathto/config.py>",
                    nargs="?",
                    default="default_conf.py",
                    type=str)

parser.add_argument("--sendOnChange",
                    help="if set sending on changed frames is enabled.",
                    action="store_true")


parser.add_argument("--showFps",
                    help="prints out the actual fps the program runs at",
                    action="store_true")

parser.add_argument("--testing",
                    help="if set will run some tests and log to stdout if debug is enabled.",
                    action="store_true")

parser.add_argument("--list",
                    help="lists valid patterns with generate functions.",
                    action="store_true")

parser.add_argument("--debug",
                    help="allows patterns and other code to print debug information.",
                    action="store_true")

# enable alpha interactive editor.
# parser.add_argument("--gui",
#                     help="enables the graphical interface.",
#                     metavar="<enabled>",
#                     nargs="?",
#                     default="disabled",
#                     type=str)
