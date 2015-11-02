import pygtk
pygtk.require('2.0')
import gtk, gobject
import math


class GtkGraphics(object):
    def __init__(self, cr=None):
        self.cr = cr
        self.fillc = (0xff, 0xff, 0xff)

    def set_context(self, cr):
        self.cr = cr

    def fill(self, event, color=(0, 0, 0)):
        if not self.cr:
            return
        self.cr.rectangle(event.area.x, event.area.y,
                          event.area.width, event.area.height)
        r, g, b = color
        self.cr.set_source_rgb(r / 0xff, g / 0xff, b / 0xff)
        self.cr.fill()

    # function for drawing a single pixel!
    def _draw_line(self, x1, y1, x2, y2, color=(0, 0, 0), width=1):
        if not self.cr:
            return
        self.cr.set_line_width(width)
        self.cr.move_to(x1, y1)
        self.cr.rel_line_to(x2, y2)
        r, g, b = color
        self.cr.set_source_rgb(r / 0xff, g / 0xff, b / 0xff)
        self.cr.stroke()
        self.cr.fill()

    def draw_pixel(self, x, y, color=(0, 0, 0)):
        self._draw_line(x, y, 1, 1, color)

    def draw_fill_circle(self, x, y, radius, color=(0, 0, 0), width=1):
        if not self.cr:
            return
        self.cr.set_line_width(width)
        self.cr.arc(x + radius, y + radius, radius, 0, 2 * math.pi)
        r, g, b = color
        self.cr.set_source_rgb(r / 0xff, g / 0xff, b / 0xff)
        self.cr.fill()

    def draw_circle(self, x, y, radius, color=(0, 0, 0), width=1):
        if not self.cr:
            return
        self.draw_fill_circle(x, y, radius, color=(0, 0, 0))
        self.draw_fill_circle(x + width, y + width,
                              radius - width, color=(0xff, 0xff, 0xff))
        self.cr.fill()

    def draw_line(self, x1, y1, x2, y2, color=(0, 0, 0), width=1):
        if not self.cr:
            return
        self.cr.set_line_width(width)
        self.cr.move_to(x1, y1)
        self.cr.rel_line_to(x2, y2)
        r, g, b = color
        self.cr.set_source_rgb(r / 0xff, g / 0xff, b / 0xff)
        self.cr.stroke()
        self.cr.fill()

    def draw_rect(self, x, y, width, height, color=(0, 0, 0), lwidth=1):
        # for w in range(0, lwidth):
        for xr in range(x, x + width):
            self.draw_pixel(xr, y)
            self.draw_pixel(xr, y + height - 1)
        for yr in range(y, y + height):
            self.draw_pixel(x, yr)
            self.draw_pixel(x + width - 1, yr)


class TurnSlider(gtk.DrawingArea):
    def __init__(self, *args, **kwds):
        gtk.DrawingArea.__init__(self)
        gtk.DrawingArea.set_size_request(self, 100, 100)
        flags = (gtk.gdk.BUTTON_RELEASE_MASK |
                 gtk.gdk.BUTTON_PRESS_MASK |
                 gtk.gdk.POINTER_MOTION_MASK)
        gtk.DrawingArea.set_events(self, flags)
        gtk.DrawingArea.connect(self, 'expose-event',
                                self.on_draw_area_expose)
        gtk.DrawingArea.connect(self, 'motion-notify-event',
                                self.motion)
        gtk.DrawingArea.connect(self, 'button-press-event',
                                self.button_handle)
        gtk.DrawingArea.connect(self, 'button-release-event',
                                self.button_handle)
        self.graphics = GtkGraphics()

        self.knobradius = 15
        self.lmpressed = False
        self.mpos = (0, 0)
        self.press_y = 0
        self.release_y = 0

    def redraw(self):
        self.queue_draw()

    def on_draw_area_expose(self, widget, event, data=None):
        self.cr = widget.window.cairo_create()
        self.graphics.set_context(self.cr)
        self.graphics.fill(event, (0xff, 0xff, 0xff))
        x, y = (event.area.width / 2 - self.knobradius,
                event.area.height / 2 - self.knobradius)
        self.graphics.draw_circle(x, y, self.knobradius)

    # use motion of mouse when pressed to update knob position
    def motion(self, widget, event):
        self.mpos = (event.x, event.y)
        self.redraw()
        return True

    def knob_drag(self, widget, event, data=None):
        print("pressed!", self.mpos)
        print(event)
        y = event.y
        type = event.type
        button = event.button
        if button == 1:
            if type == gtk.gdk.BUTTON_PRESS:
                self.press_y = y
            elif type == gtk.gdk.BUTTON_RELEASE:
                self.release_y = y
                print("dragged: %d" % (self.press_y - self.release_y))

    # keep track of which button is pressed
    # what each button does
    def button_handle(self, widget, event, data=None):
        # handle knop turning if any.
        self.knob_drag(widget, event, data)


class Gui(object):
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("destroy", self.destroy)

        self.windowbox = gtk.HBox()

        self.turnslider = TurnSlider()
        self.windowbox.pack_start(self.turnslider, False, False, 0)
        self.windowbox.show()
        self.window.add(self.windowbox)
        self.turnslider.show()
        self.window.show()

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def main(self):
        gtk.main()

if __name__ == "__main__":
    gui = Gui()
    gui.main()
