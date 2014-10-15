#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: getCoG.py

"""
DESCRIPTION:
Calculates center of gravity of a given object (with or without edge detection)
and stores all CoG's in a dictionary per object per handle side per mask side.
Why including mask in CoG calculation: Deubel et al., 1984.
For analyses with CoG without mask applied, simply take keys with 'mask_control'
(cf. parseAsc.py)

CHANGELOG:
- gravDictMask as substitution for gravDict.
"""

from matplotlib import pyplot as plt
from scipy import ndimage
import sys
import os
import numpy as np
import constants
import applyMask
from exparser import Constants


# Set font
plt.rc("font", family=Constants.fontFamily)
plt.rc("font", size=12)


# Define constants:
path = "/home/lotje/Documents/PhD Marseille/Studies/004 - One-object experiment - Orienation effect/Experiment"
pathMaskedObjects = "/home/lotje/Documents/PhD Marseille/Studies/004 - One-object experiment - Orienation effect/Analysis/plots/plots after mask is applied"


width = 720
height = 540

xCen = width/2
yCen = height/2

cenCol = "#edd400"
gravCol = "#f57900"


def centerOfGravity(src, show=False, invert=False, edgeDetect=True):

	"""
	Gets the center of gravity for an image

	Arguments:
	src		--	a 3d numpy array or a string corresponding to an image file

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
	if isinstance(src, basestring):
		src = plt.imread(src)
		
	src = np.array(src, np.uint32)

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
	y, x, col = ndimage.measurements.center_of_mass(src)
	
	# Optionally plot
	if show:		
		plt.imshow(src)
		# Indicate center of image with widht = 720, height = 540:
		plt.axvline(xCen, linestyle = "--", color = cenCol)
		plt.axhline(yCen, linestyle = "--", color = cenCol)
		
		# Indicate center of gravity:
		plt.axvline(x, color = gravCol)
		plt.axhline(y, color = gravCol)
		plt.legend(["center", "CoG"])
		plt.annotate('%.1f,%.1f' % (x,y), (x,y))
		plt.show()
		
	# Transform coordinates, so that 0,0 is center of bitmap
	y -= src.shape[0]/2
	x -= src.shape[1]/2

	return x, y

def gravDictMask(show=True, invert=True, edgeDetect=True,printScreen=False, \
		minDevForDirection = constants.CoGCorrTooLarge):
	
	"""
	Returns a dict containing CoG per masked object depending on rotation.
	
	Properties of the dictionaries:
	key = (object, handle_side) tuple, e.g. ("peeler", "left")
	value = (xCenNew, yCenNew) tuple, e.g. (381.32, 256.60)
	
	Keyword arguments:
	show				--- Boolean indicating whether or not to plot the (inverted, \
							edgedetected) source and its corrected center.
	invert				--- Boolean indicating whether the colors should be inverted, which 
							makes sense if the background is white (otherwise white
							pixels will be most heavily weighted and the corrected center
							will be almost identicaly to width/2, height/2. Default=True.
	edgeDetect -			--	Boolean indicating whether or not to apply a Sobel filter.
							Default = True.
	minDevForDirection	--- Minimum deviation from center of the screen (in px)
							that is considered to be a correction towards or 
							away from the handle.
	
	Returns:
	A dictionaries containing the center of gravity (to which the landing 
	positions should be compared) per object per rotation. Key-value pairs are 
	like so:
	d1[(object,  mask_side, handle_side)] = (x,y)
	For example:
	d1[('knife',  'mask_left', 'right')] = (354.76, 266.98)
	"""
	
	d = {}
	
	l = os.listdir(pathMaskedObjects)
	l.sort()
	
	#for src in os.listdir(pathMaskedObjects):
	for src in l:	
		obj = (os.path.splitext(src)[0]).split("_")[-3]
		
		side = (os.path.splitext(src)[0]).split("_")[-1]
		if side == 'right':		
			maskNormal = "mask_right"
			maskFlip = "mask_left"
		elif side == 'left':
			maskNormal = "mask_left"
			maskFlip = "mask_right"
		else: # Control
			maskNormal = "mask_control"
			maskFlip = "mask_control"
		
		#obj = (os.path.splitext(src)[0])
		
		if os.path.splitext(src)[-1] != ".jpg":
			continue
		
		pictPath = os.path.join(pathMaskedObjects, src)

		xHandleRight, y = centerOfGravity(pictPath, show=show,
			invert=invert, edgeDetect = edgeDetect)
		
		if xHandleRight < -minDevForDirection:
			direction = "correction awayHandle"
		
		elif xHandleRight > minDevForDirection:
			direction = "correction towardsHandle"
			
		else:
			direction = "correction smaller than %s"%minDevForDirection
			
		# Also determine the centre of gravity for flipped objects (with their
		# handle at the right side):		
		xHandleLeft = -xHandleRight
		
		if printScreen:
			print 'Handle right: The center of gravity for the %s is %.1f, %.1f' % \
				(obj, xHandleRight,y)
			print "Handle left: The center of gravity for the %s is %.1f, %.1f" %\
				(obj, xHandleLeft,y)
			print "The direction of the correction is: ", direction
			
		d[obj, maskNormal,  "right"] = xHandleRight,y, direction
		d[obj, maskFlip, "left"] = xHandleLeft, y, direction
	
	
	return d

if __name__ == '__main__':
	
	
	# Save the dictionary to a file:
	
	#import csv

	dict = gravDictMask(show=True, invert=True, edgeDetect=True, \
		printScreen=True)

	#w = csv.writer(open("cog_dict.csv", "w"))
	#for key, val in dict.items():
		#w.writerow([key, val])

	#sys.exit()
	##for key, val in csv.reader(open(exp.get_file("cog_dict.csv"))):
	##new_key = key.strip('()').split(',')
	
		
	#for i in d:
		#print i, d[i]
		#sys.exit()
	
	
	def plotPerObject(onlyControl = False):
		
		d = gravDictMask(show=True, invert=True, edgeDetect=True, \
			printScreen=False)
			
		# Calculate difference score:
		lRightX = []
		lLeftX = []
		lControlX = []

		lRightY = []
		lLeftY = []
		lControlY = []
		
		lNames = []
		l = sorted(d.keys(), key=lambda x: x[0])
		for i in l:
			
			if i[2] == 'right':
				continue

			if i[1] == 'mask_left':
				lLeftX.append(d[i][0])
				lLeftY.append(d[i][1])
			
			if i[1] == 'mask_right':
				lRightX.append(d[i][0])
				lRightY.append(d[i][1])
			
			if i[1] == 'mask_control':
				lControlX.append(d[i][0])
				lControlY.append(d[i][1])
				
				lNames.append(i[0])

		aRightX = np.array(lRightX)
		aLeftX = np.array(lLeftX)
		aControlX = np.array(lControlX)
		
		aRightY = np.array(lRightY)
		aLeftY = np.array(lLeftY)
		aControlY = np.array(lControlY)
				
		fig = plt.figure()
	
		#plt.subplot(211)
		plt.title("x CoG")
		
		if not onlyControl:
			plt.plot(aRightX, color='#3465a4', marker = 'o')
			plt.plot(aLeftX, color='#f57900', marker = 'o')
		plt.plot(aControlX, color = "#73d216", marker = 'o')
		plt.axhline(0, linestyle = "--", color = "#555753")
		plt.axhline(-constants.CoGCorrTooLarge, linestyle = "--", color = "#ef2929")
		plt.axhline(constants.CoGCorrTooLarge, linestyle = "--", color = "#ef2929")
		
		
		plt.xticks(range(0, len(lNames)), lNames, rotation = 90)
		if not onlyControl:
			plt.legend(["mask_left", "mask_right", "mask_control"])
		plt.savefig("CoG per object - onlyControl = %s.jpg"%onlyControl)
		print 'xxx'
		diff = aRightX - aLeftX

		#plt.subplot(212)
		#plt.title("y CoG")
		
		#plt.plot(aRightY, color='blue')
		#plt.plot(aLeftY, color='red')
		#plt.plot(aControlY, color = "green")
		
		#plt.xticks(range(0, len(lNames)), lNames, rotation = 90)
		#plt.legend(["mask_left", "mask_right", "mask_control"])
		#plt.savefig("CoG_per_object.jpg")
		#diff = aRightY - aLeftY
		
		
		
	plotPerObject(onlyControl = False)
	plotPerObject(onlyControl = True)

	