"""
matrix dimensions and color order for simulator.
and conversion function(s)
"""

matrix_height = 17*3
matrix_width = 10*3
matrix_size = (matrix_height * matrix_width)
COLOR_ORDER = [0, 1, 2]


def convertSnakeModes(pattern):
    for y in range(0, matrix_height, 2):
        templist = []
        for x in range(matrix_width - 1, -1, -1):
            templist.append(pattern[y * matrix_width + x])
        for x in range(0, matrix_width):
            pattern[y * matrix_width + x] = templist[x]
    return pattern
