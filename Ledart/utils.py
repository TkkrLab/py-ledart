import os, sys
import traceback


"""
    these functions are utils, that are handy to have for various things.
"""

def matrix(x=0, y=0, width=1, height=1):
    return [x, y, width, height]

def ledstrip(length=1, channel=0):
    return [0, channel, 1, length]

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

def xfrange(start, stop, step):
    """
        returns a iterator that has a range of floats.
        with float start till float stop with float steps.
    """
    i = 0
    while start + i * step < stop:
        yield start + i * step
        i += 1

def translate(value, leftmin, leftmax, rightmin, rightmax):
    leftspan = leftmax - leftmin
    rightspan = rightmax - rightmin
    if leftspan == 0:
        return 0
    valuescaled = float(value - leftmin) / float(leftspan)
    return rightmin + (valuescaled * rightspan)

""" prints out a trace """
def get_trace():
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    fmt = (exc_type, fname, exc_tb.tb_lineno)
    fmtstr = "%s:%s:%s" % fmt
    return fmtstr

""" returns a list of objects found in a directory/module """
def find_patterns_in_dir(dir):
    patterns = []
    # see if dir is already in path. else add it.
    if dir not in sys.path:
        sys.path.append(dir)
    else:
        print("directory in path.")
    # for everything in a directory.
    for item in os.listdir(dir):
        # if it is a source file.
        if item.endswith(".py") and not item.startswith("__"):
            # extract the file name and import it.
            sfile = item.split('.')[0]
            try:
                print(sfile)
                mod = __import__(sfile)
            except Exception as e:
                print("%s:Couldn't import module cause: %s" % (sfile, e))
                traceback.print_exc()
                continue
            # extract classes
            classes = get_pattern_classes(mod)
            # if any found:
            if classes:
                # append the object to patterns
                patterns += classes
    # return the patterns
    return list(set(patterns))

""" returns a list of objects that contain a generate function. """
def get_pattern_classes(module):
    # holds the patterns that are found
    patterns = []
    # look in the module dictionary for objects with generate function
    for obj in module.__dict__:
        # if we find objects
        if isinstance(obj, object):
            try:
                # we try and get that objects dictionary.
                # if it's a class it will contain methods and more.
                obj_dict = module.__dict__[obj].__dict__
                if(obj_dict['generate']):
                    patterns.append(module.__dict__[obj])
            except:
                # continue if we try and read something we can't.
                continue
    # return a list of classes that have a generate function in them
    return patterns

""" loads variables from a config file, that is actually a python file."""
def load_targets(configfile):
    # this function allows loading of the config files specified by
    # --config=configfile and load patterns defined in there.

    # test if the config file exists, if not it's maybe a local file
    # and else it's probably a path description + file.
    basepath = os.path.dirname(os.path.realpath(__file__))
    variables = dict()
    # variables['basedir'] = basepath
    
    if not os.path.exists(configfile):
        configfile = os.path.join(basepath, "configs", configfile)

    with open(configfile) as f:
        exec(f, variables)

    targets = variables.get('targets', None)
    protocol = variables.get('protocol', None)
    matrix_sim = variables.get('matrixsim', None)

    # print("configfile: %s" % configfile)
    # print("protocol: %s" % protocol)
    # print("matrixsim: %s" % matrix_sim)
    # print("targets: %s" % (str(targets)))

    return (targets, protocol, matrix_sim)

def checkList(first, second):
    for item1, item2 in zip(first, second):
        if item1 != item2:
            return False
    return True
