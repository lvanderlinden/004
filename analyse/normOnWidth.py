"""
DESCRIPTION:
Normalizes coordinates relative to stimulus width.

Note: use the width and the height of the bbox around the non-white px within
the PNG file, instead of the w and h of the PNG file itself.
"""

from matplotlib import pyplot as plt

def normOnWidth(x,y,w,h,yStim):
	
	"""
	Normalizes landing positions on object width.
	
	Arguments:
	x		---	x coordinate
	y		--- y coordinate
	w		--- width of the bbox
	h 		--- height of the bbox
	yStim	--- yStim 
	"""
	
	# Normalize yStim on display center:
	yStim = -abs(yStim)
	xNorm = float(x)/float(w)
	yNorm = (yStim-float(y))/float(h)
	
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
	
