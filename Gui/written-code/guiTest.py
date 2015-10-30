from matrix import matrix_width, matrix_height
from Tools.Graphics import Graphics, BLUE, BLACK
import gtk
import pygtk

select = "TestGui"

class GuiObj(object):
    def __init__(self):
        self.running = True
        
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        # self.window.reparent(gui)
        self.window.connect("destroy", self.destroy)
        self.window.connect("delete-event", self.destroy)
        self.window.set_border_width(10)
        
        # self.adj = gtk.Adjustment(0.0, 0.0, 101.0, 0.1, 1.0, 1.0)
        
        self.window.set_default_size(100, 250)
        
        self.hbox = gtk.HBox()
        self.window.add(self.hbox)
        # make a box in the main window and set both,
        # the box and window to show up.
        self.hbox.show()
        self.window.show()
        
        self.vscales = {}
        self.scalevalues = []

    def addScale(self):
        self.scalevalues.append(0)
        # create a adjustment
        adj = gtk.Adjustment(0.0, 0.0, 0xff, 1, 1.0, 1.0)
        # connect a function to handle changing values.
        adj.connect("value_changed", self.valChangeScale)
        # keep track of the vscale references
        self.vscales[adj] = gtk.VScale(adj)
        # add the newly created vscale to the main hbox.
        self.hbox.pack_start(self.vscales[adj], True, False, 5)
        # make the vscale visible
        self.vscales[adj].show()

    def valChangeScale(self, widget, data=None):
        for i, adj in enumerate(self.vscales):
            if adj == widget:
                self.scalevalues[i] = adj.get_value()

    def destroy(self, widget, data=None):
        pass
        # self.window.hide_all()

    def getScaleValue(self, slider):
        return self.scalevalues[slider]

    def process(self):
        while gtk.events_pending() and self.running:
            gtk.main_iteration()

class TestGui(object):
    def __init__(self):
        self.graphics = Graphics(matrix_width, matrix_height)
        self.gui = GuiObj()
        for i in range(0, 10):
            self.gui.addScale()

    def generate(self):
        self.gui.process()
        value = self.gui.getScaleValue(0)
        print(value)
        self.graphics.fill(BLUE)
        return self.graphics.getSurface()
