#!/usr/bin/bash
source venv/bin/activate
pypy -u runPatternJob.py --conf=pattern_conf.py --fps=0 --netProtocol=lmcp --color=enabled --matrixSim=enabled --netSilent=enabled --fullscreen=enabled --pixelSize=4
deactivate
