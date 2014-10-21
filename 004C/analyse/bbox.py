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
	left,upper,right,lower = im.getbbox()

	
	wBox = right-left
	hBox = lower-upper
	
	aspectRatio = wBox/hBox
	
	wBoxScaled = wBox/constants.scale
	hBoxScaled = wBoxScaled/aspectRatio

	print "Unscaled"
	print "w = ", wBox
	print "h = ", hBox
	print "Scaled:"
	print "w = ", wBoxScaled
	print "h = ", hBoxScaled


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
		bbox(f)
		
	