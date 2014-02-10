import re
from structure.molecule import Molecule
from structure.atom import Atom
from mathematics.matrix import Matrix

# define functions
def readPOTCAR(potcar):
	# first read the potcar, to return a list of elements
	f = open(potcar)
	lines = f.readlines()
	f.close()
	elements = [] # create empty list to hold the elements

	for line in lines:
		# if the line fits a regular expression, then take
		# that line as input to generate an atom
		match = re.search('^ PAW_PBE ([A-Za-z]+) [A-Za-z0-9].*',line);
		if(match):
			el = match.group(1);
			elements.append(el)

	print elements
	return elements


def readPOSCAR(poscar, elements):
	# read the default input file
	f = open(poscar)
	lines = f.readlines()
	f.close()

	mol = Molecule()

	# define system name
	sysname = lines[0]
	
	# construct bounding box matrix
	scalar = float(lines[1])
	mat = Matrix(0)
	match = re.search('^\s*([0-9.-]+)\s+([0-9.-]+)\s+([0-9.-]+)\s*$',lines[2]);
	mat.s(1,1,match.group(1))
	mat.s(1,2,match.group(2))
	mat.s(1,3,match.group(3))
	match = re.search('^\s*([0-9.-]+)\s+([0-9.-]+)\s+([0-9.-]+)\s*$',lines[3]);
	mat.s(2,1,match.group(1))
	mat.s(2,2,match.group(2))
	mat.s(2,3,match.group(3))
	match = re.search('^\s*([0-9.-]+)\s+([0-9.-]+)\s+([0-9.-]+)\s*$',lines[4]);
	mat.s(3,1,match.group(1))
	mat.s(3,2,match.group(2))
	mat.s(3,3,match.group(3))
	mat.multiplybyscalar(scalar)

	mat.printToScreen()
	atoms_per_element = lines[5].split()
	print atoms_per_element

	idx = idx2 = -1
	for elnr in atoms_per_element:
		idx2 += 1
		for i in range(0,int(elnr)):
			idx += 1
			match = re.search('^\s*([0-9.-]+)\s+([0-9.-]+)\s+([0-9.-]+).*$',lines[7+idx]);
			if(match):
				el = elements[idx2]
				x = match.group(1);
				y = match.group(2);
				z = match.group(3);
				at = Atom(el,x,y,z)
				mol.addAtom(at)

	mol.direct2cartesian(mat)
	return mol