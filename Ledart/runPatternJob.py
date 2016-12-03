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

from Tools.Graphics import Surface
from utils import load_targets
from utils import find_patterns_in_dir
from utils import matrix

basepath = os.path.dirname(os.path.realpath(__file__))
protocol, matrixscreen, targets = None, None, None


def tst_patterns(directory, showpass=False):
    test_dims = matrix(x=0, y=0, width=128, height=64)

    failed = []

    patterns = find_patterns_in_dir(directory)
    for pattern in patterns:
        try:
            pat = pattern(dims=test_dims)
            pat.generate()
            if showpass:
                print("-----------------")
                print("passed: %s" % type(pat))
                print("-----------------")
        except Exception as e:
            print("---------------------")
            print("Pattern:%s Exception:%s" % (pattern, e))
            traceback.print_exc()
            failed.append(pattern)
            print("---------------------")
            continue
    return failed

def listpatterns():
    basepath = os.path.dirname(os.path.realpath(__file__))
    pattern_objects = find_patterns_in_dir(os.path.join(basepath, 'Patterns'))
    patterns = []
    for pattern in pattern_objects:
        patterns.append(pattern.__name__)
    # print a sorted list of patterns.
    for pattern in sorted(patterns):
        print(pattern)


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
    gc.disable()

    from ArgumentParser import get_args
    # get command line arguments
    args = get_args()

    # command parsing
    if args.list:
        listpatterns()
        cleanup(5)
    if args.testing:
        directory = os.path.join(basepath, 'Patterns')
        tst_patterns(directory, showpass=args.debug)
        print("Done testing. ")
        cleanup(4)
    else:
        # load config
        global targets
        global protocol
        global matrixscreen
        targets, protocol, matrixscreen = load_targets(args.config)

        # check if there is anything configured.
        if not len(targets):
            print("nothing is configured in %s" % args.config)
            cleanup(7)
        # resolve hostenames if protocol specified.
        # else it doesn't really matter.
        for target in targets:
            if protocol:
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
