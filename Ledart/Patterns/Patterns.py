"""
import patterns here if they are in a different file.
"""
import traceback

def debugprint(discr, exception):
    import inspect
    callerframerecord = inspect.stack()[1]

    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    filename = info.filename.split('/')[-1]
    fmt = (discr, info.function, filename, info.lineno, str(exception))
    print("%s %s in %s at: %s %s" % fmt)


"""#ohm led poles."""
# from PolicePattern import PolicePattern
# from BarberpolePattern import BarberpolePattern
# from ColorFadePattern import ColorFadePattern

""" try to load patterns and see if anything goes wrong."""

try:
    from Mandelbrot import *
    from RainPattern import *
    from PixelLife import *
    from Plasma import *
    from FillTest import *
    from GraphicsTests import *
    from CellurarAutomata import *
    from Fractals import *
    from Water import *
    from Fire import *
    from Sim import *
    from VUmeter import *
    from Fft import *
    from SpiroGraph import *
except Exception as e:
    debugprint("Various patterns >>", e)
    traceback.print_exc()


""" these patterns can't standalone, they use supporting libraries."""

# uses ffmpeg
try:
    from VideoPlay import *
except Exception as e:
    debugprint("VideoPlay >>", e)
    traceback.print_exc()

# uses pygame for testing.
try:
    from SuperPixelBros import SuperPixelBros
except Exception as e:
    debugprint("PixelBros >>", e)

# try and load with pillow
try:
    from DisplayImage import *
except Exception as e:
    debugprint("DisplayImage >>", e)

# patterns that do use pygame
try:
    from Pong import *
except Exception as e:
    debugprint("Pong >>", e)

try:
    from Tron import *
except Exception as e:
    debugprint("Tron >>", e)

try:
    from Snake import *
except Exception as e:
    debugprint("snake >>", e)
