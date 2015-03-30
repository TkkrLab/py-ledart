import pygtk
import gtk
pygtk.require('2.0')

dialog = gtk.FileChooserDialog("Load File",
                                None,
                                gtk.FILE_CHOOSER_ACTION_OPEN,
                                (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                 gtk.STOCK_OPEN, gtk.RESPONSE_OK))

dialog.set_default_repsonse(gtk.RESPONSE_OK)


