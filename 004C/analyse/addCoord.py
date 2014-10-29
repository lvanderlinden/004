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

@cachedDataMatrix
def addCoord(dm, plot = False):
	
	"""
	Adds coordinates to dm
	
	Arguments:
	dm		--- A datamatrix instance.
	
	Keyword arguments:
	plot	--- Boolean indicating whether or not to show some debug plots
	"""
	
	
	exp = dm["expId"][0]

	# HACK:
	# Only symmetrical objects:
	if exp != "004C":
		dm = dm.select("symm == 'asymm'")

	# Add col headers:

	# HACK: Only first 5 saccades (otherwise it becomes too slow, and the trials
	# with a lot of fixations are probably non-representative, e.g. just after
	# a break, anyway)

	#for sacc in range(1, int(max(dm["saccCount"])) + 1):
	for sacc in range(1, 6):
		
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
	
	if exp == "004C":
		dm = dm.addField("xCogScaled")
	dm = dm.addField("xCogScaledDegr")
	dm = dm.addField("stimFile", dtype = str)

	
	count = 0
	# Walk through trials:
	for i in dm.range():
		
		# Get file info:
		aRot = dm["realAngle"][i]
		xStim = dm["xStim"][i]
		yStim = dm["yStim"][i]
		#xCog = dm["xCog"][i]
		vf = dm["visual_field"][i]
		flipCond = dm["flip"][i]
		
		# Log new info:
		# PNG name:
		# TODO: is this okay for 004A and 004B too??
		stimFile = "%s_%s.png" % (dm["stim_type"][i], dm["stim_name"][i])
		dm["stimFile"][i] = stimFile
		
		# Scaled cog:
		if exp == "004C":
			xCog = dm["xCog"][i]
			xCogScaled = xCog/3
			dm["xCogScaled"][i] = xCogScaled
		
		# Scaled cog in degrees:
		xCogScaledDegr = dm["xCogScaled"][i]/constants.ratio
		dm["xCogScaledDegr"][i] = xCogScaledDegr
		
		# Size bounding box
		wBoxScaled, hBoxScaled = bbox.bbox(stimFile)
		
		dm["wBoxScaled"][i] = wBoxScaled
		dm["hBoxScaled"][i] = hBoxScaled
		
		# Walk through fixations within trial:
		saccTot = int(dm["saccCount"][i])
		for sacc in range(1,saccTot +1):
			
			print sacc
			
			# HACK: Are there really trials containing more than 10 saccades?
			# If so, do we want these saccades anyway?
			if sacc > 5:
				continue
			
			# Get raw coordinates:
			x = dm["sacc%s_ex" % sacc][i]
			y = dm["sacc%s_ey" % sacc][i]
			
			# Normalize such that origin = (0,0):
			xNormOnCenter, yNormOnCenter = centralOrigin.centralOrigin(x, y,plot=plot)
			
			# Rotate as if object was presented at -90 in UVF:
			xRot, yRot= rotate.rotate(xNormOnCenter,yNormOnCenter, \
				aRot,plot=plot)
			
			# Normalize on orientation, as if handle was always to the right.
			xNormOnFlip, yNormOnFlip = flip.flip(xRot, \
				yRot,flipCond, vf, plot=plot)
			
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