#!/bin/bash
# python2.7 -m cProfile -s 'time' runPatternJob.py --fps=0 --conf=pattern_conf.py --netProtocol=lmcp --showFps=enabled
# pypy -m cProfile -o runPatternJob.cprof runPatternJob.py --color=enabled --conf=pattern_conf.py --netProtocol=lmcp --fps=0 --showFps=enabled

python -m cProfile -o ledart.cprof Ledart/__main__.py --conf=pattern_conf.py --fps=0 --showFps
pyprof2calltree -k -i ledart.cprof

# pyprof2calltree -k -i myscript.cprof
# python2.7 -m cProfile -o runPatternJob.cprof runPatternJob.py --conf=pattern_conf.py --netProtocol=pixelmatrix --fps=0 --showFps=enabled
