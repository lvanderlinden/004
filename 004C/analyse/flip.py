import math
import numpy as np
from matplotlib import pyplot as plt

"""
DESCRIPTION:
Flip landing positions as if objects were presented with the handle to the
right.
"""

def flip(x,y):

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