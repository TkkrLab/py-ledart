import socket
import signal
import sys


def load_targets(configfile):
    # this function allows loading of the config files specified by
    # --config/configfile and load patterns defined in there.
    import imp
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
    # if gui selected start that else start the headless code.
    if args.gui == "enabled":
        import Gui.Gui as Gui
        Gui.main(args)
        sys.exit(0)
    else:
        import time
        from artnet import buildPacket
        from matrix import matrix_width, matrix_height, convertSnakeModes
        try:
            from MatrixSim.MatrixScreen import MatrixScreen, interface_opts
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
