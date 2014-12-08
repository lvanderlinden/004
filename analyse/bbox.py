"""
Find bbox per object.
Note that we take the scaling factor (as used in OpenSesame) into account
by dividing the raw bbox by 3.
"""

import math
import numpy as np
from matplotlib import pyplot as plt
import constants
import os
from PIL import Image, ImageChops
from scipy import ndimage

def trimLabel(labels, minSize=100, verbose = False):
	
	"""
	Remove all labels that are smaller than minSize.
	NOTE: copied from corpus scripts: StimProc package, trim.py
	
	Arguments:
	labels			---- npy array containing continguous regions.
	
	Keyword arguments:
	minSize			--- minimum number of px for something to count as an object
						(rather than a group of floating pixels)
	
	Returns trimmed labels (npy array containing continguous regions from
	which the too-small regions are removed)
	"""
	
	
	for obj in np.unique(labels):
		if obj == 0: # Object 0 is the background
			continue
		y, x = np.where(labels == obj)
		size = len(x)*len(y)
		if size < minSize:
			if verbose:
				print '\tObject %d was to small (%d < %d), ignoring' % (obj, \
					size, minSize)
			labels[y,x] = 0
	
	# Return trimmed labels
	labels[np.where(labels != 0)] = 1
	
	return labels

def bbox(stim, plot = False):

	"""
	Finds bbox around SCALED stimulus.
	
	Arguments:
	stim		--- filename of the stimulus
	
	Returns scaled width and height of the bbox
	"""
	
	path = os.path.join(constants.srcStim, stim)
	im = Image.open(path)
	im = ImageChops.invert(im)
	#norm = ((im-im.min()) / (im.max() - im.min())) *-1 + 1
	
	#labels, n = ndimage.measurements.label(im)
	#plt.imshow(labels)
	#plt.show()
	#im = trimLabel(labels)
	
	#im = ndimage.imread(path, flatten=True)
	#norm = ((im-im.min()) / (im.max() - im.min())) *-1 + 1
	#labels, n = ndimage.measurements.label(norm)
	#plt.imshow(labels)
	#plt.show()

	#trimmed = trimLabel(labels, \
	#minSize = 100)
	#im = Image.fromarray(trimmed)
	
	left,upper,right,lower = im.getbbox()

	
	wBox = right-left
	hBox = lower-upper
	
	aspectRatio = wBox/hBox
	
	wBoxScaled = wBox/constants.scale
	hBoxScaled = wBoxScaled/aspectRatio

	if plot:
		plt.imshow(im)
		plt.axvline(left)
		plt.axvline(right)
		plt.axhline(upper)
		plt.axhline(lower)
		plt.show()
	
	return wBoxScaled, hBoxScaled
	
	
if __name__ == "__main__":
	
	for f in os.listdir(constants.srcStim):
		if os.path.splitext(f)[-1] != ".png":
			continue
		bbox(f, plot = True)
		
	