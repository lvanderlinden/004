#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: getCoG.py

"""
DESCRIPTION:
Calculates center of gravity of a given object (with or without edge detection)
and stores all CoG's in a dictionary per object per handle side per mask side.

Reasoning for including mask in CoG calculation: Deubel et al., 1984.

NOTE:
For analyses with CoG without mask applied, simply take keys with 'mask_control'
(cf. parseAsc.py)

CHANGELOG:
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
plt.rc("font", family="ubuntu")
plt.rc("font", size=18)
#plt.rc("font", color = "#2e3436")

# Define constants:
path = "/home/lotje/Documents/PhD Marseille/Studies/004 - Single-object experiment - Handle-orientation effect/004B/experiment"
pathMaskedObjects = "/home/lotje/Documents/PhD Marseille/Studies/004 - Single-object experiment - Handle-orientation effect/analysis 004/plots after mask is applied"
pathChoppedObjects = "/home/lotje/Documents/PhD Marseille/Studies/004 - Single-object experiment - Handle-orientation effect/004A/results/plots/bitmaps after being chopped"

# Size of the bitmaps:
width = 720
height = 540


# Centers of the bitmap:
xCen = width/2
yCen = height/2

# Color:
gravCol = "#f57900"
cenCol = "#729fcf"


def centerOfGravity(src, show=False, invert=False, edgeDetect=True, col = True):

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
	path, ext = os.path.splitext(src)
	pict = path.split("/")[-1]
	figName = "CoG calculation %s invert = %s edgeDetect = %s.svg"%(pict, invert, edgeDetect)



	if isinstance(src, basestring):
		src = plt.imread(src)
		
	src = np.array(src, np.uint32)
	# Invert the 0-1 values
	
	original = src
	
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
	# Optionally plot
	if show:		
		plt.imshow(1-original)
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
	#l = os.listdir(pathChoppedObjects)
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
		#pictPath = os.path.join(pathChoppedObjects, src)
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
			print '		Object = ', src
			print
			print 'Handle right: The center of gravity for the %s is %.1f, %.1f' % \
				(obj, xHandleRight,y)
			print "Handle left: The center of gravity for the %s is %.1f, %.1f" %\
				(obj, xHandleLeft,y)
			print "The direction of the correction is: ", direction
			print
			
		d[obj, maskNormal,  "right"] = xHandleRight,y, direction
		d[obj, maskFlip, "left"] = xHandleLeft, y, direction
	
	
	return d

def cogSaliency():
	
	"""
	Calculates cog of saliency maps
	
	
	"""
	
	src = "./saliency/saliency/saliency maps"
	
	l = []	
	
	for _map in os.listdir(src):
		
		if not "asymm" in _map:
			continue
		print _map
		path = os.path.join(src, _map)

		x, y = centerOfGravity(path, show=False, invert=False, edgeDetect = True, col = False)
		l.append(x)
		print x
	
	mean = np.asarray(l).mean()
	print mean/720

if __name__ == '__main__':
	
	
	# Save the dictionary to a file:
	
	import csv

	#cogSaliency()
#	sys.exit()

	#src = "/home/lotje/Downloads/bijlagen"
	
	#for f in os.listdir(src):
	#	fPath = os.path.join(src, f)
	#	
	#	x,y = centerOfGravity(fPath)
	#	print f
	#	print x
	#	raw_input()
	#sys.exit()

	dict = gravDictMask(show=True, invert=True, edgeDetect=True, \
		printScreen=False)
#	sys.exit()
		
	for mask in ["control", "right", "left"]:
		
		l = []
		for i in dict:
			if i[-1] != "right":
				continue
			if i[1] != "mask_%s" % mask:
				continue
			if i[0] in ["carrot", "ruler", "leveller", "roller"]:
				continue
			#print i[0], dict[i][0]
			l.append(dict[i][0])
		a = np.asarray(l)
		avg = a.mean()/720
		print mask, avg
#	sys.exit()
	w = csv.writer(open("test3.csv", "w"))
	for key, val in dict.items():
		w.writerow([key, val])

	#sys.exit()
	#for key, val in csv.reader(open(exp.get_file("cog_dict.csv"))):
	#	new_key = key.strip('()').split(',')
	
		
	##for i in d:
		#print i, d[i]
		#sys.exit()
	
	
	#def plotPerObject(onlyControl = False):
		
		#d = gravDictMask(show=True, invert=True, edgeDetect=True, \
			#printScreen=False)
			
		## Calculate difference score:
		#lRightX = []
		#lLeftX = []
		#lControlX = []

		#lRightY = []
		#lLeftY = []
		#lControlY = []
		
		#lNames = []
		#l = sorted(d.keys(), key=lambda x: x[0])
		#for i in l:
			
			#if i[2] == 'right':
				#continue

			#if i[1] == 'mask_left':
				#lLeftX.append(d[i][0])
				#lLeftY.append(d[i][1])
			
			#if i[1] == 'mask_right':
				#lRightX.append(d[i][0])
				#lRightY.append(d[i][1])
			
			#if i[1] == 'mask_control':
				#lControlX.append(d[i][0])
				#lControlY.append(d[i][1])
				
				#lNames.append(i[0])

		#aRightX = np.array(lRightX)
		#aLeftX = np.array(lLeftX)
		#aControlX = np.array(lControlX)
		
		#aRightY = np.array(lRightY)
		#aLeftY = np.array(lLeftY)
		#aControlY = np.array(lControlY)
				
		#fig = plt.figure()
	
		##plt.subplot(211)
		#plt.title("x CoG")
		
		#if not onlyControl:
			#plt.plot(aRightX, color='#3465a4', marker = 'o')
			#plt.plot(aLeftX, color='#f57900', marker = 'o')
		#plt.plot(aControlX, color = "#73d216", marker = 'o')
		#plt.axhline(0, linestyle = "--", color = "#555753")
		#plt.axhline(-constants.CoGCorrTooLarge, linestyle = "--", color = "#ef2929")
		#plt.axhline(constants.CoGCorrTooLarge, linestyle = "--", color = "#ef2929")
		
		
		#plt.xticks(range(0, len(lNames)), lNames, rotation = 90)
		#if not onlyControl:
			#plt.legend(["mask_left", "mask_right", "mask_control"])
		#plt.savefig("CoG per object - onlyControl = %s.jpg"%onlyControl)
		#print 'xxx'
		#diff = aRightX - aLeftX

		##plt.subplot(212)
		##plt.title("y CoG")
		
		##plt.plot(aRightY, color='blue')
		##plt.plot(aLeftY, color='red')
		##plt.plot(aControlY, color = "green")
		
		##plt.xticks(range(0, len(lNames)), lNames, rotation = 90)
		##plt.legend(["mask_left", "mask_right", "mask_control"])
		##plt.savefig("CoG_per_object.jpg")
		##diff = aRightY - aLeftY
		
		
		
	#plotPerObject(onlyControl = False)
	#plotPerObject(onlyControl = True)

	