# import all patterns availble for use.
from Patterns.Patterns import *

localhost = "localhost"
<<<<<<< HEAD:configs/default_conf.py
ledboard = "ledboard"
dest = localhost
=======
ledboard = "megamatrix"
dest = ledboard
>>>>>>> packaging:Ledart/configs/default_conf.py

TARGETS = {
    dest: PixelLife(),
}
