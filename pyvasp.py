#!

# This is statement is required by the build system to query build info
if __name__ == '__build__':
	raise Exception

import string
__version__ = string.split('$Revision: 0.1 $')[1]
__date__ = string.join(string.split('$Date: 2014/02/10 $')[1:3], ' ')
__author__ = 'Ivo Filot <i.a.w.filot@tue.nl>'

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import re, math
from io.readsource import *

elements = readPOTCAR("POTCAR")
mol = readPOSCAR("POSCAR", elements)
mol.center()
mol.printToXYZ()
mol.setBonds()

# Some api in the chain is translating the keystrokes to this octal string
# so instead of saying: ESCAPE = 27, we use the following.
ESCAPE = '\033'

# Number of the glut window.
window = 0

# rotation angle
rtri = ltri = 0
dimx, dimy, dimz = mol.calcdim()

# A general OpenGL initialization function.  Sets all of the initial parameters. 
def InitGL(Width, Height):				# We call this right after our OpenGL window is created.
	glClearColor(0.0, 0.0, 0.0, 0.0)	# This Will Clear The Background Color To Black
	glClearDepth(1.0)					# Enables Clearing Of The Depth Buffer
	glDepthFunc(GL_LESS)				# The Type Of Depth Test To Do
	glEnable(GL_DEPTH_TEST)				# Enables Depth Testing
	glShadeModel(GL_SMOOTH)				# Enables Smooth Color Shading
	
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()					# Reset The Projection Matrix
	gluPerspective(65.0, float(Width)/float(Height), 5.0, 100.0)

	glMatrixMode(GL_MODELVIEW)

	mat_specular = [1.0, 1.0, 1.0, 1.0];
	mat_shininess= [50.0];
	light_position = [1.5, 1.5, 1.5, 1.0];
	glClearColor(1.0, 1.0, 1.0, 0.0);
	glShadeModel(GL_SMOOTH);
	glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular);
	glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess);
	glLightfv(GL_LIGHT0, GL_POSITION, light_position);
	glColorMaterial(GL_FRONT,GL_DIFFUSE);

	glEnable(GL_COLOR_MATERIAL);
	glEnable(GL_LIGHTING);
	glEnable(GL_LIGHT0);
	glEnable(GL_DEPTH_TEST);

# The function called when our window is resized (which shouldn't happen if you enable fullscreen, below)
def ReSizeGLScene(Width, Height):
    if Height == 0:						# Prevent A Divide By Zero If The Window Is Too Small 
	    Height = 1

    glViewport(0, 0, Width, Height)		# Reset The Current Viewport And Perspective Transformation
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

# The main drawing function. 
def DrawGLScene():
	global ltri, rtri
	# Clear The Screen And The Depth Buffer
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	glPushMatrix()
	glLoadIdentity()					# Reset The View 
	glTranslatef(0, 0, -mol.boundingBox.g(3,3)*1.5);
	glRotatef(rtri, 0.0, 1.0, 0.0);
	glRotatef(ltri, 1.0, 0.0, 0.0);

	for atom in mol.atoms:
		drawAtom(atom)
	for bond in mol.bonds:
		drawBond(bond)

	drawBoundingBox(mol.boundingBox)

	glPopMatrix()

	#  since this is double buffered, swap the buffers to display what just got drawn. 
	glutSwapBuffers()

def drawAtom(atom):
	glPushMatrix();
	glTranslatef(atom.x,atom.y,atom.z);
	color = atom.getColor()
	glColor3f(color[0], color[1], color[2]);
	glutSolidSphere(atom.getRadius(), 30, 30);
	glPopMatrix();

def drawBond(bond):
	drawCylinder(bond.r1, bond.r2, 0.3, [0.2,0.2,0.2])

def drawBoundingBox(mat):
	vec0 = [0,0,0]
	vec1 = [mat.g(1,1),mat.g(1,2),mat.g(1,3)]
	vec2 = [mat.g(2,0),mat.g(2,2),mat.g(2,3)]
	vec3 = [mat.g(3,1),mat.g(3,2),mat.g(3,3)]
	vec4 = [x+y for x,y in zip(vec1,vec2)]
	vec5 = [x+y for x,y in zip(vec2,vec3)]
	vec6 = [x+y for x,y in zip(vec1,vec3)]
	vec7 = [x+y for x,y in zip(vec4,vec3)]

	vx = (mat.g(1,1)+mat.g(2,1)+mat.g(3,1))/2
	vy = (mat.g(1,2)+mat.g(2,2)+mat.g(3,2))/2
	vz = (mat.g(1,3)+mat.g(2,3)+mat.g(3,3))/2
	center = [vx, vy, vz]

	vec0 = [x-y for x,y in zip(vec0,center)]
	vec1 = [x-y for x,y in zip(vec1,center)]
	vec2 = [x-y for x,y in zip(vec2,center)]
	vec3 = [x-y for x,y in zip(vec3,center)]
	vec4 = [x-y for x,y in zip(vec4,center)]
	vec5 = [x-y for x,y in zip(vec5,center)]
	vec6 = [x-y for x,y in zip(vec6,center)]
	vec7 = [x-y for x,y in zip(vec7,center)]

	diameter = 0.1
	color = [0,0,0]

	drawCylinder(vec0, vec1, diameter, color)
	drawCylinder(vec0, vec2, diameter, color)
	drawCylinder(vec0, vec3, diameter, color)
	drawCylinder(vec1, vec4, diameter, color)
	drawCylinder(vec1, vec6, diameter, color)
	drawCylinder(vec2, vec4, diameter, color)
	drawCylinder(vec2, vec5, diameter, color)
	drawCylinder(vec3, vec5, diameter, color)
	drawCylinder(vec3, vec6, diameter, color)
	drawCylinder(vec4, vec7, diameter, color)
	drawCylinder(vec5, vec7, diameter, color)
	drawCylinder(vec6, vec7, diameter, color)

def drawCylinder(vec1, vec2, radius, color):
	vx = vec2[0] - vec1[0];
	vy = vec2[1] - vec1[1];
	vz = vec2[2] - vec1[2];

	height = math.sqrt(vx**2 + vy**2 + vz**2)
	if vz == 0:
		vz = 0.0001

	ax = 57.2957795 * math.acos( vz / height)
	if(vz < 0):
		ax *= -1
	rx = -vy * vz
	ry = vx * vz

	glPushMatrix()
	glTranslate(vec1[0],vec1[1],vec1[2])
	glRotatef(ax, rx, ry, 0.0)
	quadObj = gluNewQuadric()
	glColor3f(color[0], color[1], color[2])
	gluCylinder(quadObj, radius, radius, height, 30, 10)
	glPopMatrix()

# The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)  
def keyPressed(*args):
	global ltri, rtri
	# If escape is pressed, kill everything.
	if args[0] == ESCAPE:
		sys.exit()

	if args[0] == 'd':
		rtri += 5

	if args[0] == 'a':
		rtri -= 5

	if args[0] == 'w':
		ltri += 5

	if args[0] == 's':
		ltri -= 5

	if(rtri >= 360.):
		rtri = 0

	if(rtri < 0):
		rtri = 360

	if(ltri >= 360.):
		ltri = 0

	if(ltri < 0):
		ltri = 360

def main():
	global window
	glutInit(sys.argv)

	# Select type of Display mode:   
	#  Double buffer 
	#  RGBA color
	# Alpha components supported 
	# Depth buffer
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
	
	# get a 640 x 480 window 
	glutInitWindowSize(640, 480)
	
	# the window starts at the upper left corner of the screen 
	glutInitWindowPosition(0, 0)
	
	# Okay, like the C version we retain the window id to use when closing, but for those of you new
	# to Python (like myself), remember this assignment would make the variable local and not global
	# if it weren't for the global declaration at the start of main.
	window = glutCreateWindow("VASP")

   	# Register the drawing function with glut, BUT in Python land, at least using PyOpenGL, we need to
	# set the function pointer and invoke a function to actually register the callback, otherwise it
	# would be very much like the C version of the code.	
	glutDisplayFunc(DrawGLScene)
	
	# Uncomment this line to get full screen.
	# glutFullScreen()

	# When we are doing nothing, redraw the scene.
	glutIdleFunc(DrawGLScene)
	
	# Register the function called when our window is resized.
	glutReshapeFunc(ReSizeGLScene)
	
	# Register the function called when the keyboard is pressed.  
	glutKeyboardFunc(keyPressed)

	# Initialize our window. 
	InitGL(640, 480)

	# Start Event Processing Engine	
	glutMainLoop()

# Print message to console, and kick off the main to get it rolling.
print "Hit ESC key to quit."
main()
