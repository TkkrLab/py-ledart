#!/bin/bash
# python2.7 -m cProfile -s 'time' runPatternJob.py --fps=0 --conf=pattern_conf.py --netProtocol=lmcp --showFps=enabled
# pyprof2calltree -k -i myscript.cprof
# pyprof2calltree -k -i myscript.cprof
python2.7 -m cProfile -o runPatternJob.cprof runPatternJob.py --conf=pattern_conf.py --matrixSim=disabled --netProtocol=lmcp --fps=0 --showFps=enabled
