"""
	this file contains that describe the cells and the field.
"""
import random

class Life(object):
	def __init__(self, width = 800, height = 600, size = 10, color = (100,100,100)):
		self.surviveAbility = 2
		self.reproductiveNumber = 3
		
		self.cellSize = size
		self.cellColor = color
		
		self.fieldWidth = int(width/self.cellSize)
		self.fieldHeight = int(height/self.cellSize)
		self.fieldSize = self.fieldWidth*self.fieldHeight
		self.field = [1]*self.fieldSize
		
		self.buffer = [0]*self.fieldSize
		
		self.position = 0;
		
		self.createRandomField()
	def process(self):
		for self.position,cell in enumerate(self.field):
			if(self.field[self.position]):
				if(self.totalAround(self.field, self.position) == self.surviveAbility):
					self.buffer[self.position]=1
				elif(self.totalAround(self.field, self.position) == self.surviveAbility+1):
					self.buffer[self.position]=1
				else:
					self.buffer[self.position]=0
			else:
				if(self.totalAround(self.field, self.position) == self.reproductiveNumber):
					self.buffer[self.position] = 1
				else:
					self.buffer[self.position] = 0
		self.copy_buffer(self.buffer, self.field)
	#create a random field
	def createRandomField(self):
		for i,cell in enumerate(self.field):
			self.field[i] = random.randint(0,1);
	def copy_buffer(self, buffer, field):
		for index in xrange(self.fieldSize):
			self.field[index] = self.buffer[index]
		return
	def checkUpper(self, field, position):
		if position-self.fieldWidth > 0:
			if field[position-self.fieldWidth]:
				return 1
			else:
				return 0
		else:
			return 0
		return 0
	def checkLower(self, field, position):
		if position+self.fieldWidth<self.fieldSize:
			if field[position+self.fieldWidth]:
				return 1
			else:
				return 0
		else:
			return 0
		return 0
	#check if there is a cell to the left of the current position in field.
	def checkLeft(self, field, position):
		if(position-1>0):
			if(field[position-1]):
				return 1
			else:
				return 0
		else:
			return 0
		return 0
	#check if there is a cell to the right of the current position in field.
	def checkRight(self, field, position):
		if(position+1<self.fieldSize):
			if(field[position+1]):
				return 1
			else:
				return 0
		else:
			return 0
		return 0
	#check if there is a cell to the upper left of the current position in field.
	def checkUpperLeft(self, field, position):
		if(position-self.fieldWidth+1>0):
			if(field[position-self.fieldWidth+1]):
				return 1
			else:
				return 0
		else:
			return 0
		return 0
	#check if there is a cell to the upper right of the current position in field.
	def checkUpperRight(self, field, position):
		if(position-self.fieldWidth-1>0):
			if(field[position-self.fieldWidth-1]):
				return 1
			else:
				return 0
		else:
			return 0
		return 0
	#check if there is a cell to the lower Left of the current position in field.
	def checkLowerLeft(self, field, position):
		if(position+self.fieldWidth-1<self.fieldSize):
			if(field[position+self.fieldWidth-1]):
				return 1
			else:
				return 0
		else:
			return 0
		return 0
	#check if there is a cell to the lower Right of the current position in field.
	def checkLowerRight(self, field, position):
		if(position+self.fieldWidth+1<self.fieldSize):
			if(field[position+self.fieldWidth+1]):
				return 1
			else:
				return 0
		else:
			return 0
		return 0
	#return how many lifing cels are around a position in field.
	def totalAround(self, field, position):
		around = self.checkUpper(field, position)+self.checkLower(field, position)+self.checkLeft(field, position)+self.checkRight(field, position)+self.checkUpperLeft(field, position)+self.checkUpperRight(field, position)+self.checkLowerLeft(field, position)+self.checkLowerRight(field, position);
		return around
