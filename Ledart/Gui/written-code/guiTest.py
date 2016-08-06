from matrix import matrix_width, matrix_height
from Tools.Graphics import Graphics, BLUE, BLACK, WHITE
import time
import gtk
import pygtk

select = "TestGui"

class TurnSlider(gtk.Widget):
    def __init__(self):
        gtk.Widget.__init__(self)
        print("hello")

class GuiObj(object):
    def __init__(self):
        self.running = True
        
        self.vscales = []
        self.scalevalues = []
        
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(10)
        
        # self.adj = gtk.Adjustment(0.0, 0.0, 101.0, 0.1, 1.0, 1.0)
        
        self.window.set_default_size(100, 250)
        
        #setup the indexing of the boxes.
        self.mainbox = gtk.VBox()
        self.scalebox = gtk.HBox()
        self.buttonbox = gtk.VBox()
        self.radiobuttonbox = gtk.HBox()
        self.checkbuttonbox = gtk.HBox()
        self.mainbox.show()
        self.scalebox.show()
        self.buttonbox.show()
        self.radiobuttonbox.show()
        self.checkbuttonbox.show()
        
        self.mainbox.pack_start(self.scalebox, True, True, 0)
        self.mainbox.pack_start(self.buttonbox, False, False, 0)
        self.buttonbox.pack_start(self.radiobuttonbox, False, False, 0)
        self.buttonbox.pack_start(self.checkbuttonbox, False, False, 0)
        
        self.window.add(self.mainbox)
        
        self.addTestButtons()
        
        self.turnslider = TurnSlider()
        del self.turnslider
        
        # make a box in the main window and set both,
        # the box and window to show up.
        self.window.show()

    def addTestButtons(self):
        # test some buttons to add.
        checkbutton = gtk.CheckButton()
        self.checkbuttonbox.pack_start(checkbutton, False, False, 0)
        checkbutton.show()
        
        radiobutton = gtk.RadioButton()
        self.radiobuttonbox.pack_start(radiobutton, False, False, 0)
        radiobutton.show()

    def addScale(self, adj=None):
        scale = []
        self.scalevalues.append(0)
        # create a adjustment
        if not adj:
            adj = gtk.Adjustment(0.0, 0.0, 0xff, 1, 1.0, 1.0)
        else:
            vstart = adj[0]
            minVal = adj[1]
            maxVal = adj[2]
            step = adj[3]
            pageInc = 1.0
            pageSize = 1.0
            adj = gtk.Adjustmen(vstart, minVal, maxVal, step, pageInc, pageSize)
        scale.append(adj)
        # connect a function to handle changing values.
        adj.connect("value_changed", self.valChangeScale)
        # keep track of the vscale references
        vscale = gtk.VScale(adj)
        vscale.set_draw_value(False)
        scale.append(vscale)
        self.vscales.append(scale)
        # add the newly created vscale to the main hbox.
        self.scalebox.pack_start(vscale, True, False, 5)
        # make the vscale visible
        vscale.show()

    def valChangeScale(self, widget, data=None):
        for i, scale in enumerate(self.vscales):
            if scale[0] == widget:
                self.scalevalues[i] = scale[0].get_value()

    def destroy(self, widget, data=None):
        print("destroying")
        self.window.destroy()

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
        self.graphics.fill(BLACK)
        return self.graphics.getSurface()
