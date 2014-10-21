import math
import numpy as np
from matplotlib import pyplot as plt

import constants
"""
DESCRIPTION:
- Convert landing positions as if central (x,y) = (0,0)
- Normalize landing positions on stimulus width

NOTE: In PsychoPy, upper = positive.
"""

def relToCenter(x,y,plot=False):

	"""
	Converts landing positions as if center = (0,0)
	
	Arguments:
	x	--- x coordinate
	y	--- y coordinate
	
	Returns an _x,_y tuple containing coordinates relative to center
	"""
	
	# Convert angle in degrees to angle in radians:
	
	
	_x = x-constants.xCen
	_y = y-constants.yCen
	
	if plot:
		plt.subplot(211)
		plt.scatter(x,y, color = "red", label = "start")
		plt.xlim(0,constants.w)
		plt.ylim(0,constants.h)
		plt.axhline(constants.yCen)
		plt.axvline(constants.xCen)
		plt.subplot(212)
		plt.scatter(_x,_y, color = "red", label = "end")
		plt.xlim(-constants.xCen, constants.xCen)
		plt.ylim(-constants.yCen, constants.yCen)
		plt.axhline(0)
		plt.axvline(0)
		plt.show()
		
	return _x, _y

def relToFlip(x,y, flip, plot = True):
	
	"""
	Converts landing positions relative to flip, such that landing positions
	should be interpreted as if handle was always on the right.
	
	Arguments:
	x		--- to-be-flipped x coordinate
	y		--- to-be-flipped y coordinate
	flip 	--- {'left', 'right'}, flip condition
	
	Returns flipped (xFlip,yFlip) tuple
	"""
	
	if flip == "right":
		xFlip = x
		yFlip = y
	if flip == "left":
		xFlip = x*-1
		yFlip = y
		
	if plot:
		plt.title("flip = %s" % flip)
		plt.scatter(x,y, color = "blue", label = "start")
		plt.scatter(xFlip,yFlip, color = "red", label = "end")
		plt.legend()
		plt.xlim(-constants.xCen, constants.xCen)
		plt.ylim(-constants.yCen, constants.yCen)
		plt.axvline(0)
		plt.axhline(0)
		plt.show()
	
	
	
	return xFlip, yFlip

def normOnWidth(x,y,w,h):
	
	"""
	Normalizes landing positions on object width.
	
	Arguments:
	x		---	x coordinate
	y		--- y coordinate
	w		--- width
	h 		--- height
	"""
	
	xNorm = float(x)/float(w)
	yNorm = float(y)/float(h)
	
	return xNorm, yNorm

if __name__ == "__main__":
	

	w = 10
	h = 4
	
	x = 9
	y = 2
	
	_x,_y = normOnWidth(x,y,w,h)
	print _x
	print _y
	sys.exit()
	
