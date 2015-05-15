from runPatternJob import find_patterns_in_dir
from matrix import matrix_size


def test():
    patterns = find_patterns_in_dir('patterns')
    assert(len(patterns) != 0)
    for pattern in patterns:
        pat = pattern()
        generated = pat.generate()
        print(pat, type(generated))
        print(generated)
        assert(len(generated) == matrix_size)
