from Ledart.Tools.Graphics import Surface


# this function swaps widht and height
def convert_dim_layout(data):
    ndata = Surface(width=data.height, height=data.width)
    points = data.get_points()
    for point in points:
        x, y = point
        npoint = (y, x)
        ndata[npoint] = data[point]
    return ndata


# inverts every other line in the y direction.
def convert_snake_layout(data):
    ndata = Surface(data)
    points = ndata.get_points()
    for point in points:
        x, y = point
        if not ((y + 1) % 2):
            for x in range(0, data.width):
                xi = data.width - 1 - x
                pos = xi, y
                ndata[(x, y)] = data[pos]
    return ndata
