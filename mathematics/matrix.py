class Matrix:
	def __init__(self, val):
		self.v = []
		for i in range(0,9):
			self.v.append(val)
	def g(self, row, col):
		return self.v[(row-1)*3 + col-1]
	def s(self, row, col, val):
		self.v[(row-1)*3 + col-1] = float(val)
	def printToScreen(self):
		for i in range(0,3):
				print(str(self.g(i+1,1))+"\t"+str(self.g(i+1,2))+"\t"+str(self.g(i+1,3)))
	def multiplybyscalar(self, scalar):
		for i in range(0,9):
			self.v[i] *= scalar