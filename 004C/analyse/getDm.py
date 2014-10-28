"""
DESCRIPTION:
Prepare DVs for statistical analyses: LP relative to CoG, normalized for 
object size and orientation
"""


import sys
import os
import numpy as np
from matplotlib import pyplot as plt

import constants
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

debug = False

dstPlot = "debug plots"


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
	for sacc in range(1, int(max(dm["saccCount"])) + 1):
		dm = dm.addField("xRot%s" % sacc, default = -1000)
		dm = dm.addField("yRot%s" % sacc, default = -1000)
		dm = dm.addField("xFlipped%s" % sacc, default = -1000)
		dm = dm.addField("yFlipped%s" % sacc, default = -1000)
		
		dm = dm.addField("xNorm%s" % sacc, default = -1000)
		dm = dm.addField("yNorm%s" % sacc, default = -1000)
		dm = dm.addField("xNormOnCenter%s" % sacc, default = -1000)
		dm = dm.addField("yNormOnCenter%s" % sacc, default = -1000)

	dm = dm.addField("wBoxScaled")
	dm = dm.addField("hBoxScaled")
	dm = dm.addField("xCogScaled")
	dm = dm.addField("xCogScaledDegr")
	dm = dm.addField("stimFile", dtype = str)

	
	count = 0
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
		
		# Scaled cog in degrees:
		xCogScaledDegr = xCogScaled/constants.ratio
		dm["xCogScaledDegr"][i] = xCogScaledDegr
		
		
		# Size bounding box
		wBoxScaled, hBoxScaled = bbox.bbox(stimFile)
		dm["wBoxScaled"][i] = wBoxScaled
		dm["hBoxScaled"][i] = hBoxScaled
		
		# Walk through fixations within trial:
		saccTot = int(dm["saccCount"][i])
		

		for sacc in range(1,saccTot +1):
			
			# Get raw coordinates:
			x = dm["sacc%s_ex" % sacc][i]
			y = dm["sacc%s_ey" % sacc][i]
			
			
			
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
				yNormOnFlip, wBoxScaled, hBoxScaled, yStim)

			# Save new variables:
			dm["xRot%s" % sacc][i] = xRot
			dm["yRot%s" % sacc][i] = yRot
			dm["xNorm%s" % sacc][i] = xNormOnWidth
			dm["yNorm%s" % sacc][i] = yNormOnWidth
			dm["xNormOnCenter%s" % sacc][i] = xNormOnCenter
			dm["yNormOnCenter%s" % sacc][i] = yNormOnCenter
			dm["xFlipped%s" % sacc][i] = xNormOnFlip
			dm["yFlipped%s" % sacc][i] = yNormOnFlip
			
	return dm

@cachedDataMatrix
def addLat(dm):
	
	"""
	Add sacc latency relative to stimulus onset
	
	Arguments:
	dm		--- A datamatrix instance.
	"""
	count = 0
	
	# Add col headers:
	for sacc in range(1, int(max(dm["saccCount"])) + 1):
		dm = dm.addField("saccLat%s" % sacc)
	
	
	# Walk through trials:
	for i in dm.range():
		stimOnset = dm["stim_onset"][i]
		saccTot = int(dm["saccCount"][i])

		for sacc in range(1,saccTot +1):
			
			sSacc= dm["sacc%s_sTime" % sacc][i]
			saccLat = sSacc - stimOnset
			dm["saccLat%s" % sacc][i] = saccLat
	
	return dm		

	