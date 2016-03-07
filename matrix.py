"""
matrix dimensions and color order.
and conversion function(s) to apply to matrices
"""

# tkkrlab ledboard size
# matrix_height = 48
# matrix_width = 96

# pixelmatrix size
matrix_height = 10
matrix_width = 17

matrix_size = (matrix_height * matrix_width)

COLOR_ORDER = [0, 1, 2]


def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


def to_matrix(l, n):
    return [l[i:i + n] for i in range(0, len(l), n)]
