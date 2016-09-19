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
# import all needed submodules
from Ledart.Lmcp import *
from Ledart.Artnet import *
from Ledart.stripinfo import *
from Ledart.MatrixSim.MatrixScreen import MatrixScreen, interface_opts

localhost = "localhost"
dest = localhost

width, height = 32, 32
set_strip_dimensions(matrix(0, 0, width, height))

# sendout with the ArtNet protocol
protocol = ArtNet()

# use None to not sendout anything
# protocol = None

# start the simulator for a nice demo.
matrixsim = MatrixScreen(width=width,
                         height=height,
                         pixelsize=10,
                         fullscreen=False,
                         interface=interface_opts["pygame"])
# or use None to not start the simulator.
# matrixsim = None

# import patterns.
from Ledart.Patterns.Patterns import *

targets = {
    dest: PixelLife(color=(0, 0, 0xff)),
}

```
and is called like:
```
    $ python -m Ledart --conf=pathtoconfig/the_conf.py
```

you simply import a protocol from a submodule like Artnet and set the variable protocol with it.

then you can decide to run a simulator, like the one based on pygame.

if any of the variables ``` protocol ``` or ``` matrixsim ``` is set to ``` None```, the tool wil simply not run that part of the interface.

so to be clear if ``` protocol ``` is set to ``` None```, no data wil be sendout via a protocol,
and when ``` matrixim``` is set to ``` None``` no simulation will be run.

``` set_strip_dimensions() ``` must always be called either with ``` matrix(x, y, width, height)```

or with ``` ledstrip(length) ```

```targets``` is a list of pairs,
where the left value is the destination, like ip or hostname.

and the right value is a pattern to run.

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
        '10.42.3.42' : PixelLife(),
    }
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
keep in mind the pypi version brobably lacks behind some.

some of the dependecies require compiling,
like with pygame-cffi,
mostly the dependencies can be installed via your favorite
packagemanager

the dependencies currently include:
```
    Pillow >= 3.3.0
    PyOpenGL >= 3.1.0
    PyUserInput >= 0.1.10
    cffi >= 1.7.0
    pygame-cffi >= 0.1.1
    pyserial >= 3.1.1
    python-xlib >= 0.16
    pyalsaaudio >= 0.8.2
```
that can be installed via pip

and one other that must beinstalled via packagemanger is:

``` ffmpeg```