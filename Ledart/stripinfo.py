"""
    functions for setting the type of string, 
    as in is it one long line,
    or configured as a matrix ?
"""

# x y can be used for a position on a matrix,
# or color channels on a strip.
strip_x, strip_y =  0, 0
strip_width = 1
strip_height = 1
strip_size = (strip_width * strip_height)

def matrix(x=0, y=0, width=1, height=1):
    return [x, y, width, height]

def ledstrip(length=1, channel=0):
    return [0, channel, 1, length]

def set_strip_dimensions(dims=ledstrip(length=1)):
    global strip_x
    global strip_y
    global strip_width
    global strip_height
    global strip_size
    strip_x, strip_y, strip_width, strip_height = dims
    strip_size = (strip_width * strip_height)