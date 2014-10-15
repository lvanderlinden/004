#!/usr/bin/env python
#-*- coding:utf-8 -*-

from exparser.DataMatrix import DataMatrix
#from generate import edgeDetect
import os
import numpy as np
from matplotlib import pyplot as plt
from scipy import ndimage, interpolate, misc
from exparser import TraceKit as tk
from skimage import draw

def cog(path, f=1.25, xy=None, th=10, show=False):

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

	src = ndimage.imread(path)[:,:,:3]
	while True:
		im = np.array(src, np.uint32)
		
		#if edgeDetect:
		sx = ndimage.sobel(src, axis=0, mode='constant')
		sy = ndimage.sobel(src, axis=1, mode='constant')
		src = np.hypot(sx, sy)
		
		#im = edgeDetect(im)
		y, x, col = ndimage.measurements.center_of_mass(im)
		print src
		print x
		sys.exit()
		print 'COG = %.2f, %.2f' % (x, y)
		if xy == None or abs(x-xy[0]) < th:
			break
		print 'Transforming to change CoG!'
		if x > xy[0]:
			src = transform(src, left=f, right=1./f)
		else:
			src = transform(src, left=1./f, right=f)
			misc.imsave(path+'.cog-correct.png', src)
	xc = im.shape[1]/2
	yc = im.shape[0]/2
	if show:
		plt.imshow(im)
		plt.axhline(y, color='red')
		plt.axvline(x, color='red')
		plt.axhline(yc, color='blue')
		plt.axvline(xc, color='blue')
	return x, y

def transform(im, left=1, right=1):

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

	im2 = np.empty(im.shape, dtype=im.dtype)
	im2[:] = 255
	yc = im.shape[0]/2
	transform = np.linspace(left, right, im.shape[1])
	for x in range(im.shape[1]):
		for y in range(im.shape[0]):
			dy = y-yc
			y2from = int(yc+transform[x]*dy)
			y2to = int(yc+transform[x]*(dy+1))
			if y2from > 0 and y2to < im2.shape[0]:
				im2[y2from:y2to,x] = im[y,x]
	return im2

if __name__ == '__main__':

	srcOb = "/home/lotje/Documents/PhD Marseille/Studies/004 - Single-object experiment - Handle-orientation effect/004C/stimuli/final/objects"
	srcNob = "/home/lotje/Documents/PhD Marseille/Studies/004 - Single-object experiment - Handle-orientation effect/004C/stimuli/final/non-objects with texture"

	l = [['img', 'xCogOrig', 'yCogOrig', 'xCogMatch', 'yCogMatch']]
	for stimName in os.listdir(srcOb):
		if 
		objPath = os.path.join(srcOb, stimName)
		nobPath = os.path.join(srcNob, stimName)
		#plt.subplot(211)
		print 'Original %s' % objPath
		x, y = cog(objPath)
		#plt.subplot(212)
		print 'Match %s' % nobPath
		_x, _y = cog(nobPath, xy=(x,y))
		l.append([stimName, x, y, _x, _y])
		#plt.show()
		#break

	dm = DataMatrix(l)
	print dm
	dm.save('cogMatch.csv')
