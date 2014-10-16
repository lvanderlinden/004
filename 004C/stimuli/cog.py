import os
from scipy import ndimage
from matplotlib import pyplot as plt
import numpy as np

# Size of the bitmaps:
width = 720
height = 540


# Centers of the bitmap:
xCen = width/2
yCen = height/2

# Color:
gravCol = "#f57900"
cenCol = "#729fcf"



def cog(_src, show=False, invert=True, edgeDetect=True, col = True):

	"""
	Gets the center of gravity for an image

	Arguments:
	_src		--	a 3d numpy array or a string corresponding to an image file

	Keyword arguments:
	show			--- Boolean indicating whether or not to plot the (inverted, \
					edgedetected) source and its corrected center.
	invert		--- Boolean indicating whether the colors should be inverted, which 
					makes sense if the background is white (otherwise white
					pixels will be most heavily weighted and the corrected center
					will be almost identicaly to width/2, height/2. Default=True.
	edgeDetect ---	Boolean indicating whether or not to apply a Sobel filter.
					Default = True.
	
	Returns:
	An (x, y) tuple of floats that gives the center of gravity for the image
	"""

	# Read if the image is a string and not a numpy array
	#path, ext = os.path.splitext(src)
	#pict = path.split("/")[-1]
	#figName = "CoG calculation %s invert = %s edgeDetect = %s.svg"%(pict, invert, edgeDetect)



	#if isinstance(src, basestring):
	#	src = plt.imread(src)
	#
	#print src.dtype, np.max(src), np.min(src)
	
	#original = src
	
	#src = np.array(src, np.uint32)	
	
	# TODO: change 'corrCoG.py' such that it takes src as input
#	_src = np.empty(src.shape, dtype=np.uint32)
#	_src[:] = src
	src = _src
		
	# Invert the 0-1 values		
	
	if invert:
		src = 1-src
		
	# Edge detection using Sobel operator, see
	# <http://scipy-lectures.github.com/advanced/image_processing/index.html#edge-detection>
	if edgeDetect:
		sx = ndimage.sobel(src, axis=0, mode='constant')
		sy = ndimage.sobel(src, axis=1, mode='constant')
		src = np.hypot(sx, sy)
		
	# Get center of mass	
	
	if col:
		y, x, col = ndimage.measurements.center_of_mass(src)
	else:
		y, x = ndimage.measurements.center_of_mass(src)
	#Optionally plot
	if show:		
		plt.imshow(original)
		# Indicate center of image with widht = 720, height = 540:
		line1 = plt.axvline(xCen, color = cenCol, linewidth = 3)
		plt.axhline(yCen, color = cenCol,linewidth = 3)
		plt.xticks([])
		plt.yticks([])
		
		# Indicate center of gravity:
		line2 = plt.axvline(x, linestyle = "--", color = gravCol, linewidth = 2)
		plt.axhline(y, linestyle = "--", color = gravCol, linewidth = 2)
		plt.legend([line1, line2], ["center of bitmap", "center of gravity"], loc = 'best')
		#plt.annotate('%.1f,%.1f' % (x,y), (x,y))
		#if "mask_control" in pict:
		#	plt.savefig(figName)
		#	plt.savefig("%s.png" % figName)
		
		#plt.clf()
		plt.show()
		
		
	# Transform coordinates, so that 0,0 is center of bitmap
	y -= src.shape[0]/2
	x -= src.shape[1]/2
	print x, y
	return x, y
