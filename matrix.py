"""
matrix dimensions and color order.
and conversion function(s) to apply to matrices
"""

from Tools.Graphics import Surface

matrix_height = 48
matrix_width = 96

# matrix_width = 10
# matrix_height = 10

# matrix_height = 34
# matrix_width = 20

# matrix_height = 17
# matrix_width = 10

# matrix_height = 80
# matrix_width = 7

# matrix_height = 8
# matrix_width = 8

# matrix_height = 12
# matrix_width = 12

# matrix_height = 32
# matrix_width = 32

# matrix_height = 8
# matrix_width = 8

matrix_size = (matrix_height * matrix_width)

COLOR_ORDER = [0, 1, 2]


def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


def to_matrix(l, n):
    return [l[i:i + n] for i in range(0, len(l), n)]


# inverts every other line in the y direction.
def convertSnakeModes(data):
    ndata = Surface(data)
    points = ndata.get_points()
    for point in points:
        x, y = point
        if not ((y + 1) % 2):
            for x in range(0, matrix_width):
                xi = matrix_width - 1 - x
                pos = xi, y
                ndata[(x, y)] = data[pos]
    return ndata
