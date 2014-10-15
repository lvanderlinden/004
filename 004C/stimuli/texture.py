#!/usr/bin/env python
#-*- coding:utf-8 -*-

from scipy import ndimage, misc
import numpy as np
from matplotlib import pyplot as plt
import os

res = (1280, 960)

def isArrayIm(v):

	"""
	Checks whether a value is a image-like numpy array.

	Arguments:
	v	--	The value to check.

	Returns:
	True if v is image-like, False otherwise.
	"""

	return isinstance(v, np.ndarray) and len(v.shape) in (2,3)

def isPoint(v, nDim=2):

	"""
	Checks whether a value is point-like, i.e. a coordinate or resolution tuple.

	Arguments:
	v		--	The value to check.

	Keyword arguments:
	nDim	--	The dimensionality of the point. (default=2)

	Returns:
	True if v is point-like, False otherwise.
	"""

	if not isinstance(v, tuple):
		return False
	if len(v) != nDim:
		return False
	for i in range(nDim):
		if not isinstance(v[i], int):
			return False
	return True

def paste(src, dst, pos):

	"""
	Pastes a source image onto a destination image at position pos. The paste
	may occur partly outside the boundaries of the destination image.

	Arguments:
	src		--	The source image as numpy array.
	dst		--	The destination image as numpy array.
	pos		--	The top-left position for the paste. Must be a (row, col) tuple.

	Returns:
	A copy of the destination image with the source image pasted onto it.
	"""

	# Check arguments
	if not isArrayIm(src):
		raise Exception('src must be a two- or three-dimensional numpy array')
	if not isArrayIm(dst):
		raise Exception('dst must be a two- or three-dimensional numpy array')
	if len(srcIm.shape) != len(dst.shape):
		raise Exception('src and dst must have the same number of dimensions')
	if not isPoint(pos):
		raise Exception('pos must be an (int, int) tuple')

	dst = dst.copy() # Copy so we don't modify in place
	dstRows = dst.shape[0]
	dstCols = dst.shape[1]
	srcRows = srcIm.shape[0]
	srcCols = srcIm.shape[1]
	row, col = pos
	# Crop the source image if (when pasted) it falls partly outside of the
	# destination image
	rowMargin = dstRows - row - srcRows
	if rowMargin < 0:
		src = src[:rowMargin]
	colMargin = dstCols - col - srcCols
	if colMargin < 0:
		src = src[:,:colMargin]
	if row < 0:
		src = src[-row:]
		row = 0
	if col < 0:
		src = src[:,-col:]
		col = 0
	srcRows = srcIm.shape[0]
	srcCols = srcIm.shape[1]
	# Paste with preserving transparency
	if len(dst.shape) == 3 and dst.shape[2] == 4:
		_rows, _cols  = np.where(src[:,:,3] != 0)
		for _row, _col in zip(_rows, _cols):
			dst[row+_row, col+_col] = src[_row, _col]
	else:
		# Paste without transparency
		dst[row:row+srcRows, col:col+srcCols] = src
	return dst

def createRandomBg(srcIm, dst, res=res):

	"""
	Creates a background surface which contains randomly placed copies of a
	series of pictures that fully cover the surface.

	Arguments:
	lSrc	--	A list of source images, where each source image as a numpy
				array.
	dst		--	The destination image as numpy array.

	Keyword arguments:
	res		--	The resolution of the output image.
	"""

	# Check arguments
	#if not isinstance(lSrc, list):
	#	raise Exception('lSrc must be a list of images')
	#for src in lSrc:
	if not isArrayIm(srcIm):
		raise Exception(
			'Items in lSrc must be two- or three-dimensional numpy arrays')
	if not isArrayIm(dst):
		raise Exception('dst must be a two- or three-dimensional numpy array')
	if len(srcIm.shape) != len(dst.shape):
		raise Exception('src and dst must have the same number of dimensions')
	if not isPoint(res):
		raise Exception('res must be an (int, int) tuple')

	cycle = 0
	while True:
		# Get a list of indices where the alpha channel is 0 (i.e. transparent)
		rows, cols = np.where(dst[:,:,3] == 0)
		# Break the loop if there are no more transparent pixels
		if len(rows) == 0:
			break
		print '%d: N(transparent) == %d' % (cycle, np.sum(dst[:,:,3] == 0))
		# Get a random transparent pixel
		i = np.random.randint(0, len(rows))
		row = rows[i]
		col = cols[i]
		print '%d: dst:empty %d:(%d, %d)' % (cycle, i, row, col)
		# Get a random image and a random non-transparent pixel in this image
		#src = lSrc[0]
		#print src
		rows, cols = np.where(srcIm[:,:,3] != 0)
		i = np.random.randint(0, len(rows)-1)
		_row = rows[i]
		_col = cols[i]
		print '%d: src:non-empty %d:(%d, %d)' % (cycle, i, _row, _col)
		# Pase the input image into the output image
		print '%d: Paste @ (%d,%d)' % (cycle, row-_row, col-_col)
		dst = paste(srcIm, dst, (row-_row, col-_col))
		cycle += 1
	return dst

if __name__ == '__main__':

	# This example assumes that there are two test images in a subfolder called
	# 'test'.
	src = "src"
	dst = "texture input"
	for stim in os.listdir(src):
		print stim
		
		if not "hammer.png" in stim:
			continue
		stimPath = os.path.join(src, stim)
		srcIm = ndimage.imread(stimPath)
		 #ndimage.imread('test/input2.png')]
		dstStim = np.zeros( (res[0], res[1], 4), dtype=np.uint8)
		dstStim = createRandomBg(srcIm, dstStim)
		misc.imsave(os.path.join(dst, "texture_%s" % stim), dstStim)
		#plt.imshow(dst)
		#plt.savefig("texture_%s" % stim)
