[![Build Status](https://travis-ci.org/TkkrLab/py-ledart.svg?branch=master)](https://travis-ci.org/TkkrLab/py-ledart)

py-ledart
==========
py-ledart is a python lib for controlling ledstrips and ledmatrices on a network.

supports following protocols:

* Lmcp (ledmatrix control protocol)(https://www.tkkrlab.nl/wiki/Ledboard)

* Artnet (https://en.wikipedia.org/wiki/Art-Net)


py-ledart has some submodules that make it easy to send and generate pixeldata.

or for when you just want to run it from the command line, 
there are some build in patterns that can be run.

## features
features include:

submodules for easily coding patterns,

easily drawing, and easily sending out patterns.

other features include easily previewing your creations, with a matrix simulator.


## configuration for the commandline tool.
a example config might look like:
```python
# import all patterns availble for use.
from Ledart.Lmcp import *
from Ledart.Artnet import *
from Ledart.utils import *
from Ledart.MatrixSim.MatrixScreen import MatrixScreen, interface_opts

localhost = "localhost"
dest = localhost

width, height = 32, 32
dims = matrix(0, 0, width, height)

# don't send out anything.
protocol = None
# start the simulator for a nice demo.
matrixsim = MatrixScreen(dims=dims,
                         pixelsize=7,
                         fullscreen=False,
                         interface=interface_opts["pygame"])

from Ledart.Patterns.Patterns import *

targets = {
    dest: PixelLife(dims=dims, color=(0, 0, 0xff)),
}


```
and is called like:
```
    $ python -m Ledart --conf=pathtoconfig/the_conf.py
```

calling the script with:
```
    $ python -m Ledart
```

will give you a nice demo of the above code.


you import a protocol from a submodule like Artnet and set the variable protocol with it.

then you can decide to run a simulator, like the one based on pygame.

if any of the variables ``` protocol ``` or ``` matrixsim ``` is set to ``` None```, the tool wil simply not run that part of the interface.

so to be clear if ``` protocol ``` is set to ``` None```, no data wil be sendout via a protocol,
and when ``` matrixsim``` is set to ``` None``` no simulation will be run.

a dimension representing a matrix or a led strip must always be passed to a pattern and/or the matriximulator.

a dimension object can be constructed with: ``` ledstrip(length=number_of_pixel) ```

or with: ``` matrix(x=x_pos, y=y_pos, width=width_in_pixel, height=height_in_pixels) ```

```targets``` is a list of pairs,
where the left value is the destination, like ip or hostname.

and the right value is a pattern to run.

notice that if you pass a hostename instead of a ip address, the hostname will be tried to be resolved when a protocol is specified.

it might error when it's not able to find it.

the pattern follows like:
```
targets = 
    {
        destination : pattern,
    }
```

multiple patterns can be sendout like:

```
targets = 
    {
        destination1 : pattern1(),
        destination2 : pattern2(),
        destination1 : pattern2()
    }
```

a real case might look like:
```
targets = 
    {
        '10.42.3.42' : PixelLife(dims=matrix(0, 0, 32, 32)),
    }
```

## pre-installation
install these through your favorite packagemanager:
```
    ffmpeg
    pygame
```

## installation
installing the software is as easy as installing it with pip

either from the git repo:
```
    $ pip install git+https://github.com/TkkrLab/py-ledart
```

or from pypi:
```
    $ pip install Ledart
```
keep in mind the pypi version probably lacks behind some.

the dependencies currently include:
```
    Pillow >= 2.9.0
    PyOpenGL >= 3.1.0
    PyUserInput >= 0.1.10
    cffi >= 1.7.0
    pygame-cffi >= 0.1.1
    pyserial >= 3.1.1
    python-xlib >= 0.16
    pyalsaaudio >= 0.8.2
```
that can be installed via pip

