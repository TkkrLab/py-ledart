from matrix import matrix_width, matrix_height
from Tools.Graphics import Graphics, BLUE, BLACK

select = "TestGui"

class GuiObj(object):
    def __init__(self):
        import gtk
        import pygtk
        self.gtk = gtk
        self.pygtk = pygtk
        self.running = True
        
        self.window = self.gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(10)
        
        self.adj = self.gtk.Adjustment(0.0, 0.0, 101.0, 0.1, 1.0, 1.0)
        self.window.set_default_size(100, 250)
        self.window.show()
        self.hbox = self.gtk.HBox()
        
        self.vscales = []

    def addScale(self, adj=None):
        if not adj:
            adj = self.adj
        self.vscales.append(self.gtk.VScale(adj))
        for scale in self.vscales:
            vbox = self.gtk.VBox()
            vbox.pack_start(scale, True, True, 1)
            self.hbox.pack_start(vbox, False, False, 0)
            self.window.add(self.hbox)
            self.hbox.show()
            vbox.show()
            scale.show()

    def hello(self, widget, data=None):
        print "hello!"

    def destroy(self, widget, data=None):
        pass

    def getSliderValues(self):
        pass

    def process(self):
        while self.gtk.events_pending() and self.running:
            self.gtk.main_iteration()

class TestGui(object):
    def __init__(self):
        self.graphics = Graphics(matrix_width, matrix_height)
        self.gui = GuiObj()
        for i in range(0, 10):
            self.gui.addScale()

    def generate(self):
        self.gui.process()
        self.graphics.fill(BLUE)
        return self.graphics.getSurface()