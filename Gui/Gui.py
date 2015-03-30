import pygtk
pygtk.require('2.0')
import gtk

class Base(object):
    itteration = 0
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

        self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.window.set_size_request(800, 600)
        self.window.set_tooltip_text("This is my Gui\nAnother line.")
        self.window.set_title("My Gui")

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

        self.box2.pack_start(self.box1)
        self.box2.pack_start(self.textbox)
        self.box2.pack_start(self.label1)
        self.box2.pack_start(self.combo)

        self.box3.pack_start(self.box2)
        self.box3.pack_start(self.button6)

        dialog = gtk.FileChooserDialog("Load Image", None,
                                        )

        self.pix = gtk.gdk.pixbuf_new_from_file("/home/robert/py-art-net/hacked.png")
        self.pix = self.pix.scale_simple(100, 100, gtk.gdk.INTERP_BILINEAR)
        self.image = gtk.image_new_from_pixbuf(self.pix)
        self.image.set_from_pixbuf(self.pix)

        self.box4.pack_start(self.box3)
        self.box4.pack_start(self.image)

        self.window.add(self.box4)
        self.window.show_all()
        self.window.connect("destroy", self.destroy)

    def main(self):
        gtk.main()

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
        self.itteration+=1

    def destroy(self, widget, data=None):
        print("Quiting")
        gtk.main_quit()

if __name__ == '__main__':
    base = Base()
    base.main()
