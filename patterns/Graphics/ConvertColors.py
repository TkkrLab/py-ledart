from math import floor
from HSLColorTools import *
from HSVColorTools import *
from RGBColorTools import *

def RGBtoHSL(color):
	r,g,b, = color
	r /= 256.0
	g /= 256.0
	b /= 256.0

	maxColor = max(r,g,b)
	minColor = min(r,g,b)

	if(minColor == maxColor):
		h = 0.
		s = 0.
		l = r
	else:
		l = (minColor+maxColor)/2
		if(l<0.5): s=(maxColor-minColor)/(maxColor+minColor)
		if(l >= 0.5): s=(maxColor-minColor)/(2.0-maxColor-minColor)

		if(r == maxColor): h=(g-b)/(maxColor-minColor)
		if(g == maxColor): h=2.0+(b-r)/(maxColor-minColor)
		if(b == maxColor): h=4.0+(r-g)/(maxColor-minColor)
		h /= 6
		if(h < 0): h+=1

	h*=255.
	s*=255.
	l*=255.
	return (int(h), int(s), int(l),)

def HSLtoRGB(color):
	h,s,l = color
	h /= 256.
	s /= 256.
	l /= 256.

	if(s == 0):
		r = l
		g = l
		b = l
	else:
		if(l<0.5):
			temp2 = l*(1+s)
		else:
			temp2 = (l+s)-(l*s)
		temp1 = 2*l-temp2
		tempr=h+1.0/3.0
		if(tempr > 1.0):
			tempr -= 1
		tempg = h
		tempb = h-1.0/3.0
		if(tempb < 0.0):
			tempb+=1

		#red
		if(tempr < 1.0 / 6.0): r = temp1 + (temp2 - temp1) * 6.0 * tempr
		elif(tempr < 0.5): r = temp2
		elif(tempr < 2.0 / 3.0): r = temp1 + (temp2 - temp1) * ((2.0 / 3.0) - tempr) * 6.0
		else: r = temp1

		#green
		if(tempg < 1.0 / 6.0): g = temp1 + (temp2 - temp1) * 6.0 * tempg
		elif(tempg < 0.5): g=temp2
		elif(tempg < 2.0 / 3.0): g = temp1 + (temp2 - temp1) * ((2.0 / 3.0) - tempg) * 6.0
		else: g = temp1

		#blue
		if(tempb < 1.0 / 6.0): b = temp1 + (temp2 - temp1) * 6.0 * tempb
		elif(tempb < 0.5): b = temp2
		elif(tempb < 2.0 / 3.0): b = temp1 + (temp2 - temp1) * ((2.0 / 3.0) - tempb) * 6.0
		else: b = temp1

	r *= 255.
	g *= 255.
	b *= 255.
	return (int(r),int(g),int(b),)

def RGBtoHSV(color):
	r,g,b = color
	r/=256.
	g/=256.
	b/=256.

	maxColor = max(r,g,b)
	minColor = min(r,g,b)

	v = maxColor

	if(maxColor == 0.0):
		s = 0.0
	else:
		s = (maxColor - minColor)/maxColor

	if(s==0.0):
		h = 0.0
	else:
		if(r == maxColor):
			h = (g-b)/(maColor-minColor)
		if(g == maxColor):
			h = 2.0 + (b-r) / (maxColor-minColor)
		if(b == maxColor):
			h = 4.0 + (r-g) / (maxColor-minColor)
		h/=6.0
		if(h<0.0):
			h+=1
	h*=255.
	s*=255.
	v*=255.
	return (int(h),int(s),int(v),)


def HSVtoRGB(color):
	h,s,v = color
	h/=256.
	s/=256.
	v/=256.

	if(s==0.):
		r = v
		g = v
		b = v
	else:
		h *= 6.0
		i = int(floor(h))
		f = h - i

		p = v*(1.0-s)
		q = v*(1.0-(s*f))
		t = v*(1.0-(s*(1.0-f)))

		if i == 0:
			r=v;g=t;b=p
		if i == 1:
			r=q;g=v;b=p
		if i == 2:
			r=p;g=v;b=t
		if i == 3:
			r=p;g=q;b=v
		if i == 4:
			r=t;g=p;b=v
		if i == 5:
			r=v;g=p;b=q
	r*=255.
	g*=255.
	b*=255.
	return (int(r),int(g),int(b),)