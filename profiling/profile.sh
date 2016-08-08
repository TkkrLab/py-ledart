#!/bin/bash
# python2.7 -m cProfile -s 'time' runPatternJob.py --fps=0 --conf=pattern_conf.py --netProtocol=lmcp --showFps=enabled
# python2.7 -m cProfile -o runPatternJob.cprof runPatternJob.py --color=enabled --conf=pattern_conf.py --netProtocol=lmcp --fps=0 --showFps=enabled
pypy -m cProfile -o Ledart.cprof Ledart/runPatternJob.py --color=disabled --fps=0 --conf=pattern_conf.py --netProtocol=legacylmcp --showFps=enabled
pyprof2calltree2 -k -i Ledart.cprof
# pyprof2calltree -k -i myscript.cprof
# pypy -m cProfile -o runPatternJob.cprof runPatternJob.py --conf=pattern_conf.py --netProtocol=pixelmatrix --fps=0 --showFps=enabled
