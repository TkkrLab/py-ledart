from MatrixScreen import MatrixScreen, interface_opts
from Interfaces.Interface import Interface
from Ledart.utils import matrix
from Ledart.Tools.Graphics import Graphics, BLUE
from Ledart.utils import chunked

from multiprocessing import Process, Pipe
import time
import os


class DetachedScreen(object):
    def __init__(self, dims=matrix(0, 0, 1, 1), pixelsize=10, fullscreen=False,
                 interface=Interface):
        matrixscreen = MatrixScreen(dims, pixelsize, fullscreen, interface)

        self.running = True
        self.parrent_conn, self.child_conn = Pipe()
        self.p = Process(target=self.screen_process, args=(self.child_conn, matrixscreen))
        self.p.start()

    def screen_process(self, conn, matrixscreen):
        while(self.running):
            try:
                matrixscreen.process(conn.recv())
            except Exception as e:
                print("exiting")
                sys.exit(1)

    def process(self, pattern):
        self.parrent_conn.send(pattern)
        if not self.running:
            print("terminating. ")
            self.p.terminate()
            self.p.join(1)
            raise KeyboardInterrupt

    def close(self):
        self.p.terminate()
        self.p.join(1)
