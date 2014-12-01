from matrix import *

def convertSnakeModes(pattern):
	for y in range(0,matrix_height,2):
		tempList = []
		for x in range(matrix_width-1,-1,-1):
			tempList.append(pattern[y*matrix_width+x])
		for x in range(0, matrix_width):
			pattern[y*matrix_width+x] = tempList[x]
	return pattern
