#!/usr/bin/env python
import socket
import signal
import sys
import imp
import os
import time


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
            mod = __import__(sfile)
            # extract classes
            classes = get_pattern_classes(mod)
            # if any found:
            if classes:
                # append the object to patterns
                patterns += classes
    # return the patterns found
    return patterns


def get_pattern_classes(module):
    # holds the patterns that are found
    patterns = []
    # look into the modules dictionary for the things in there
    for obj in module.__dict__:
        # if we find objects
        if isinstance(obj, object):
            try:
                # we try and get that objects dictionary.
                # if it's a class it will contain methods and more.
                thedict = module.__dict__[obj].__dict__
                # and if it contains the 'generate' method
                if(thedict['generate']):
                    # the class is appended to the list.
                    patterns.append(module.__dict__[obj])
            except:
                # continue if we try and read something we can't.
                continue
    # return a list of classes that have a generate function in them
    return patterns


def testgenerated(generate, size, tsize, type, inrange):
    fail = False
    color_ints = True
    generated = []
    # for every color tuple in generated.
    for t in generated:
        # if length is 3
        if len(t) == tsize:
            # check if every color is a int in range of 0 - 0xff
            for c in t:
                # if not break and report with color_ints
                if c != type or (c > inrange[0] or c < inrange[1]):
                    color_ints = False
                    break
        # if length is not 3 we break and report with fail.
        else:
            fail = True
            break
    return (fail and color_ints) and (len(generated) == size)


def test_patterns(dir):
    from matrix import matrix_size
    patterns = find_patterns_in_dir(dir)
    for obj in patterns:
        try:
            pattern = obj()
            if len(pattern.generate()) == matrix_size:
                fmt = (obj, len(pattern.generate()))
                print("%s Passed: %s" % fmt)
            else:
                fmt = (obj, len(pattern.generate()))
                print("%s Failed: %s" % fmt)
        except Exception as e:
            print("\n-------------------")
            print("%s >> %s" % (obj, e))
            print("-------------------\n")
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


def signal_handler(signal, frame):
    print("\nExiting closing connections.")
    sock.close()
    sys.exit(0)


def sendout(args):
    # sendout function that sends out data to the networked devices and
    # also to the matrix screen simulator if enabled.
    # or only to the matrix simulator if netSilent enabled.
    try:
        for t in TARGETS:
            pattern = TARGETS[t]
            data = pattern.generate()
            # make sure matrixSim always displays
            # the data the right way.
            if args.matrixSim == "enabled":
                    matrixscreen.process(data)
            # convert the data for the special matrix layout.
            if args.snakeMode == "enabled":
                data = convertSnakeModes(data)
            # if this is a simulation draw it to the matrixscreen else
            # send it out over the network.
            if not (args.netSilent == "enabled"):
                sock.sendto(buildPacket(0, data), (t, UDP_PORT))
    # matrix sim needs this because i am to lazy to press the x button.
    except KeyboardInterrupt:
        signal_handler(None, None)
    except SystemExit:
        signal_handler(None, None)

if __name__ == "__main__":
    from ArgumentParser import get_args
    # get command line arguments:
    args = get_args()
    if args.list:
        sys.exit()
    if args.testing == "enabled":
        test_patterns('patterns')
        print("Done testing. ")
        sys.exit()
    # if gui selected start that else start the headless code.
    if args.gui == "enabled":
        try:
            from Gui.Gui import Gui
            editor = Gui(args)
            editor.main()
        except Exception as e:
            print(e)
        print("Exiting.")
        sys.exit(0)
    else:
        from artnet import buildPacket
        from matrix import matrix_width, matrix_height, convertSnakeModes
        from MatrixSim.MatrixScreen import interface_opts
        try:
            from MatrixSim.MatrixScreen import MatrixScreen
        except Exception as e:
            print("MatrixScreen>> " + str(e))

        UDP_PORT = 6454
        TARGETS = load_targets(args.config)

        # check if there is anything configured.
        if not len(TARGETS):
            print("nothing is configured in %s" % args.config)
            sys.exit(1)
        # ---------

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setblocking(False)

        signal.signal(signal.SIGINT, signal_handler)

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

        if args.fps > 0:
            fps = 1. / args.fps

        # hold values for time.
        current = 0
        previous = 0

        while(True):
            # send patterns out in a timed fasion. if args.fps != 0
            if args.fps > 0:
                current = time.time()
                if (current - previous) >= fps:
                    previous = time.time()
                    sendout(args)
            # else send everything out as fast as possible
            else:
                sendout(args)
        signal_handler(None, None)
