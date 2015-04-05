import pygtk
pygtk.require('2.0')
import gtk
import gobject
import pango
from gtkcodebuffer import CodeBuffer, SyntaxLoader
import py_compile
import sys
import string

from MatrixSim.MatrixScreen import MatrixScreen, interface_opts
from MatrixSim.Interfaces import Interface
from matrix import matrix_width, matrix_height


class MatrixSimWidget(gtk.DrawingArea, Interface):
    def __init__(self, parent, args):
        gtk.DrawingArea.__init__(self)
        Interface.__init__(self, matrix_width, matrix_height, args.pixelSize)
        self.args = args
        self.par = parent
        self.pattern = None
        self.connect("expose-event", self.expose)

        if args.fps:
            gobject.timeout_add(int(1000 / args.fps), self.run)
        else:
            gobject.timeout_add(0, self.run)

        interface = interface_opts["dummy"]
        self.matrixscreen = MatrixScreen(matrix_width, matrix_height,
                                         args.pixelSize, interface)
        gtk.DrawingArea.set_size_request(self, self.width, self.height)

    def get_pattern(self):
        return self.pattern

    def set_pattern(self, pattern):
        self.pattern = pattern

    def color_convert_f(self, color, depth=8):
        temp = []
        for c in color:
            temp.append(c / 255.)
        return tuple(temp)

    def get_target(self):
        return self.target

    def set_target(self, target):
        return self.target

    def run(self):
        if self.pattern:
            data = self.pattern.generate()
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
                cr.stroke()
                cr.set_source_rgb(r, g, b)
                cr.rectangle(x + 1, y + 1, width - 2, height - 2)
                cr.fill()


class Gui(object):
    def __init__(self, args):
        self.args = args
        # tabwidth in spaces
        self.tabwidth = 4
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        # self.window.maximize()
        self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.window.set_title("artnet-editor")
        self.window.connect("destroy", gtk.main_quit)

        self.matrix_widget = MatrixSimWidget(self, self.args)
        width, height = self.matrix_widget.width, self.matrix_widget.height
        self.window.resize(width * 2, height * 2)
        self.syntaxfile = "/home/robert/py-artnet/Gui/syntax-highlight/python"
        self.textfilename = "/home/robert/py-artnet/patterns/Pong/Pong.py"
        self.intermediatefilename = "/home/robert/py-artnet/Gui/"\
                                    "IntermediateCode/intermediate.py"

        # syntax highlighting.
        self.lang = SyntaxLoader(self.syntaxfile)
        self.buff = CodeBuffer(lang=self.lang)
        self.buff.set_text(self.loadfile(self.textfilename))
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
        newi.connect("activate", self.newfile)
        filemenu.append(newi)

        openm = gtk.ImageMenuItem(gtk.STOCK_OPEN, agr)
        key, mod = gtk.accelerator_parse("<Control>O")
        openm.add_accelerator("activate", agr, key, mod,
                              gtk.ACCEL_VISIBLE)
        openm.connect("activate", self.openfile)
        filemenu.append(openm)

        savem = gtk.ImageMenuItem(gtk.STOCK_SAVE, agr)
        key, mod = gtk.accelerator_parse("<Control>S")
        openm.add_accelerator("activate", agr, key, mod,
                              gtk.ACCEL_VISIBLE)
        savem.connect("activate", self.savefile)
        filemenu.append(savem)

        sep = gtk.SeparatorMenuItem()
        filemenu.append(sep)

        exit = gtk.ImageMenuItem(gtk.STOCK_QUIT, agr)
        key, mod = gtk.accelerator_parse("<Control>Q")
        exit.add_accelerator("activate", agr, key, mod,
                             gtk.ACCEL_VISIBLE)
        exit.connect("activate", gtk.main_quit)
        filemenu.append(exit)
        mb.append(filem)

        self.textview = gtk.TextView(self.buff)
        fontdesc = pango.FontDescription("monospace 9")
        self.textview.modify_font(fontdesc)
        tabs = pango.TabArray(1, True)
        tabs.set_tab(0, pango.TAB_LEFT, 32)
        self.textview.set_tabs(tabs)
        scrolledwindow = gtk.ScrolledWindow()
        scrolledwindow.add(self.textview)

        self.hbox = gtk.HBox()
        self.vbox = gtk.VBox()
        self.vbox.pack_start(mb, False, False)
        self.vbox.pack_start(scrolledwindow)
        self.hbox.pack_start(self.vbox)
        # this sets it so that the scrolledwindow follows matrix_widget
        self.hbox.pack_start(self.matrix_widget, False, True)
        self.window.add(self.hbox)
        self.buff.connect("changed", self.text_change)
        self.insert_id = self.buff.connect("insert_text", self.inserted_cb)
        self.window.show_all()

        # do this once and we can import our compiled code.
        self.modpath = '/'.join(self.intermediatefilename.split('/')[:-1])
        sys.path.insert(0, self.modpath)

    def insert(self, widget):
        widget.handler_block(self.insert_id)
        widget.insert_at_cursor(" " * self.tabwidth)
        widget.handler_unblock(self.insert_id)

    def inserted_cb(self, widget, text_iter, char, num):
        if char == '\t':
            widget.stop_emission("insert_text")
            gtk.idle_add(self.insert, widget)

    def text_change(self, widget):
        text = self.get_text()

        # save and compile the text in the text widget on change.
        self.storefile(self.intermediatefilename, text)
        py_compile.compile(self.intermediatefilename)
        # always get the latest itteration of the compiled code.
        intermediate = __import__("intermediate")
        intermediate = reload(intermediate)

        # check agains all the classes in intermediate code base.
        for obj in intermediate.__dict__:
            if isinstance(obj, object):
                try:
                    # for finding the methods of a class if class
                    thedict = intermediate.__dict__[obj].__dict__
                    # if the class has a generate method. it can make patterns.
                    if(thedict['generate']):
                        # make a instance of that pattern so we can run it
                        # in the editor.
                        pattern = intermediate.__dict__[obj]()
                        # tell the matrix widget that we have a new pattern
                        # to generate output.
                        self.matrix_widget.set_pattern(pattern)
                except:
                    continue

    def get_text(self):
        start_iter = self.buff.get_start_iter()
        end_iter = self.buff.get_end_iter()
        text = self.buff.get_text(start_iter, end_iter, True)
        return text

    def loadfile(self, file):
        text = []
        with open(file, 'r') as thefile:
            text.append(thefile.read())
        return text[0]

    def storefile(self, filename, text):
        with open(filename, 'w') as thefile:
            thefile.write(text)

    def savefile(self, widget):
        filename = self.textfilename
        text = self.get_text()
        with open(filename, 'w') as thefile:
            thefile.write(text)

    def newfile(self, widget):
        print("supposed to make a new empty file")

    def openfile(self, widget):
        # create a dialog window.
        dialog = gtk.FileChooserDialog("Open..",
                                       None,
                                       gtk.FILE_CHOOSER_ACTION_OPEN,
                                       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                        gtk.STOCK_OPEN, gtk.RESPONSE_OK)
                                       )
        dialog.set_default_response(gtk.RESPONSE_OK)

        filter = gtk.FileFilter()
        filter.set_name("Python Files.")
        filter.add_mime_type("python")
        filter.add_pattern("*.py")
        dialog.add_filter(filter)

        filter = gtk.FileFilter()
        filter.set_name("All files")
        filter.add_pattern("*")
        dialog.add_filter(filter)

        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            self.textfilename = dialog.get_filename()
            self.buff.set_text(self.loadfile(self.textfilename))
        dialog.destroy()

    def main(self):
        gtk.main()
