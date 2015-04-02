import pygtk
pygtk.require('2.0')
import gtk
import gobject

from MatrixSim.MatrixScreen import MatrixScreen
from MatrixSim.Interfaces import Interface
import matrix


class MatrixSimWidget(gtk.Widget, MatrixScreen, Interface):
    def __init__(self, width, height, pixelsize,
                 fullscreen=False, interface=None):
        gtk.Widget.__init__(self)
        Interface.__init__(width, height, pixelsize)
        MatrixScreen.__init__(width, height, pixelsize, Interface)


class Gui(object):
    def __init__(self, args):
        self.args = args
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.window.set_title("artnet-editor")
        self.window.connect("destroy", gtk.main_quit)

        self.matrix_widget = MatrixSimWidget(matrix.matrix_width,
                                             matrix.matrix_height,
                                             self.args.pixelsize)

        if self.args.fps:
            gobject.timeout_add(int(1000 / self.args.fps), self.run)
        else:
            gobject.timeout_add(0, self.run)

        self.window.show()

    def run(self):
        return True

    def main(self):
        gtk.main()


class Base(object):
    itteration = 0

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

        self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.window.set_size_request(800, 600)
        self.window.set_tooltip_text("This is my Gui\nAnother line.")
        self.window.set_title("My Gui")

        self.about_button = gtk.Button("About")
        self.about_button.connect("clicked", self.about_win)

        self.open_image = gtk.Button("Open Image")
        self.open_image.connect("clicked", self.openimage)

        self.button1 = gtk.Button("Exit")
        self.button1.connect("clicked", self.destroy)
        self.button1.set_tooltip_text("Click to Exit")

        self.button2 = gtk.Button("Hide")
        self.button2.connect("clicked", self.myhide)

        self.button3 = gtk.Button("Show")
        self.button3.connect("clicked", self.myshow)

        self.button4 = gtk.Button("relabel label")
        self.button4.connect("clicked", self.relabel)

        self.button5 = gtk.Button("clear text")
        self.button5.connect("clicked", self.cleartext)

        self.button6 = gtk.Button("add to combo")
        self.button6.connect("clicked", self.addcombotext)

        self.label1 = gtk.Label("label")
        self.textbox = gtk.Entry()
        self.textbox.connect("changed", self.textchange)

        self.combo = gtk.combo_box_entry_new_text()
        self.combo.connect("changed", self.combotext)
        self.combo.append_text("this is some text")
        self.combo.append_text("this is option 2")

        self.box1 = gtk.HBox()
        self.box2 = gtk.VBox()
        self.box3 = gtk.HBox()
        self.box4 = gtk.VBox()
        self.box1.pack_start(self.button1)
        self.box1.pack_start(self.button2)
        self.box1.pack_start(self.button3)
        self.box1.pack_start(self.button4)
        self.box1.pack_start(self.button5)
        self.box1.pack_start(self.open_image)
        self.box1.pack_start(self.about_button)

        self.box2.pack_start(self.box1)
        self.box2.pack_start(self.textbox)
        self.box2.pack_start(self.label1)
        self.box2.pack_start(self.combo)

        self.box3.pack_start(self.box2)
        self.box3.pack_start(self.button6)

        self.box4.pack_start(self.box3)

        self.window.add(self.box4)
        self.window.show_all()
        self.window.connect("destroy", self.destroy)
        self.imagedir = "home/robert/py-art-net/hacked.png"

    def main(self):
        gtk.main()

    def openimage(self, widget):

        dialog = gtk.FileChooserDialog("Load Image", None,
                                       gtk.FILE_CHOOSER_ACTION_OPEN,
                                       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                        gtk.STOCK_OPEN, gtk.RESPONSE_OK))

        dialog.set_default_response(gtk.RESPONSE_OK)
        filter = gtk.FileFilter()
        filter.set_name("Images")
        filter.add_mime_type("image/png")
        filter.add_mime_type("image/jpeg")
        filter.add_mime_type("image/bmp")
        filter.add_pattern("*.png")
        filter.add_pattern("*.jpg")
        filter.add_pattern("*.jpeg")
        dialog.add_filter(filter)

        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            self.pix = gtk.gdk.pixbuf_new_from_file(dialog.get_filename())
            self.pix = self.pix.scale_simple(100, 100, gtk.gdk.INTERP_BILINEAR)
            self.image = gtk.image_new_from_pixbuf(self.pix)
            self.image.set_from_pixbuf(self.pix)
            self.box4.pack_start(self.image)
        elif response == gtk.RESPONSE_CANCEL:
            print("no file selected")
            em = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE,
                                   "File Not Loaded\nWindow looks different")
            em.run()
            em.destroy()
        self.window.show_all()
        dialog.destroy()

    def about_win(self, widget):
        about = gtk.AboutDialog()
        about.set_program_name("My Guid")
        about.set_version("0.1")
        about.set_copyright("Duality")
        about.set_comments("this is a gtk program in python")
        about.set_website("http://www.github.com/tkkrlab/py-art-net/")
        about.set_logo(gtk.gdk.pixbuf_new_from_file(self.imagedir))
        about.run()
        about.destroy()

    def clicked(self, widget):
        print("clicked")

    def addcombotext(self, widget):
        self.combo.append_text(self.textbox.get_text())

    def combotext(self, widget):
        self.textbox.set_text(widget.get_active_text())

    def cleartext(self, widget):
        self.textbox.set_text("")

    def textchange(self, widget):
        self.label1.set_text(widget.get_text())

    def myhide(self, widget):
        self.button1.hide()

    def myshow(self, widget):
        self.button1.show()

    def relabel(self, widget):
        self.label1.set_text(str(self.itteration))
        self.itteration += 1

    def destroy(self, widget, data=None):
        print("Quiting")
        gtk.main_quit()


def main(args):
    base = Gui(args)
    base.main()
    # base = Base()
    # base.main()
