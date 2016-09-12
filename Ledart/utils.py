"""
    these functions are utils, that are handy to have for various things.
"""


def chunked(data, chunksize):
    """
    yield 'chunks' of data with a size <chunksize>, with iteration count.
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
    """
    yields chunks of a list.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


def to_matrix(l, n):
    """
    turns a list l into a 2d list with inner list size of n
    """
    return [l[i:i + n] for i in range(0, len(l), n)]
