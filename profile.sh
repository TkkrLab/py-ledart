#!/bin/bash
# python2.7 -m cProfile -s 'time' runPatternJob.py --fps=0 --conf=pattern_conf.py --netProtocol=lmcp --showFps=enabled
# python2.7 -m cProfile -o runPatternJob.cprof runPatternJob.py --color=enabled --conf=pattern_conf.py --netProtocol=lmcp --fps=0 --showFps=enabled
python2.7 -m cProfile -o runPatternJob.cprof runPatternJob.py --color=enabled --fps=0 --netSilent=enabled --matrixSim=enabled --pixelSize=7 --conf=pattern_conf.py
pyprof2calltree2 -k -i runPatternJob.cprof
# pyprof2calltree -k -i myscript.cprof
# pypy -m cProfile -o runPatternJob.cprof runPatternJob.py --conf=pattern_conf.py --netProtocol=pixelmatrix --fps=0 --showFps=enabled
