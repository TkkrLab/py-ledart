import os, sys

from Ledart.runPatternJob import find_patterns_in_dir
from Ledart.stripinfo import strip_size

currentdir = os.path.dirname(os.path.abspath(sys.argv[0]))

def test():
    patterns = find_patterns_in_dir(os.path.join(currentdir, 'Patterns'))
    assert(len(patterns) != 0)
    for pattern in patterns:
        pat = pattern()
        pat.generate()
    assert(len(pat) == strip_size)

