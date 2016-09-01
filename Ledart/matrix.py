"""
matrix dimensions and color order.
and conversion function(s) to apply to matrices
"""

# tkkrlab ledboard size
# matrix_height = 48
# matrix_width = 96

# matrix_height = 10
# matrix_width = 17

# matrix_height = 32
# matrix_width = 64

# matrix_height = 48
# matrix_width = 64

matrix_height = 64
matrix_width = 128

# matrix_height = 800
# matrix_width = 1280

# pixelmatrix size
# matrix_height = 10
# matrix_width = 17

matrix_size = (matrix_height * matrix_width)

COLOR_ORDER = [0, 1, 2]


def chunked(data, chunksize):
    """
    yield sections 'chunks' of data with size <chunksize>, with iteration count.
    """
    chunk = []
    it = 0
    if chunksize <= 0:
        yield (0, [])
    else:
        while(it < (len(data) / chunksize)):
            index = (it * chunksize)
            chunk = data[index:(index + chunksize)]
            yield (it, chunk)
            it += 1

def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


def to_matrix(l, n):
    return [l[i:i + n] for i in range(0, len(l), n)]
