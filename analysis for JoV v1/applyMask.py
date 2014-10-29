#!/usr/bin/env python

"""
DESCRIPTION:

CHANGELOG:

TODO:
How do I know for sure that what happens here is the same as what I used during the
experiment with PsychoPy?
"""

from matplotlib import pyplot as plt
from scipy import ndimage, misc
import sys
import os
import numpy as np
import constants


# Define constants:
path = "/home/lotje/Documents/PhD Marseille/Studies/004 - Single-object experiment - Handle-orientation effect/004B/experiment"
dst = "/home/lotje/Documents/PhD Marseille/Studies/004 - Single-object experiment - Handle-orientation effect/004A/results/plots/bitmaps after mask is applied"

width = 720
height = 540

xCen = width/2
yCen = height/2




def applyMask(src, maskSide = "right", minTransp = 1, maxTransp = 0, \
		maskWidth = width, showFig = False, saveFig = False, saveExt = ".jpg"):

	"""
	Loads image and applies mask
	
	Arguments:
	src
	
	Keyword arguments:
	mask_side	--- {'right', 'left'}, applies mask either to the left or to 
					the right. Default = 'right'.
	"""
	
	# Load image:
	
	pictName = "%s_mask_%s%s" % (os.path.splitext(src.split("/")[-1])[0], maskSide, \
		saveExt)
	#print pictName
	#sys.exit()
		
	
	# Read if the image is a string and not a numpy array
	if isinstance(src, basestring):
		src = plt.imread(src)			
	srcImage = np.array(src, np.uint32)
	plt.subplot(221)
	plt.imshow(src)
	
	# Make white background of the same shape:
	bg = np.empty(srcImage.shape, dtype=np.uint32)
	bg[:] = 255
	
	plt.subplot(222)
	plt.imshow(bg)

	# Make grating:
	mask = np.empty(srcImage.shape, dtype=np.float64)
	
	for row in range(0, height):
		for col in range(0, 3):	
			if maskSide == "left":
				mask[row,:,col] = np.linspace(maxTransp, minTransp, maskWidth)
			if maskSide == "right":
				mask[row,:,col] = np.linspace(minTransp, maxTransp, maskWidth)
			if maskSide == "control":
				mask[row,:,col] = np.linspace(minTransp, minTransp, maskWidth)
		
	plt.subplot(223)
	plt.imshow(mask)	
	
	# End result:
	# Image * grating + Background * (1-grating):
	maskedImage = np.array((srcImage * mask) + (bg * (1-mask)), dtype=int)	
	plt.subplot(224)
	plt.imshow(maskedImage)	
	savePath = os.path.join(dst, pictName)
	misc.imsave(savePath, maskedImage)	


if __name__ == "__main__":
	
	
	for src in os.listdir(path):
		
		obj = (os.path.splitext(src)[0]).split("_")[-1]
		
		if os.path.splitext(src)[-1] != ".jpg":
			continue
	
		a = applyMask(os.path.join(path, src), showFig = True, saveFig = False,\
			maskSide = "right")
