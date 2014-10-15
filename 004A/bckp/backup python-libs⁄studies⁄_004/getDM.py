#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: getDM.py

"""
DESCRIPTION:
Apply selection criteria, add useful variables, etc.

Note that I end up with four types of RT:
- 'response_time' as returned by OpenSesame -> this one is not useful because
	it doesn't take the speed of the fixation checks into account
- 'rtFromStim' is the interval between stimulus onset and response
- 'rtFrom Landing' is the interval between landing on the stimulus and response
- 'rtFromSuccess' is the interval between the timestamp where the fixation 
	check on the object was successful, and the response.
	
TODO: determine cutoff criteria.
"""

# Import Python modules:
import numpy as np
import os
import sys

# Import own modules:
from exparser.DataMatrix import DataMatrix
import constants
import parseAsc


def getDM(driftCorr, excludeErrors = False, saccTooFast = 80, saccTooSlow = None,\
		rtTooFast = None, rtTooSlow = None, rtVar = 'rtFromStim', \
		exclFailedChecks = True, \
		fixCheck1TooLong = 700, fixCheck2TooLong = 450):
	
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
	exclFailedChecks	--- Boolean indicating whether or not to excude trials on
							which one or more fix checks failed. Default = False
	fixCheckTooLong1	--- Cutoff for excluding too long fixation checks. Set
							to None to deactivate this filter. Default = 700, 
							based on looking at plt.hist(dm['durCheck1'])
	fixCheckTooLong2	--- Cutoff for excluding too long fixation check on 
							object. Set to None to deactivate. Default = 450,
							based on looking at plt.hist(dm['durCheck2'])
	drifCorr			--- 
	"""

	# Declare constants:
	src = '/home/lotje/python-libs/studies/_004'

	dm = parseAsc.parseAsc(driftCorr = driftCorr)
	
	dm = dm.addField("driftCorr", dtype = str)
	dm["driftCorr"] = driftCorr

	# Exclude practice trials:
	dm = dm.select("rep != 'practice'")
	
	# During parsing, tirals on which the variable 'response' did not contain
	# an int were given the value -1. Otherwise the dm will make all the 
	# 'response' values strings. Therefore, start by excluding those eventual
	# -1's:
	dm = dm.select("response != -1")
	
	# Check whether the dummy variables for the newly-determined variables
	# are all overwritten:
	
	for dummyVar in ('saccLat', 'rtFromStim', 'rtFromSuccess', 'xCoG', \
		'yCoG', 'xCoGMask', 'yCoGMask','endX', 'endY', 'endXCorr', 'endXCorrMask',
		'durCheck1', 'durCheck2'):
		dm = dm.select('%s != %s' %(dummyVar,constants.parseDummyVar))
	
	# Saccade latencies of 0 (or -1) should not happen:
	# If no saccade is detected during a trial, 'saccLat' is changed from -1000
	# to -1 during parsing:
	dm = dm.select('saccLat > 0')
	
	# Negative new RT's should not happen:
	dm = dm.select('rtFromStim > 0')
	
	# Add values indicating whether the eyes landed towards the handle (positive
	# values) or towards the other side of the object (negative values):
	# Also, make sure all values are eventually converted to visual degrees:
	
	# Without any correction:
	dm = dm.addField("pxTowardsHandle")
	dm = dm.addField("degrTowardsHandle")
	indicesRight = np.where(dm["handle_side"] == 'right')
	indicesLeft = np.where(dm["handle_side"] == 'left')
	dm["pxTowardsHandle"][indicesRight] = (dm["endX"][indicesRight])
	dm["pxTowardsHandle"][indicesLeft] = dm["endX"][indicesRight]*-1
	dm["degrTowardsHandle"] = dm["pxTowardsHandle"]/constants.ratioPxDegr

	# With CoG correction based on the original bitmap (without mask):
	dm = dm.addField("pxTowardsHandleCorr")
	dm = dm.addField("degrTowardsHandleCorr")
	indicesRight = np.where(dm["handle_side"] == 'right')
	indicesLeft = np.where(dm["handle_side"] == 'left')
	dm["pxTowardsHandleCorr"][indicesRight] = (dm["endXCorr"][indicesRight])
	dm["pxTowardsHandleCorr"][indicesLeft] = dm["endXCorr"][indicesRight]*-1
	dm["degrTowardsHandleCorr"] = dm["pxTowardsHandleCorr"]/constants.ratioPxDegr

	# Wit CoG correction with taking mask into account::
	dm = dm.addField("pxTowardsHandleCorrMask")
	dm = dm.addField("degrTowardsHandleCorrMask")
	indicesRight = np.where(dm["handle_side"] == 'right')
	indicesLeft = np.where(dm["handle_side"] == 'left')
	dm["pxTowardsHandleCorrMask"][indicesRight] = \
		(dm["endXCorrMask"][indicesRight])
	dm["pxTowardsHandleCorrMask"][indicesLeft] = \
		dm["endXCorrMask"][indicesRight]*-1
	dm["degrTowardsHandleCorrMask"] = \
		dm["pxTowardsHandleCorrMask"]/constants.ratioPxDegr

	# Convert landing positions to visual degrees:
	dm = dm.addField("endXDegr")
	dm = dm.addField("endXCorrDegr")
	dm = dm.addField("endXCorrMaskDegr")
	dm["endXDegr"] = dm["endX"]/constants.ratioPxDegr
	dm["endXCorrDegr"] = dm["endXCorr"]/constants.ratioPxDegr
	dm["endXCorrMaskDegr"] = dm["endXCorrMask"]/constants.ratioPxDegr

	# Convert starting position to visual degrees:
	dm = dm.addField("startXDegr")
	dm["startXDegr"] = dm["startX"]/constants.ratioPxDegr
	
	dm = dm.addField("rtFromLanding")
	dm['rtFromLanding'] = dm['rtFromStim']-dm['saccLat']
	
	if saccTooFast != None:
		dm = dm.select('saccLat > %s'%saccTooFast)
	if saccTooSlow != None:
		dm = dm.select('saccLat < %s'%saccTooSlow)

	if rtTooFast != None:
		dm = dm.select('%s > %s'%(rtVar,rtTooFast))
	
	if rtTooSlow != None:
		dm = dm.select('%s < %s'%(rtVar,rtTooSlow))
	
	# Exclude trials on which a fixation check failed or took too long:
	if exclFailedChecks:
		# Note why those will probably never lead to exclusions anymore: in those
		# cases durCheck1 or durCheck2 would have the value -1000 (because they 
		# couldnt be calculated) and therefore are already excluded above.
		dm = dm.select('checkFixDotFailed == "False"')
		dm = dm.select('checkObjectFailed == "False"')

	if fixCheck1TooLong != None:
		dm = dm.select('durCheck1 < %s' % fixCheck1TooLong)
	if fixCheck2TooLong != None:
		dm = dm.select('durCheck2 < %s' % fixCheck2TooLong)
	
	if excludeErrors:
		dm = dm.select('accuracy == 1')
	
	dm.save(os.path.join(src,"data - drift correction = %s - selected.csv"%driftCorr))

		
	return dm

if __name__ == "__main__":
	
	getDM(driftCorr = True)
	getDM()
