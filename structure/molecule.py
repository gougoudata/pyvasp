from structure.bond import Bond

class Molecule:
	"""Defines a molecule, which can hold multiple atoms"""
	def __init__(self):
		self.atoms = [] # make an empty list of atoms on initiation
		self.bonds = [] # make an empty list of atoms on initiation
		self.nrat = 0
	def setBoundingBox(self, mat):
		self.boundingBox = mat
	def addAtom(self, at):
		self.atoms.append(at)
		self.nrat += 1
	def printToScreen(self):
		for atom in self.atoms:
			atom.printToScreen()
	def translate(self, xx, yy, zz):
		for atom in self.atoms:
			atom.translate(xx, yy, zz)
	def printToXYZ(self):
		print(self.nrat)
		print("Molecule")
		for atom in self.atoms:
			atom.printToScreen()
	def printBond(self):
		self.atoms[self.at1].printToScreen()
		self.atoms[self.at2].printToScreen()
	def printToCif(self):
		for atom in self.atoms:
			atom.printToScreen()
	def center(self):
		dx,dy,dz = self.calccenter()
		self.translate(-dx, -dy, -dz)
	def calccenter(self):
		sumx = sumy = sumz = 0
		for atom in self.atoms:
			sumx += atom.x
			sumy += atom.y
			sumz += atom.z
		sumx /= self.nrat
		sumy /= self.nrat
		sumz /= self.nrat
		return sumx, sumy, sumz
	def calcdim(self):
		minx = miny = minz = 1000
		maxx = maxy = maxz = 0
		for atom in self.atoms:
			minx = min(minx, atom.x)
			miny = min(miny, atom.y)
			minz = min(minz, atom.z)
			maxx = max(maxx, atom.x)
			maxy = max(maxy, atom.y)
			maxz = max(maxz, atom.z)
		return (maxx-minx), (maxy-miny), (maxz-minz)
	def direct2cartesian(self, mat):
		for atom in self.atoms:
			x = mat.g(1,1) * atom.x + mat.g(2,1) * atom.y + mat.g(3,1) * atom.z
			y = mat.g(1,2) * atom.x + mat.g(2,2) * atom.y + mat.g(3,2) * atom.z
			z = mat.g(1,3) * atom.x + mat.g(2,3) * atom.y + mat.g(3,3) * atom.z
			atom.x = x
			atom.y = y
			atom.z = z
	def setBonds(self):
		for i in range(0, len(self.atoms)):
			for j in range(i+1, len(self.atoms)):
				if self.atoms[i].dist(self.atoms[j]) < 3:
					self.bonds.append(Bond(self.atoms[i].r, self.atoms[j].r))