"""
DESCRIPTION:
Rotate landing positions as if all objects were presented on the vertical 
meridian in the upper visual field.

http://en.wikipedia.org/wiki/Rotation_(mathematics)
"""


import math
import numpy as np
from matplotlib import pyplot as plt
import constants


def rotate(x,y,a, plot=False):

	"""
	Rotates x and y by a given angle.
	
	Arguments:
	x	--- unrotated x coordinate
	y	--- unrotated y coordinate
	a 	--- angle in degrees
	
	Returns an xRot, yRot tuple containing the rotated coordinates.
	"""
	
	# Convert angle in degrees to angle in radians:
	_a = math.radians(a)

	# Rotate coordinates.
	xRot = (x*math.cos(_a)) - (y*math.sin(_a))
	yRot = (x*math.sin(_a)) + (y*math.cos(_a))
	
	if plot:
		plt.scatter(x,y, label = "original")
		plt.scatter(xRot, yRot, color = "red", label = "rotated")
		plt.axvline(0)
		plt.axhline(0)
		plt.xlim(-constants.xCen, constants.xCen)
		plt.ylim(-constants.yCen, constants.yCen)
		plt.legend(loc = 'best', frameon=False)
		plt.show()
		
	return xRot, yRot


if __name__ == "__main__":
	
	x = 10
	y = -20
	
	
	orAngle = 200
	#orAngle = 180+orAngle
	angle = orAngle * -1
	plt.scatter(x,y, label = "original")
	xRot, yRot = rotate(x,y, angle)
	plt.scatter(xRot, yRot, color = "red", label = "rotated")
	plt.axvline(0)
	plt.axhline(0)
	plt.xlim(-30, 30)
	plt.ylim(-30, 30)
	plt.legend()
	plt.show()