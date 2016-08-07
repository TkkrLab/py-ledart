#!/usr/bin/env pypy

# import some generaly used libraries
import signal
import sys
import imp
import os
import time
import atexit
import traceback
from socket import gethostbyname

import cProfile

# import matrix simulator and matrix specifics
from matrix import matrix_width, matrix_height
from Tools.Graphics import Surface
from MatrixSim.MatrixScreen import interface_opts
try:
    from MatrixSim.MatrixScreen import MatrixScreen
except Exception as e:
    print("MatrixScreen>> " + str(e))
    traceback.print_exc()

from ArgumentParser import get_args

# get command line arguments
args = get_args()

# generate no byte code
sys.dont_write_bytecode = True

# setup a screen if matrixSim argument was set.
if args.matrixSim == "enabled":
    if args.fullscreen == "enabled":
        fullscreen = True
    else:
        fullscreen = False
    interface = interface_opts[args.simInterface]
    matrixscreen = MatrixScreen(matrix_width, matrix_height,
                                args.pixelSize,
                                fullscreen,
                                interface)

def get_protocol(args):
    if args.netProtocol == "artnet":
        import Artnet
        protocol = Artnet.Artnet(args)
    elif args.netProtocol == "pixelmatrix":
        import Artnet
        protocol = Artnet.Pixelmatrix(args)
    elif args.netProtocol == "lmcp":
        import Lmcp
        protocol = Lmcp.Lmcp(args)
    elif args.netProtocol == "legacylmcp":
        import Lmcp
        protocol = Lmcp.LegacyLmcp(args)
    elif args.netProtocol == "testlmcp":
        import Lmcp
        protocol = Lmcp.TestLmcp(args)
    else:
        raise(Exception("no protocol found/selected."))
    return protocol

# setup which protocol to use.
protocol = get_protocol(args)

# generate no byte code
sys.dont_write_bytecode = True

def get_trace():
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    fmt = (exc_type, fname, exc_tb.tb_lineno)
    fmtstr = "%s:%s:%s" % fmt
    return fmtstr


def find_patterns_in_dir(dir):
    patterns = []
    # get the current working directory so we.
    # can join and find it.
    dir = os.path.join(os.getcwd(), dir)
    # see if dir is already in path. else add it.
    if dir not in sys.path:
        sys.path.append(dir)
    else:
        print("directory in path.")
    # for everything in a directory.
    for item in os.listdir(dir):
        # if it is a source file.
        if item.endswith("py"):
            # extract the file name and import it.
            sfile = item.split('.')[0]
            try:
                mod = __import__(sfile)
            except Exception as e:
                print("%s:Couldn't import module cause: %s" % (sfile, e))
                continue
            # extract classes
            classes = get_pattern_classes(mod)
            # if any found:
            if classes:
                # append the object to patterns
                patterns += classes
    # return the patterns
    return list(set(patterns))


def get_pattern_classes(module):
    # holds the patterns that are found
    patterns = []
    # look in the module dictionary for objects with generate function
    for obj in module.__dict__:
        # if we find objects
        if isinstance(obj, object):
            try:
                # we try and get that objects dictionary.
                # if it's a class it will contain methods and more.
                thedict = module.__dict__[obj].__dict__
                if(thedict['generate']):
                    patterns.append(module.__dict__[obj])
            except:
                # continue if we try and read something we can't.
                continue
    # return a list of classes that have a generate function in them
    return patterns


def tst_patterns(dir, showpass=True):
    def name_of_global_obj(xx):
        return [objname for objname,oid in globals().items() if id(oid)==id(xx)][0]
    patterns = find_patterns_in_dir(dir)
    for pattern in patterns:
        try:
            pat = pattern()
            pat.generate()
            if showpass:
                print("-----------------")
                print("passed: %s" % type(pat))
                print("-----------------")
        except Exception as e:
            print("---------------------")
            print("Pattern:%s Exception:%s" % (pattern, e))
            print("---------------------")
            continue


def load_targets(configfile):
    # this function allows loading of the config files specified by
    # --config/configfile and load patterns defined in there.
    package = "configs"
    fp, path, description = imp.find_module(package)
    path = [path]
    fp, path, description = imp.find_module(str(configfile)[:-3], path)
    config = imp.load_module("configuration", fp, path, description)
    return config.TARGETS


def debugprint(data):
    """Function that prints into the stdout, in the shape of the matrix."""
    from matrix import matrix_size, matrix_width
    chunksize = matrix_width
    for i in range(0, matrix_size, chunksize):
        print(data[i:i + chunksize])
    print("")


def checkList(first, second):
    for item1, item2 in zip(first, second):
        if item1 != item2:
            return False
    return True


def sendout(args, TARGETS, protocol):
    # sendout function that sends out data to the networked devices and
    # also to the matrix screen simulator if enabled.
    # or only to the matrix simulator if netSilent enabled.
    try:
        for t in TARGETS:
            pattern = TARGETS[t]
            # generate the next set of images to send.
            pattern.generate()
            if args.matrixSim == "enabled":
                matrixscreen.handleinput()
                matrixscreen.process(pattern)
            if args.sendOnChange == "enabled":
                changed = (Surface(pattern) != Surface(sendout.previous))
                sendout.previous = Surface(pattern)
            else:
                changed = True
            if changed:
                if not (args.netSilent == "enabled"):
                    try:
                        protocol.send(pattern, t)
                    except Exception as e:
                        traceback.print_exc()
                        print("\r\ndest: %s" % (t))
                        print("pattern size, width, height: ",
                              pattern.get_size(), pattern.get_width(),
                              pattern.get_height())
                        raise(e)
    # matrix sim needs this because i am to lazy to press the x button.
    except KeyboardInterrupt:
        cleanup(1)
    except SystemExit:
        cleanup(2)
sendout.previous = Surface(width=10, height=10)


def listpatterns():
    pattern_objects = find_patterns_in_dir('Patterns')
    patterns = []
    for pattern in pattern_objects:
        patterns.append(pattern.__name__)
    # print a sorted list of patterns.
    for pattern in sorted(patterns):
        print(pattern)

# cleanup exits calls close and leaves tty in sane state.
def cleanup(d):
    print("\nExiting(%d) closing connections." % d)
    os.system('stty sane; echo ""')
    args = get_args()
    if args.netSilent != "enabled":
        protocol.close()
    sys.exit(0)

def main():
    # first thing we do register at exit function.
    # make tty be sane so that if the tty/terminal screws up.
    # this will make it workable again.
    if args.list:
        listpatterns()
        cleanup(5)
    if args.testing:
        tst_patterns('Patterns', showpass=False)
        print("Done testing. ")
        cleanup(4)
    # if gui selected start that else start the headless code.
    if args.gui == "enabled":
        try:
            from Gui.Gui import Gui
            editor = Gui(args)
            editor.main()
        except Exception as e:
            print(e)
        print("Exiting.")
        cleanup(6)
    else:
        TARGETS = load_targets(args.config)

        # check if there is anything configured.
        if not len(TARGETS):
            print("nothing is configured in %s" % args.config)
            cleanup(7)
        # resolve hostenames if any
        for target in TARGETS:
            TARGETS[gethostbyname(target)] = TARGETS.pop(target)
        # ---------

        protocol.open()

        if args.fps > 0:
            fps = 1. / args.fps

        previousTime = 0
        adjust = 0
        currentTime = time.time()
        measured = []

        while(True):
            # send patterns out in a timed fasion. if args.fps != 0
            # check if we want to print the fps to the terminal
            currentTime = time.time()
            cfps = 1. / (currentTime - previousTime)
            measured.append(cfps)
            if len(measured) > 100:
                del measured[0]
            if args.showFps == "enabled":
                fmt = (cfps, sum(measured) / len(measured))
                fmtstr = "current fps: %0.2f average: %0.2f            \r"
                sys.stdout.write(fmtstr % fmt)
                sys.stdout.flush()
            if args.fps > 0:
                sendout(args, TARGETS, protocol)
                time.sleep(abs(fps))
            # else send everything out as fast as possible
            else:
                sendout(args, TARGETS, protocol)
            previousTime = currentTime

if __name__ == "__main__":
    main()