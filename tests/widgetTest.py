import pygtk
pygtk.require('2.0')
import gtk
from gtk import gdk


class TurnSlider(gtk.Button):
    def __init__(self, *args, **kwds):
        gtk.Button.__init__(self)
        gtk.Button.connect(self, "pressed", self.pressed)
        gtk.Button.connect(self, "released", self.released)
        gtk.Button.connect(self, "motion-notify-event", self.evented)
        gtk.Button.set_events(self, gdk.POINTER_MOTION_MASK)
        self.props.relief = gtk.RELIEF_NONE

        self.image = gtk.Image()
        self.image.set_from_file('/home/robert/py-artnet/hacked.png')
        self.image.show()
        self.add(self.image)

        self.lmousedown = False
        self.mpos = (0, 0)

    def evented(self, widget, event):
        self.mpos = (event.x, event.y)
        return True

    def pressed(self, widget, data=None):
        print("pressed!", self.mpos)
        self.lmousedown = True

    def released(self, widget, data=None):
        self.lmousedown = False


class Gui(object):
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("destroy", self.destroy)
        self.turnslider = TurnSlider()
        self.window.add(self.turnslider)
        self.turnslider.show()
        self.window.show()

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def main(self):
        gtk.main()

if __name__ == "__main__":
    gui = Gui()
    gui.main()
