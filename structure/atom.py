from math import sqrt

class Atom:
	"""Defines an atom, contains permutation classes"""
	def __init__(self, ell, xx, yy, zz):
		self.el = ell # the shorthand notation for the element
		self.x = float(xx)
		self.y = float(yy)
		self.z = float(zz)
		self.setPosition()
	def setPosition(self):
		self.r = [self.x, self.y, self.z]
	def printToScreen(self):
		print(self.el + "\t" + str(self.x) + "\t" + str(self.y) + "\t" + str(self.z))
	def translate(self, xx, yy, zz):
		self.x += xx
		self.y += yy
		self.z += zz
		self.setPosition()
	def rotate(self, rmat):
		nx = rmat.g(1,1) * self.x + rmat.g(1,2) * self.y + rmat.g(1,3) * self.z;
		ny = rmat.g(2,1) * self.x + rmat.g(2,2) * self.y + rmat.g(2,3) * self.z;
		nz = rmat.g(3,1) * self.x + rmat.g(3,2) * self.y + rmat.g(3,3) * self.z;
		self.x = nx;
		self.y = ny;
		self.z = nz;
		self.setPosition()
	def getColor(self):
		if self.el == "Ru":
			return [0.0,1.0,0.0]
		if self.el == "C":
			return [0.0,0.0,0.0]
		if self.el == "O":
			return [1.0,0.0,0.0]
		return [1.0,0.0,0.0]
	def getRadius(self):
		if self.el == "Ru":
			return 0.8
		if self.el == "C":
			return 0.6
		if self.el == "O":
			return 0.6
		return 1.0
	def dist(self, atom):
		dx = self.x - atom.x
		dy = self.y - atom.y
		dz = self.z - atom.z

		return sqrt(dx**2 + dy**2 + dz**2)