#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: drawRects.py

"""
Following Pajak & Nuthmann (2013), an imaginary just-fitting rectangle is drawn
around the objects to determine an object's 'personal' width and height.
This will enable us to normalize all landing positions.

A dictionary containing width and height per object will be created, that can 
be used during parsing.

NOTE:
The resulting size (w and h) have to be divided by the scaling factor used in OpenSesame
(since objects were not displayed in their original size).
"""

# import Python modules:
import sys
import os
from PIL import Image, ImageFont, ImageDraw, ImageChops


# Folder containing stimuli used for the experiment:
src = "/home/lotje/Documents/PhD Marseille/Studies/004 - Single-object experiment - Handle-orientation effect/004A/results/plots/bitmaps original"
dst = "/home/lotje/Documents/PhD Marseille/Studies/004 - Single-object experiment - Handle-orientation effect/004A/results/plots/bitmaps after being chopped"

print
print
print
print 'ATTENTION: DID YOU TAKE SCALE FACTOR INTO ACCOUNT??'
#sys.exit()

def boxDict():
	
	"""
	Returns a dictionary containing width and height per bitmap.
	"""

	boxDict = {}


	for pict in os.listdir(src):
		
		picName, ext = os.path.splitext(pict)
		if ext != ".jpg":
			continue
		
		# Open the R&P picture:
		picIm = Image.open(os.path.join(src,pict))
		#print 'xx'
		#picIm.show()
		
		# Invert the picutre (because the function bbox works such that
		# it looks for the first non-zero):
		picIm = ImageChops.invert(picIm)
		
		# Calculate the bounding box:
		# See: <http://www.pythonware.com/library/pil/handbook/image.htm>
		
		# Note that due to some slopiness in the original R&P files,
		# this doesn't always work that well. Manual removal of the random
		# non-white spots in the GIMP is necessary.
		bbox = picIm.getbbox()
		
		# Crop the picture according to the bounding box:
		picIm = picIm.crop(bbox)
		
		# And invert back to the original black-and-white ratio.
		picIm = ImageChops.invert(picIm)

		# Save the object:
		name = "handle_right_%s"%pict
		picIm.save(os.path.join(dst, name))
		
		# Determine size:
		w, h =  picIm.size
		boxDict[picName] = w, h 
		
		# Also make a .png with handle left:
		handleLeft = picIm.transpose(Image.FLIP_LEFT_RIGHT)
		nameLeft = "handle_left_%s"%pict
		handleLeft.save(os.path.join(dst,nameLeft))

	return boxDict

if __name__ == "__main__":
	
	d = boxDict()
	
	for i in d:
		
		print i, d[i]
		
		
		