"""
DESCRIPTION:
Flip landing positions as if handle was always oriented to the right
"""

from matplotlib import pyplot as plt
import constants

def flip(x,y, flipCond, vf, plot = True):
	
	"""
	Converts landing positions relative to flip, such that landing positions
	should be interpreted as if handle was always on the right.
	
	NOTE: because of the rotation, LPs should be flipped another time if the
	stimuli was presented in the LVF (alpha = 160, 180 or 200)
	
	Arguments:
	x		--- to-be-flipped x coordinate
	y		--- to-be-flipped y coordinate
	flipCond 	--- {'left', 'right'}, flip condition
	
	Returns flipped (xFlip,yFlip) tuple
	"""
	
	if flipCond == "right":
		xFlip = x
		yFlip = y
	if flipCond == "left":
		xFlip = x*-1
		yFlip = y
	
	if vf == "lower":
		xFlip *= -1
	
	if plot:
		fig = plt.figure()
		plt.title("flip = %s" % flipCond)
		plt.scatter(x,y, color = "blue", label = "start")
		plt.scatter(xFlip,yFlip, color = "red", label = "end")
		plt.legend()
		plt.xlim(-constants.xCen, constants.xCen)
		plt.ylim(-constants.yCen, constants.yCen)
		plt.axvline(0)
		plt.axhline(0)
		plt.show()
	
	
	
	return xFlip, yFlip