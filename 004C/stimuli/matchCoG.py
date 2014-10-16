#!/usr/bin/env python
#-*- coding:utf-8 -*-

"""
DESCRIPTION:
Transforms non-objects until CoG matches the CoG of the real object.
"""


from exparser.DataMatrix import DataMatrix
import os
import cog
import numpy as np
from matplotlib import pyplot as plt
from scipy import ndimage, interpolate, misc
from exparser import TraceKit as tk
from skimage import draw

# Size of the bitmaps:
width = 720
height = 540

# Centers of the bitmap:
xCen = width/2
yCen = height/2

srcOb = "src"
srcNob = "non-objects with texture"
dst = "final"


def matchCog(path, f=1.025, xy=None, th=1, show=False):

	"""
	desc:
		Gets the center of gravity for an image, and optionally transforms the
		image to reach a target center of gravity.

	arguments:
		path:	The path to the image.

	keywords:
		f:		The factor to transform the image for reaching a target cog.
				Lower values are more accurate, but slower.
		xy:		A target cog tuple, or None.
		th:		Threshold cog difference (default = 10)
		show:	Indicates whether a plot should be shown.
	"""
	
	_src = ndimage.imread(path)[:,:,:3]	
	src = np.empty(_src.shape, dtype=np.uint32)
	src[:] = _src
	orig = src.copy()
	left = 1.
	right = 1.
	while True:				
		#im = np.array(_src, np.uint32)
		x, y = cog.cog(src.copy())		
		print '	COG = %.2f, %.2f' % (x, y)
		if xy == None or abs(x-xy[0]) < th:
			break
		print '	Transforming to change CoG!'
		if x > xy[0]:
			left *= f
			right /= f**2
		else:
			left /= f**2
			right *= f
		src = transform(orig, left=left, right=right)
	#misc.imsave(path+'.cog-correct.jpg', src)
	if "non-object" in path:
		misc.imsave(os.path.join(dst, os.path.basename(path)), src)
	else:
		misc.imsave(os.path.join(dst, "object_%s" % os.path.basename(path)), src)
	xc = src.shape[1]/2
	yc = src.shape[0]/2
	if show:
		plt.imshow(src)
		plt.axhline(y+yc, color='red')
		plt.axvline(x+xc, color='red')
		plt.axhline(yc, color='blue')
		plt.axvline(xc, color='blue')
		plt.show()
	return x, y

def transform(im, left=1., right=1.):

	"""
	desc:
		Transforms the image by making the left thinner and the right thicker,
		or vice versa.

	arguments:
		im:		An image array.

	keywords:
		left:	The left thickness, where 1 is the original thickness.
		right:	The right thickness.
	"""

	left = min(3., left)
	right = min(3., right)
	im2 = np.empty(im.shape, dtype=im.dtype)
	im2[:] = 255
	yc = im.shape[0]/2
	print '	transform: %.4f - %.4f' % (left, right)
	transform = np.linspace(left, right, im.shape[1])
	#plt.plot(transform)
	#plt.show()
	for x in range(im.shape[1]):
		for y in range(im.shape[0]):
			dy = y-yc
			#print x, dy
			y2from = yc+transform[x]*dy
			y2to = yc+transform[x]*(dy+1)
			#print '%.2f -> (%.2f:%.2f)' % (y, y2from, y2to)
			if y2from > 0 and y2to < im2.shape[0]:
				im2[y2from:y2to,x] = im[y,x]
	return im2

if __name__ == '__main__':



	l = [['img', 'xCogOrig', 'yCogOrig', 'xCogMatch', 'yCogMatch']]
	for obj in os.listdir(srcOb):
		
		#if not "paintbrush" in obj:
		#	continue
		if "png" in obj or 'cog-correct' in obj:
			continue
		nob = "non-object_%s" % obj		
		objPath = os.path.join(srcOb, obj)
		nobPath = os.path.join(srcNob, nob)
		print
		print 'Original %s' % objPath
		x, y = matchCog(objPath)
		print "COG original object = ", x
		#sys.exit()
		
		print 'Match %s' % nobPath
		_x, _y = matchCog(nobPath, xy=(x,y))
		l.append([obj, x, y, _x, _y])
		#plt.show()
		#break

	dm = DataMatrix(l)
	print dm
	dm.save('cogMatch.csv')
