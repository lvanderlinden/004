"""
DESCRIPTION:
Only for 004A:
Prepare DV relative to absolute center (instead of relative to CoG, as in
addCoord.py).
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
def addCoord2(dm, plot = False):
	
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
		
		dm = dm.addField("xNormAbsCenter%s" % sacc, default = -1000)
		dm = dm.addField("yNormAbsCenter%s" % sacc, default = -1000)

	count = 0
	# Walk through trials:
	for i in dm.range():
		
		# Get file info:
		aRot = dm["realAngle"][i]
		xStim = 0
		yStim = dm["yStim"][i]
		#xCog = dm["xCog"][i]
		vf = dm["visual_field"][i]
		flipCond = dm["flip"][i]
		
		stimFile = dm["stimFile"][i]
		wBoxScaled = dm["wBoxScaled"][i]
		hBoxScaled = dm["hBoxScaled"][i]
		
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

			dm["xNormAbsCenter%s" % sacc][i] = xNormOnWidth
			dm["yNormAbsCenter%s" % sacc][i] = yNormOnWidth
			
	return dm