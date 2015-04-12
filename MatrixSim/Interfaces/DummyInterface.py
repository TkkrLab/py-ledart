from Interface import Interface


class DummyInterface(Interface):
    def __init__(self, width, height, blocksize, fullscreen=False):
        Interface.__init__(self, width, height, blocksize, fullscreen)
