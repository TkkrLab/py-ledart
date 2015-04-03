import pygtk
pygtk.require('2.0')
import gtk
import gobject

from MatrixSim.MatrixScreen import MatrixScreen, interface_opts
from MatrixSim.Interfaces import Interface
from matrix import matrix_width, matrix_height
from runPatternJob import load_targets


class MatrixSimWidget(gtk.DrawingArea, Interface):
    def __init__(self, parent, args, target):
        gtk.DrawingArea.__init__(self)
        Interface.__init__(self, matrix_width, matrix_height, args.pixelSize)
        self.par = parent
        self.target = self.par.TARGETS
        self.set_size_request(self.height, self.width)
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

        if args.fullscreen == "enabled":
            self.fullscreen = True
        else:
            self.fullscreen = False

        self.TARGETS = load_targets(args.config)
        self.matrix_widget = MatrixSimWidget(self, self.args, self.TARGETS)
        width, height = self.matrix_widget.width, self.matrix_widget.height
        self.window.resize(width * 2, height * 2)

        self.window.add(self.matrix_widget)
        self.window.show_all()

    def main(self):
        gtk.main()
