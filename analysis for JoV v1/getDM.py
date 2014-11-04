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

NOTE:
Eye movements outside of the object are still included. These have to be 
excluded separately for every variable of interest (e.g. endX1Norm)

CHANGELOG:
01-07-2013: 
	- rtFromLanding is no longer determined here but during parsing.
	
05-07-2013:
	- Made script applicable for both 004A and 004B. The main differences are:
		- for 004B no gaze-contingent fix checks were carried out (and so the 
			selection criteria for that are not necessary)
	- Dash and Sebastiaan have to be excluded
	
22-01-2014:
No --select in sys.argv anymore. It was too dangerous and led to too many 
mistakes.
"""

# Import Python modules:
import numpy as np
import os
import sys

# Import own modules:
from exparser.DataMatrix import DataMatrix
from exparser.PivotMatrix import PivotMatrix
from exparser.CsvReader import CsvReader
import ascParser
import constants


def getDM(exp, noFiltering=False, driftCorr = True, excludeErrors = True, \
		saccTooFast = None, 
		saccTooSlow = None,\
		rtTooFast = None, rtTooSlow = None, rtVar = 'rtFromStim', \
		exclFailedChecks = True, \
		fixCheck1TooLong = 1000, fixCheck2TooLong = 1000, cutoffHeavy = 0, \
		onlyControl = True, excludeFillers = True):
	
	"""
	Applies several exclusion criteria to obtain a filtered dm.
	
	Arguments:
	dm					--- data matrix
	exp 				--- {"004A", "004B"}, string indicating whether first or second
							experiment is analysed
	
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
	cutoffHeavy			--- minimum deviation necessary to indicate one side of the object
							as heavier. In px. Default = 8.
	onlyControl			--- indicates whether only trials in which manipulation was not 
							manipulated, should be included. Default = True.
	excludeFillers		--- Default = True.
	"""


	if driftCorr:
		fName = "selected_dm_%s_WITH_drift_corr_onlyControl_%s.csv" % (exp, onlyControl)
	else:
		fName = "selected_dm_%s_NO_drift_corr_onlyControl_%s.csv" % (exp, onlyControl)
	
	if exp == "004C":

		
		data = "./dm_004C_simulation.csv"
		
		a = np.genfromtxt(data, dtype=None, delimiter=",")
		dm = DataMatrix(a)
		
		# Add some important column headers:
		dm = dm.addField("file", dtype = str)
		dm = dm.addField("accuracy")
		dm = dm.addField("contrast_side", dtype = str)

		dm["file"] = "simulation"
		dm["accuracy"] = 1

		dm["contrast_side"] = "test"
		dm["contrast_side"][np.where(dm["mask_side"] == "right")] = "_left"
		dm["contrast_side"][np.where(dm["mask_side"] == "control")] = "control"
		dm["contrast_side"][np.where(dm["mask_side"] == "left")] = "right"
		
		
		
	else:

		dm = ascParser.parseAsc(exp = exp, driftCorr = driftCorr)
	
	if noFiltering:
		
		return dm
	
	# Start by applying some general selections (such that 
	# the reported exclusion percentages will not differ depending
	# on when you execute those):

	# Exclude practice trials:
	dm = dm.select("rep != 'practice'")
	
	# For the second experiment, exclude Dash and Sebastiaan:
	if exp == "004B":
	
		# Exclude Sebastiaan:
		dm = dm.select('file != "00401.asc"')
		# Exclude Dash because he's left handed:
		dm = dm.select('file != "00402.asc"')
	
	if onlyControl:
		dm = dm.select("mask_side == 'control'")
	
	if excludeFillers:
		dm = dm.select("symm == 'asymm'")

	if excludeErrors:
		dm = dm.select('accuracy == 1')
		
	# 'Real' selections:
	
	# During parsing, tirals on which the variable 'response' did not contain
	# an int were given the value -1. Otherwise the dm will make all the 
	# 'response' values strings. Therefore, start by excluding those eventual
	# -1's:
	dm = dm.select("response != -1")


	# Remove all trials on which saccLat1 doesn't have a value:
	dm = dm.select("saccLat1 != ''")

	# Negative initial saccade latencies should not happen:
	dm = dm.select('saccLat1 > 0.')

	# Add column header indicating whether drift correction was used:
	dm = dm.addField("driftCorr", dtype = str)
	dm["driftCorr"] = driftCorr
	
	# Add a column header indicating which experiment is analysed:
	dm = dm.addField("exp", dtype = str)
	dm["exp"] = exp
		
	# Add variable indicating whether CoG is to the left or to the
	# right:
	# For objects with handle right, and without mask applied: 
	# - negative xCoG means: heavier on the left
	# - pos means: heavier on the right
	dm = dm.addField('heavySide', dtype = str)
	dm["heavySide"] = 'control'
	dm["heavySide"][np.where(dm["xCoG"] >= cutoffHeavy)] = 'right__'
	dm["heavySide"][np.where(dm["xCoG"] <= -cutoffHeavy)] = 'left__'


	# Some stuff we can't do for the simulation, because those columns don't 
	# exist:
	if exp != "004C":
		# Add variable indicating experimental half (first or second):
		dm = dm.addField("half", dtype = str)
		dm["half"] = "first"
		dm["half"][np.where(dm["block_count"] >= 3)] = "second"
		
	if saccTooFast != None:
		dm = dm.select('saccLat1 > %s'%saccTooFast)
	
	if saccTooSlow != None:
		dm = dm.select('saccLat1 < %s'%saccTooSlow)

	if rtTooFast != None:
		dm = dm.select('%s > %s'%(rtVar,rtTLooFast))
	
	if rtTooSlow != None:
		dm = dm.select('%s < %s'%(rtVar,rtTooSlow))
	
	# Filter on screen coordinates:
	# Y:
	if exp != "004C":
		dm = dm.select("endYRaw1 < %s" % constants.screenH)
		dm = dm.select("endYRaw1 > 0")
		# X:
		dm = dm.select("endXRaw1 < %s" % constants.screenW)
		dm = dm.select("endXRaw1 > 0")
		
		# Re-code initial y coordinates such that we can use one cutoff
		# for both upwards and downwards saccade to see whether they were in
		# the right direction (i.e. > center coordinate):
		dm = dm.addField("sacc_dir")
		dm["sacc_dir"] = dm["endYRaw1"]
		dm["sacc_dir"][dm.where("visual_field == 'upper'")] = \
			dm["endYRaw1"][dm.where("visual_field == 'upper'")]+\
			constants.yCen
			
		# Select saccades that were in the right vertical direction:
		dm.select("sacc_dir > %s" % str(constants.yCen))
	
	# Exclude trials on which a fixation check failed or took too long:
	if exp == "004A":
		
		if exclFailedChecks:
			# Note why those will probably never lead to exclusions anymore: 
			# in those cases durCheck1 or durCheck2 would have the value -1000 (because they 
			# couldnt be calculated) and therefore are already excluded above.
			dm = dm.select('checkFixDotFailed == "False"')
			dm = dm.select('checkObjectFailed == "False"')

		if fixCheck1TooLong != None:
			dm = dm.select('durCheck1 < %s' % fixCheck1TooLong)
		if fixCheck2TooLong != None:
			dm = dm.select('durCheck2 < %s' % fixCheck2TooLong)

	if exp != "004C":
		# Negative new RT's should not happen:
		dm = dm.select('rtFromStim > 0')

	dm.save(fName)
	
	return dm

if __name__ == "__main__":
	
	for exp in ["004A", "004B", "004C"]:
		
		dm = getDM(exp,onlyControl = True)
		dm = getDM(exp,onlyControl = False)
	