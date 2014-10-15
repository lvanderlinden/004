#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: getDM.py

"""
DESCRIPTION:

Apply selection criteria to data from 004B.
The only difference with 004A is that no trials on which 
the fixation checks didn't work, have to be excluded.

Apply selection criteria, add useful variables, etc.

Note that I end up with four types of RT:
- 'response_time' as returned by OpenSesame -> this one is not useful because
	it doesn't take the speed of the fixation checks into account
- 'rtFromStim' is the interval between stimulus onset and response
- 'rtFrom Landing' is the interval between landing on the stimulus and response
- 'rtFromSuccess' is the interval between the timestamp where the fixation 
	check on the object was successful, and the response.
	
TODO: determine cutoff criteria.

NOTE:
Eye movements outside of the object are still included. These have to be 
excluded separately for every variable of interest (e.g. endX1Norm)

CHANGELOG:
01-07-2013: 
	- rtFromLanding is no longer determined here but during parsing.
"""

# Import Python modules:
import numpy as np
import os
import sys

# Import own modules:
from exparser.DataMatrix import DataMatrix
from exparser.PivotMatrix import PivotMatrix
from exparser.CsvReader import CsvReader

import studies._004.constants
import ascParser004B


def getDM(driftCorr, excludeErrors = False, saccTooFast = 80, saccTooSlow = None,\
		rtTooFast = None, rtTooSlow = None, rtVar = 'rtFromStim'):
	
	"""
	Applies several exclusion criteria to obtain a filtered dm.
	
	Arguments:
	dm		--- data matrix
	
	Keyword arguments:
	excludeErrors		--- Boolean indicating whether error trials should be
							excluded. Default = False.
	saccTooFast			--- Cutoff for exclusion of too-fast saccades. Set to None
							to deactivate this filter. Default = 80.
	saccTooSlow 			--- Cutoff for exclusion of too-slow saccades. Set to None
							to deactivate this filter.
	rtTooFast			--- Cutoff for exclusion of too-fast RTs. Set to None to
							deactivate this filter.
	rtTooSlow			--- Cutoff for exclusion of too-slow RTs. Set to None to 
							deactivate this filter.
	rtVar				--- rt variable to use for excluding too fast and/or
							too slow response times.
	drifCorr			--- 
	"""

	# Declare constants:
	#src = '/home/lotje/python-libs/studies/_004'

	if driftCorr:
		fName = "selected_dm_WITH_drift_corr.csv"
	else:
		fName = "selected_dm_NO_drift_corr.csv"
	
	if '--shortcut' in sys.argv:
		
		
		a = np.genfromtxt(fName, dtype=None, delimiter=",")
		dm = DataMatrix(a)
		
		#dm = CsvReader(fName, delimiter=',').dataMatrix()

		return dm
		
	dm = ascParser004B.parseAsc(driftCorr = driftCorr)
	
	# Exclude Sebastiaan:
	dm = dm.select('file != "00401.asc"')
	
	# Exclude Dash because he's left handed:
	dm = dm.select('file != "00402.asc"')
	
	
	# Add column header indicating whether drift correction was used:
	dm = dm.addField("driftCorr", dtype = str)
	dm["driftCorr"] = driftCorr
	
	# Make a new variable (instead of 'mask_side') that indicates the
	# highest contrast side:
	dm = dm.addField('contrast_side', dtype = str)
	dm['contrast_side'][np.where(dm['mask_side'] == "right")] = "_left"
	dm['contrast_side'][np.where(dm['mask_side'] == "left")] = "right"
	dm['contrast_side'][np.where(dm['mask_side'] == "control")] = "control"
	
	# Add variable indicating whether CoG is to the left or to the
	# right:
	# For objects with handle right, and without mask applied: 
	# - negative xCoG means: heavier on the left
	# - pos means: heavier on the right
	dm = dm.addField('heavySide', dtype = str)
	dm["heavySide"] = 'left'
	dm["heavySide"][np.where(dm["xCoG"] >= 0)] = 'right'

	# Add variable indicating experimental half (first or second):
	dm = dm.addField("half", dtype = str)
	dm["half"] = "first"
	dm["half"][np.where(dm["block_count"] >= 3)] = "second"

	# Exclude practice trials:
	dm = dm.select("rep != 'practice'")
	
	# During parsing, tirals on which the variable 'response' did not contain
	# an int were given the value -1. Otherwise the dm will make all the 
	# 'response' values strings. Therefore, start by excluding those eventual
	# -1's:
	dm = dm.select("response != -1")

	# Saccade latencies of 0 (or -1) should not happen:
	# If no saccade is detected during a trial, 'saccLat' is changed from -1000
	# to -1 during parsing:
	dm = dm.select('saccLat1 > 0')
	
	# Negative new RT's should not happen:
	dm = dm.select('rtFromStim > 0')
	
	# Add values indicating whether the eyes landed towards the handle (positive
	# values) or towards the other side of the object (negative values):
	# Also, make sure all values are eventually converted to visual degrees:
	
	# If first landing position is empty, skip the trial:
	dm = dm.select("endX1 != ''")
	
	# Without any correction:
	dm = dm.addField("pxTowardsHandle")
	dm = dm.addField("degrTowardsHandle")
	indicesRight = np.where(dm["handle_side"] == 'right')
	indicesLeft = np.where(dm["handle_side"] == 'left')
	dm["pxTowardsHandle"][indicesRight] = (dm["endX1"][indicesRight])
	dm["pxTowardsHandle"][indicesLeft] = dm["endX1"][indicesRight]*-1
	dm["degrTowardsHandle"] = dm["pxTowardsHandle"]/studies._004.constants.ratioPxDegr

	## With CoG correction based on the original bitmap (without mask):
	#dm = dm.addField("pxTowardsHandleCorr")
	#dm = dm.addField("degrTowardsHandleCorr")
	#indicesRight = np.where(dm["handle_side"] == 'right')
	#indicesLeft = np.where(dm["handle_side"] == 'left')
	#dm["pxTowardsHandleCorr"][indicesRight] = (dm["endXCorr"][indicesRight])
	#dm["pxTowardsHandleCorr"][indicesLeft] = dm["endXCorr"][indicesRight]*-1
	#dm["degrTowardsHandleCorr"] = dm["pxTowardsHandleCorr"]/constants.ratioPxDegr

	## Wit CoG correction with taking mask into account::
	#dm = dm.addField("pxTowardsHandleCorrMask")
	#dm = dm.addField("degrTowardsHandleCorrMask")
	#indicesRight = np.where(dm["handle_side"] == 'right')
	#indicesLeft = np.where(dm["handle_side"] == 'left')
	#dm["pxTowardsHandleCorrMask"][indicesRight] = \
		#(dm["endXCorrMask"][indicesRight])
	#dm["pxTowardsHandleCorrMask"][indicesLeft] = \
		#dm["endXCorrMask"][indicesRight]*-1
	#dm["degrTowardsHandleCorrMask"] = \
		#dm["pxTowardsHandleCorrMask"]/constants.ratioPxDegr

	# Convert landing positions to visual degrees:
	dm = dm.addField("endXDegr")
	#dm = dm.addField("endXCorrDegr")
	#dm = dm.addField("endXCorrMaskDegr")
	dm["endXDegr"] = dm["endX1"]/studies._004.constants.ratioPxDegr
	#dm["endXCorrDegr"] = dm["endXCorr"]/constants.ratioPxDegr
	#dm["endXCorrMaskDegr"] = dm["endXCorrMask"]/constants.ratioPxDegr

	# Convert starting position to visual degrees:
	dm = dm.addField("startX1Degr")
	dm["startX1Degr"] = dm["startX1"]/studies._004.constants.ratioPxDegr
	
	#dm = dm.addField("rtFromLanding")
	#dm['rtFromLanding'] = dm['rtFromStim']-dm['saccLandingTime1']
	
	if saccTooFast != None:
		dm = dm.select('saccLat1 > %s'%saccTooFast)
	if saccTooSlow != None:
		dm = dm.select('saccLat1 < %s'%saccTooSlow)

	if rtTooFast != None:
		dm = dm.select('%s > %s'%(rtVar,rtTooFast))
	
	if rtTooSlow != None:
		dm = dm.select('%s < %s'%(rtVar,rtTooSlow))
	
	
	if excludeErrors:
		dm = dm.select('accuracy == 1')
	
	dm.save(fName)
	
	return dm

if __name__ == "__main__":
	
	getDM(driftCorr = True)