"""
DESCRIPTION:
Convert coordinates as if origin is at (0,0)
"""

from matplotlib import pyplot as plt
import constants

def centralOrigin(x,y,plot=False):

	"""
	Converts landing positions as if origin = (0,0)
	
	Arguments:
	x	--- x coordinate
	y	--- y coordinate
	
	Returns an _x,_y tuple containing coordinates relative to center
	"""
	
	_x = x-constants.xCen
	_y = y-constants.yCen
	
	if plot:
		fig = plt.figure()
		plt.suptitle("relative to center")
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