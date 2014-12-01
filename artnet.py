#!/usr/bin/python

# 2013-09-02 Aprogas

def buildPacket(universe, dmxdata):
    # Stolen from fire-ohmlogo.py by OHM2013
	size = len(dmxdata) * 3
	#              01234567   8   9   a   b   c   d   e   f   10  11  
	#                         op-code protver seq phy universe len  
	data = bytearray("Art-Net\x00\x00\x50\x00\x0e\x00\x00")
	data += chr(int(universe % 256))
	data += chr(int(universe / 256))
	data += chr(int(size / 256))
	data += chr(int(size % 256))
	for (r, g, b) in dmxdata:
		data += chr(r)
		data += chr(g)
		data += chr(b)
	return data
