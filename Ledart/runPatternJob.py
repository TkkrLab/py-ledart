#!/usr/bin/env python

# import some generaly used libraries
import os
import gc
import sys
import imp
import time
import signal
import atexit
import traceback
from socket import gethostbyname

import cProfile

# import matrix simulator and matrix specifics
from Tools.Graphics import Surface

from ArgumentParser import get_args
# get command line arguments
args = get_args()
protocol = None
matrixsim = None
targets = None

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
        if item.endswith(".py") and not item.startswith("__"):
            # extract the file name and import it.
            sfile = item.split('.')[0]
            try:
                mod = __import__(sfile)
            except Exception as e:
                print("%s:Couldn't import module cause: %s" % (sfile, e))
                traceback.print_exc()
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
                obj_dict = module.__dict__[obj].__dict__
                if(obj_dict['generate']):
                    patterns.append(module.__dict__[obj])
            except:
                # continue if we try and read something we can't.
                continue
    # return a list of classes that have a generate function in them
    return patterns


def tst_patterns(directory, showpass=True):
    patterns = find_patterns_in_dir(directory)
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
            traceback.print_exc()
            print("---------------------")
            continue

""" TODO: use actuall config file and not python source files. """
def load_targets(configfile):
    # this function allows loading of the config files specified by
    # --config=configfile and load patterns defined in there.

    # test if the config file exists, if not it's maybe a local file
    # and else it's probably a path description + file.
    currentdir = os.path.dirname(os.path.abspath(sys.argv[0]))
    variables = {}
    variables['basedir'] = currentdir
    
    if not os.path.exists(configfile):
        configfile = os.path.join(currentdir, "configs", configfile)
    
    print("loading config from: %s" % (configfile))
    execfile(configfile, variables)

    targets = variables.get('targets', None)
    protocol = variables.get('protocol', None)
    matrix_sim = variables.get('matrixsim', None)

    print("protocol: %s" % protocol)
    print("matrixsim: %s" % matrix_sim)

    return (targets, protocol, matrix_sim)


def checkList(first, second):
    for item1, item2 in zip(first, second):
        if item1 != item2:
            return False
    return True


def sendout(args, targets, protocol):
    # sendout function that sends out data to the networked devices and
    # also to the matrix screen simulator if enabled.
    # or only to the matrix simulator if no pattern is selected.
    try:
        for t in targets:
            pattern = targets[t]
            # generate the next set of images to send.
            pattern.generate()
            if matrixscreen:
                matrixscreen.handleinput()
                matrixscreen.process(pattern)
            if args.sendOnChange:
                changed = (Surface(pattern) != Surface(sendout.previous))
                sendout.previous = Surface(pattern)
            else:
                changed = True
            if changed and protocol:
                protocol.send(pattern, t)
    except KeyboardInterrupt:
        cleanup(9)
    except Exception as e:
        traceback.print_exc()
        print("\r\ndest: %s" % (t))
        print("pattern size, width, height: ",
              pattern.get_size(), pattern.get_width(),
              pattern.get_height())
        cleanup(8)
sendout.previous = Surface(width=10, height=10)


def listpatterns():
    currentdir = os.path.dirname(os.path.abspath(sys.argv[0]))
    pattern_objects = find_patterns_in_dir(os.path.join(currentdir, 'Patterns'))
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
    if protocol:
        protocol.close()
    sys.exit(0)

def sigint_handler(signal, frame):
    cleanup(3)


# generate no byte code
sys.dont_write_bytecode = True

def main():
    # first thing we do register at exit function.
    # make tty be sane so that if the tty/terminal screws up.
    # this will make it workable again.
    signal.signal(signal.SIGINT, sigint_handler)
    # load config
    targets, protocol, matrixscreen = load_targets(args.config)

    # command parsing
    if args.list:
        listpatterns()
        cleanup(5)
    if args.testing:
        currentdir = os.path.dirname(os.path.abspath(sys.argv[0]))
        directory = os.path.join(currentdir, 'Patterns')
        tst_patterns(directory, showpass=args.debug)
        print("Done testing. ")
        cleanup(4)
    else:

        # check if there is anything configured.
        if not len(targets):
            print("nothing is configured in %s" % args.config)
            cleanup(7)
        # resolve hostenames if any
        for target in targets:
            targets[gethostbyname(target)] = targets.pop(target)
        # ---------
        if protocol:
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
            if args.showFps:
                fmt = (cfps, sum(measured) / len(measured))
                fmtstr = "current fps: %0.2f average: %0.2f            \r"
                sys.stdout.write(fmtstr % fmt)
                sys.stdout.flush()
            if args.fps > 0:
                sendout(args, targets, protocol)
                time.sleep(abs(fps))
            # else send everything out as fast as possible
            else:
                sendout(args, targets, protocol)
            previousTime = currentTime

if __name__ == "__main__":
    main()