matrix_height = 20
matrix_width = 20
matrix_size = (matrix_height*matrix_width)
COLOR_ORDER = [2,0,1]

#some matrixes need conversion in some kind
def convertSnakeModes(pattern):
	for y in range(0,matrix_height,2):
		tempList = []
		for x in range(matrix_width-1,-1,-1):
			tempList.append(pattern[y*matrix_width+x])
		for x in range(0, matrix_width):
			pattern[y*matrix_width+x] = tempList[x]
	return pattern
