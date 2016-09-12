"""
    functions for setting the type of string, 
    as in is it one long line,
    or configured as a matrix ?
"""


def matrix(x=0, y=0, width=1, height=1):
    return [x, y, width, height]

def ledstrip(length=1):
    return [0, 0, 1, length]
