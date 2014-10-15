#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import numpy as np
from matplotlib import pyplot as plt
from scipy import ndimage, interpolate, misc
from exparser import TraceKit as tk
from skimage import draw

def fromRadialShape(a, r, shape):

	"""
	desc:
		Generates an image array based on angle and radius information. The
		image will be 0 for background and 1 for shape.

	arguments:
		a:
			desc:	An array with angles (radial).
			type:	ndarray
		r:
			desc:	An array with radii (pixels).
			type:	ndarray
		shape:
			desc:	The shape (width, height) for the resulting shape.
			type:	tuple

	returns:
		desc:	An image.
		type:	ndarray
	"""

	x = shape[0]/2 + r * np.cos(a)
	y = shape[1]/2 + r * np.sin(a)
	rr, cc = draw.polygon(x, y)
	im = np.zeros(shape)
	im[rr, cc] = 1
	return im

def toRadialShape(im, s=1024, smooth=501):

	"""
	desc:
		Extracts the radial outline from an image.

	argumens:
		im:
			desc:	An image with 0 for background and 1 for shape.
			type:	ndarray

	keywords:
		s:
			desc:	The length of the output arrays.
			type:	int
		smooth:
			desc:	Smoothing window for the radius or None for no smoothing.
			type:	[int, NoneType]

	returns:
		desc:	A tuple with an array of angles and an array of radii.
		type:	tuple
	"""

	im = edgeDetect(im)
	cx = im.shape[0]/2
	cy = im.shape[1]/2
	x, y = np.where(im != 0)
	a = np.arctan2(y-cy, x-cx)
	r = np.sqrt((x-cx)**2+(y-cy)**2)
	a = np.concatenate( (a-2*np.pi, a, a+2*np.pi) )
	r = np.concatenate( (r, r, r ) )
	i = np.argsort(a)
	a = a[i]
	r = r[i]
	if smooth != None:
		r = tk.smooth(r, windowLen=smooth)
	f = interpolate.interp1d(a, r)
	ia = np.linspace(-np.pi, np.pi, s)
	ir = f(ia)
	return ia, ir

def readBinIm(path):

	"""
	desc:
		Reads an image, converts to binary (0 for background, 1 for shape), and
		fills any internal holes.

	arguments:
		path:
			desc:	The image path.
			type:	[str, unicode]

	returns:
		desc:	An image array.
		type:	ndarray
	"""

	im = ndimage.imread(path, flatten=True)
	i1 = np.where(im == 255)
	i2 = np.where(im != 255)
	im[i1] = 0
	im[i2] = 1
	im = ndimage.binary_fill_holes(im)
	return im

def edgeDetect(im):

	"""
	desc:
		Performs Sobel edge detection on an image.

	arguments:
		im:
			desc:	An image array.
			type:	ndarray

	returns:
		desc:	An image array.
		type:	ndarray
	"""

	dx = ndimage.sobel(im, 0)
	dy = ndimage.sobel(im, 1)
	mag = np.hypot(dx, dy)
	mag /= np.max(mag)
	mag[np.where(mag != 0)] = 1
	return mag

def addNoise(im, n=.25):

	"""
	desc:
		Adds noise to an image.

	arguments:
		im:
			desc:	An image array.
			type:	ndarray

	keywords:
		n:
			desc:	The noise level (0-1).
			type:	float

	returns:
		desc:	An image array.
		type:	ndarray
	"""

	im = n+(1-n*2)*im
	r = np.random.rand(im.shape[0], im.shape[1])
	r = r*2*n-n
	im += r
	return im

if __name__ == '__main__':

	lr = []
	for path in os.listdir('src'):
		if not path.endswith('.jpg'):
			continue
		print path
		im = readBinIm('src/'+path)
		a, r = toRadialShape(im)
		im = fromRadialShape(a, r, im.shape)
		misc.imsave('mask/%s' % path, im)
		#ns = addNoise(im)
		#misc.imsave('mask-noise/%s' % path, ns)
		lr.append(r)

	ar = np.array(lr)
	for i in range(50):
		print 'mix-mask %d' % i
		sar = ar[np.random.choice(ar.shape[0], 2)]
		im = fromRadialShape(a, sar.mean(axis=0), im.shape)
		misc.imsave('mask-mix/mask-%.3d.png' % i, im)
		#ns = addNoise(im)
		#misc.imsave('mask-mix-noise/mask-%.3d.png' % i, ns)
