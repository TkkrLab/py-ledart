import pygtk
pygtk.require('2.0')
import gtk
import gobject

from MatrixSim.MatrixScreen import MatrixScreen, interface_opts
from MatrixSim.Interfaces import Interface
from matrix import matrix_width, matrix_height
from runPatternJob import load_targets
from gtkcodebuffer import CodeBuffer, SyntaxLoader


class MatrixSimWidget(gtk.DrawingArea, Interface):
    def __init__(self, parent, args, target):
        gtk.DrawingArea.__init__(self)
        Interface.__init__(self, matrix_width, matrix_height, args.pixelSize)
        self.par = parent
        self.target = self.par.TARGETS
        self.set_size_request(-1, -1)
        self.connect("expose-event", self.expose)

        if args.fps:
            gobject.timeout_add(int(1000 / args.fps), self.run)
        else:
            gobject.timeout_add(0, self.run)

        interface = interface_opts["dummy"]
        self.matrixscreen = MatrixScreen(matrix_width, matrix_height,
                                         args.pixelSize, interface)

    def color_convert_f(self, color, depth=8):
        temp = []
        for c in color:
            temp.append(c / 255.)
        return tuple(temp)

    def run(self):
        for dest in self.target:
            data = self.target[dest].generate()
        self.matrixscreen.process_pixels(data)
        data = self.matrixscreen.get_pixels()
        self.queue_draw()
        return True

    def expose(self, widget, event):
        cr = widget.window.cairo_create()
        if len(self.matrixscreen.pixels):
            for pixel in self.matrixscreen.pixels:
                x, y, width, height = pixel.getRect()
                pixelcolor = pixel.getColor()
                r, g, b = self.color_convert_f(pixelcolor)
                cr.set_source_rgb(0.0, 0.0, 0.0)
                cr.rectangle(x, y, width, height)
                cr.fill()
                cr.set_source_rgb(r, g, b)
                cr.rectangle(x + 1, y + 1, width - 2, height - 2)
                cr.fill()


class Gui(object):
    def __init__(self, args):
        self.args = args
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.window.set_title("artnet-editor")
        self.window.connect("destroy", gtk.main_quit)

        self.TARGETS = load_targets(args.config)
        self.matrix_widget = MatrixSimWidget(self, self.args, self.TARGETS)
        width, height = self.matrix_widget.width, self.matrix_widget.height
        self.window.resize(width * 2, height * 2)

        self.hbox = gtk.HBox()
        self.vbox = gtk.VBox()

        # syntax highlighting.
        lang = SyntaxLoader("/home/robert/py-artnet/python")
        buff = CodeBuffer(lang=lang)
        # menu items
        mb = gtk.MenuBar()

        filemenu = gtk.Menu()
        filem = gtk.MenuItem("_File")
        filem.set_submenu(filemenu)

        agr = gtk.AccelGroup()
        self.window.add_accel_group(agr)

        newi = gtk.ImageMenuItem(gtk.STOCK_NEW, agr)
        key, mod = gtk.accelerator_parse("<Control>N")
        newi.add_accelerator("activate", agr, key, mod,
                             gtk.ACCEL_VISIBLE)
        filemenu.append(newi)

        openm = gtk.ImageMenuItem(gtk.STOCK_OPEN, agr)
        key, mod = gtk.accelerator_parse("<Control>O")
        openm.add_accelerator("activate", agr, key, mod,
                              gtk.ACCEL_VISIBLE)
        filemenu.append(openm)

        sep = gtk.SeparatorMenuItem()
        filemenu.append(sep)

        exit = gtk.ImageMenuItem(gtk.STOCK_QUIT, agr)
        key, mod = gtk.accelerator_parse("<Control>Q")
        exit.add_accelerator("activate", agr, key, mod,
                             gtk.ACCEL_VISIBLE)
        exit.connect("activate", gtk.main_quit)
        filemenu.append(exit)
        mb.append(filem)

        self.vbox.add(self.matrix_widget)
        button = gtk.Button("button")
        self.vbox.add(button)
        self.hbox.add(self.vbox)
        textview = gtk.TextView(buff)
        self.vbox1 = gtk.VBox()
        self.vbox1.pack_start(mb, False, False, 0)
        scr = gtk.ScrolledWindow()
        scr.add(textview)
        self.vbox1.add(scr)
        self.hbox.add(self.vbox1)
        self.vbox2 = gtk.VBox()
        self.vbox2.add(self.hbox)
        self.window.add(self.vbox2)
        self.window.show_all()

    def main(self):
        gtk.main()
