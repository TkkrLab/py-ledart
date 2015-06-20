"""
matrix dimensions and color order for simulator.
and conversion function(s)
"""

# matrix_height = 17
# matrix_width = 10

# matrix_height = 80
# matrix_width = 7

matrix_height = 8
matrix_width = 8

matrix_size = (matrix_height * matrix_width)
COLOR_ORDER = [0, 1, 2]


def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


def convertSnakeModes(data):
    for y in range(0, matrix_height, 2):
        templist = []
        for x in range(matrix_width - 1, -1, -1):
            templist.append(data[y * matrix_width + x])
        for x in range(0, matrix_width):
            data[y * matrix_width + x] = templist[x]
    return data


def convertByteMode(data, color):
    if color > 2 or color < 0:
        raise Exception("error invalid color choosen.")
    templist = []
    # extract the colors we want.
    for c in data:
        templist.append(c[color])

    data = templist
    templist = list()
    # extract WORD length list (chunksize depends on matrix width)
    for c in chunks(data, matrix_width):
        templist.append(c)
    data = templist
    templist = list()
    byteval = 0x00
    # pack into WORDS.
    for byte in data:
        for i in range(0, len(byte)):
            if(byte[i]):
                byteval |= (1 << i)
            else:
                byteval |= (0 << i)
        templist.append(byteval)
        byteval = 0x00
    # pack the values into groups of three (that is what
    # is needed for transmitting the data)
    data = templist
    templist = list()
    for c in chunks(data, 3):
        templist.append(tuple(c))
    # make sure the 'led data packets', are three long always.
    if len(templist[len(templist) - 1]) < 3:
        c = list(templist[len(templist) - 1])
        c.append(c[1])
        templist[len(templist) - 1] = tuple(c)
    return templist
