import sys
import os
import numpy as np
from matplotlib import pyplot as plt

import bbox
import rotate
import parse
import flip
import normOnWidth
import centralOrigin
from exparser.DataMatrix import DataMatrix
from exparser.PivotMatrix import PivotMatrix
from exparser.EyelinkAscFolderReader import EyelinkAscFolderReader
from exparser.CsvReader import CsvReader
from exparser.Cache import cachedDataMatrix, cachedArray

"""
Prepare DVs for statistical analyses: LP relative to CoG, normalized for 
object size and orientation

1. Normalize LP's relative to 
2. Flip landing positions as if handle was always on the right side.

3. Normalize objects on width

"""


@cachedDataMatrix
def addCoord(dm, plot = False):
	
	"""
	Adds coordinates to dm
	
	Arguments:
	dm		--- A datamatrix instance.
	
	Keyword arguments:
	plot	--- Boolean indicating whether or not to show some debug plots
	"""
	
	# Add col headers:
	for fix in range(1, max(dm["fixCount"]) + 1):
		dm = dm.addField("xRot%s" % fix, default = -1000)
		dm = dm.addField("yRot%s" % fix, default = -1000)
		dm = dm.addField("xNorm%s" % fix, default = -1000)
		dm = dm.addField("yNorm%s" % fix, default = -1000)

	dm = dm.addField("wBoxScaled")
	dm = dm.addField("hBoxScaled")
	dm = dm.addField("xCogScaled")
	dm = dm.addField("stimFile", dtype = str)
	dm = dm.addField("xNormOnCenter")
	dm = dm.addField("yNormOnCenter")

	# Walk through trials:
	for i in dm.range():
		
		# Get file info:
		aRot = dm["realAngle"][i]
		ecc = dm["ecc"][i]
		xStim = dm["xStim"][i]
		yStim = dm["yStim"][i]
		xCog = dm["xCog"][i]
		vf = dm["visual_field"][i]
		flipCond = dm["flip"][i]
		
		# Log new info:
		# PNG name:
		stimFile = "%s_%s.png" % (dm["stim_type"][i], dm["stim_name"][i])
		dm["stimFile"][i] = stimFile
		
		# Scaled cog:
		xCogScaled = xCog/3
		dm["xCogScaled"][i] = xCogScaled
		
		# Size bounding box
		wBoxScaled, hBoxScaled = bbox.bbox(stimFile)
		dm["wBoxScaled"][i] = wBoxScaled
		dm["hBoxScaled"][i] = hBoxScaled
		
		# Walk through fixations within trial:
		fixTot = int(dm["fixCount"][i])

		for fix in range(1,fixTot +1):
			
			# Get raw coordinates:
			x = dm["fix%s_x" % fix][i]
			y = dm["fix%s_y" % fix][i]
			
			# Normalize such that origin = (0,0):
			xNormOnCenter, yNormOnCenter = centralOrigin.centralOrigin(x, y,plot=plot)
			
			# Rotate as if object was presented at -90 in UVF:
			xRot, yRot= rotate.rotate(xNormOnCenter,yNormOnCenter, \
				aRot,plot=plot)
			
			# Normalize on orientation, as if handle was always to the right.
			# TODO: check!!!
			xNormOnFlip, yNormOnFlip = flip.flip(xRot, \
				yRot,flipCond, plot=plot)
			
			# Normalize on object width:
			xNormOnWidth, yNormOnWidth = normOnWidth.normOnWidth(xNormOnFlip, 
				yNormOnFlip, wBoxScaled, hBoxScaled)

			# Save new variables:
			dm["xRot%s" % fix][i] = xRot
			dm["yRot%s" % fix][i] = yRot
			dm["xNorm%s" % fix][i] = xNormOnWidth
			dm["yNorm%s" % fix][i] = yNormOnWidth
	return dm

@cachedDataMatrix
def addLat(dm):
	
	"""
	Add sacc latency relative to stimulus onset
	
	Arguments:
	dm		--- A datamatrix instance.
	"""
	
	# Add col headers:
	for fix in range(1, int(max(dm["fixCount"])) + 1):
		dm = dm.addField("saccLat%s" % fix)
		
	# Walk through trials:
	for i in dm.range():
		stimOnset = dm["stim_onset"][i]
		fixTot = int(dm["fixCount"][i])

		for fix in range(1,fixTot +1):
			sFix = dm["fix%s_sTime" % fix][i]
			saccLat = sFix - stimOnset
			dm["saccLat%s" % fix][i] = saccLat
			#print dm["saccLat%s" % fix][i]
	#print dm["saccLat1"]
	
	return dm		

	