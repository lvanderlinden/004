#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: ovpEffects.py

"""
DESCRIPTION:
Determines OVP effects as a function of landing position!
Raw vs corrected landing positions are used.

TODO:
- cf P&N -> heatmaps with both coordinates?
- bin?
"""

# Import Python modules:
import numpy as np
import os
import sys
from matplotlib import pyplot as plt

# Import own modules:
from exparser.DataMatrix import DataMatrix
from exparser.PivotMatrix import PivotMatrix
import getDM

# Get dm:

def ovp(dm, rt = "rtFromLanding", ws = True, nRows = 1, nCols = 8, nBin = 5, \
	binVar = "endX1Norm", binVar2 = None, figSize = (15,4), onlyControl = True):
	
	"""
	Plots OVP effects as a function of binned initial landing position.
	
	Arguments:
	dm			--- data matrix
	rt			--- variable for RT
	ws 			--- Vincentize or not.
	binVar		--- variable for first row of OVP plots
	binVar2		--- variable for second row of OVP plots (optional)
	onlyControl	--- exclude contrast manipulation. Default = True
	
	"""
	
	# If wanted, exclude the contrast manipulation:
	if onlyControl:
		dm = dm.select("mask_side == 'control'")
	
	# Determine whether or not to first split data per participant
	# (i.e. to make within-subjects bins):
	if ws:
		keys = ['file']
	else:
		keys = None

	# Determine exp:
	exp = dm["exp"][0]
	

	# Add factors containing bins:
	binnedVar = "binned_%s"%binVar
	dm = dm.addField(binnedVar)
	dm = dm.calcPerc(binVar, binnedVar,keys = keys, nBin = nBin)
	
	factorList = [binnedVar]
	
	if binVar2 != None:
		binnedVar2 = "binned_%s" % binVar2
		dm = dm.addField(binnedVar2)
		dm = dm.calcPerc(binVar2, binnedVar2, keys = keys, nBin = nBin)
		factorList.append(binnedVar2)
	
	# Create figure:
	fig = plt.figure(figsize = figSize)
	plt.subplots_adjust(wspace = .5)
	figName = "%s: OVP effects as a function of binned %s - WS = %s" % (exp, factorList, ws)
	plt.suptitle(figName)

	plotCount = 0

	# Define keys:
	subjectID = ["file"]
	dvList = [rt, "durationFix1", "refixProb", "saccCount", "gazeDur", "durationFix2", \
		"endX2Norm", "saccLat1"]
	
	for factors in factorList:
		for dv in dvList:

			plotCount +=1
			
			# Exclude trials on which the dv does not exist:
			_dm = dm.select("%s != ''"%dv)
			
			plt.subplot(nRows, nCols, plotCount)
			plt.title(dv)
			pm = PivotMatrix(_dm, factors, subjectID, dv, colsWithin = True)
			pm.barPlot(fig = fig)
			
			if dv == 'endX2Norm':
				plt.axhline(0, linestyle = '--', color = 'gray')
				
			# Determine ylim's:
			if exp == "004A":
				if dv == "rtFromLanding":
					plt.ylim(500,550)
				if dv == "durationFix1":
					plt.ylim(260, 300)
				if dv == "durationFix2":
					plt.ylim(315, 355)
				if dv == "refixProb":
					plt.ylim(0.58, 0.72)
				if dv == "saccCount":
					plt.ylim(1.75, 1.94)
				if dv == "endX2Norm":
					plt.ylim(-.2, .2)
				if dv == "gazeDur":
					plt.ylim(500, 600)
				if dv == "saccLat1":
					plt.ylim(150, 200)
			
			if exp == "004B":
				
				if dv == "rtFromLanding":
					plt.ylim(400,500)
				if dv == "durationFix1":
					plt.ylim(260, 300)
				if dv == "durationFix2":
					plt.ylim(270, 300)
				if dv == "refixProb":
					plt.ylim(0.4, 0.65)
				if dv == "saccCount":
					plt.ylim(1.6, 2.)
				if dv == "endX2Norm":
					plt.ylim(-.2, .2)
				if dv == "gazeDur":
					plt.ylim(450, 510)
				if dv == "saccLat1":
					plt.ylim(150, 250)
			
			
			#plt.ylabel(dv)
			plt.xticks([])

	plt.savefig("%s RT = %s nBin = %s.png"%(figName,rt, nBin))

def ovpOtherFactor(dm, factor, rt = 'rtFromLanding',\
		nRows = 2, nCols = 4, nBin = 5, ws = True):
	
	"""
	"""
	
	# Determine whether or not to first split data per participant
	# (i.e. to make within-subjects bins):
	if ws:
		keys = ['file', factor]
	else:
		keys = None

	# Determine exp:
	exp = dm["exp"][0]
	
	# Add factors containing bins:
	dm = dm.addField("binned_endX1")
	dm = dm.calcPerc("endX1Norm", "binned_endX1", \
		keys = keys, nBin = nBin)
	
	if exp == "004A":
		dm = dm.addField("binned_endX1Corr")
		dm = dm.calcPerc("endX1CorrNorm", "binned_endX1Corr", \
			keys = keys, nBin = nBin)

	
	
	fig = plt.figure()
	plt.subplots_adjust(wspace = .3, hspace = .4)
	
	figName = "%s: OVP effects as a function of binned landing positions and %s - WS = %s" \
		% (exp, factor, ws)
	plt.suptitle(figName)

	plotCount = 0

	subjectID = ["file"]
	
	if exp == "004A":
		factorList = [[factor,"binned_endX1"], [factor,"binned_endX1Corr"]]
	else:
		factorList = [[factor,"binned_endX1"]]
		
	for factors in factorList:
		for dv in [rt, "durationFix1", "refixProb", "saccCount"]:
			
			plotCount +=1
		
			_dm = dm.select("%s != ''"%dv)
			
			plt.subplot(nRows, nCols, plotCount)
			plt.title(dv)
			pm = PivotMatrix(_dm, factors, subjectID, dv, colsWithin = True)
			pm.linePlot(fig = fig)

	plt.savefig("%s.png"%figName)
	
def ovpSingleFix(dm, counter = 'fixCount', \
		rt = 'rtFromLanding', ws = True, nRows = 2, nCols = 4, nBin = 4):
	
	"""
	Plots OVP effects (only the ones that are suitable) for single-fixation
	cases only
	"""
	
	# Select only single fixations:
	dm = dm.select('%s == 1' % counter)
	
	# Determine exp:
	exp = dm['exp'][0]
	
	
	if ws:
		keys = ['file']
	else:
		keys = None

	# Add factors containing bins:
	dm = dm.addField("binned_endX1")
	dm = dm.calcPerc("endX1Norm", "binned_endX1", \
		keys = keys, nBin = nBin)
	if exp == "004A":
		dm = dm.addField("binned_endX1Corr")
		dm = dm.calcPerc("endX1CorrNorm", "binned_endX1Corr", \
			keys = keys, nBin = nBin)
	
	
	# Create figure:
	fig = plt.figure()
	#fig = plt.figure(figsize = (10,5))
	plt.subplots_adjust(wspace = .4, hspace = 0)
	figName = "%s: OVP effects for single fixations only - counter = %s - WS = %s" % (exp, counter, ws)
	plt.suptitle(figName)

	plotCount = 0

	# Define keys:
	factors = ["binned_endX1"]
	subjectID = ["file"]
	dvList = [rt, "durationFix1", "gazeDur", "saccLat1"]
	
	if exp == "004A":
		factorList = ["binned_endX1", "binned_endX1Corr"]
	else:
		factorList = ["binned_endX1"]
		
	for factors in factorList:
		for dv in dvList:
			
			plotCount +=1
			
			# Exclude trials on which the dv does not exist:
			_dm = dm.select("%s != ''"%dv)
			
			plt.subplot(nRows, nCols, plotCount)
			#if factors == factorList[0]:
				#plt.title(dv)
			pm = PivotMatrix(_dm, factors, subjectID, dv, colsWithin = True)
			pm.plot(nLvl1 = 1, fig = fig)
			
			if dv == 'endX2Norm':
				plt.axhline(0, linestyle = '--', color = 'gray')
				
			if factors == factorList[0]:
				plt.xticks([])

	plt.savefig("%s RT = %s.png"%(figName,rt))

def ovpUnsigned(dm, rt = "rtFromLanding", ws = True, nRows = 2, nCols = 8, \
		nBin = 5, saccNr = "1"):
	
	"""
	OVP effect for unsigned saccades.
	
	Original normalised landing positions are normalised across
	handle orientations such that -.5 indicates completely
	away from the handle, and .5 indicates at the extreme
	of the handle.
	
	To achieve this, the sign of the original end x positions
	for the handle = left trials are reversed.
	"""

	# Create new column header:
	dm = dm.addField("endX%sUnsigned"%saccNr)
	dm = dm.addField("endX%sUnsignedCorr"%saccNr)
	
	# Only on-object saccades:
	dm = dm.select('endX%sNorm < .5'%saccNr)
	dm = dm.select('endX%sNorm > -.5'%saccNr)
	
	# Fill the new variable with original landing positions:
	dm["endX%sUnsigned"%saccNr] = dm["endX%sNorm"%saccNr]
	dm["endX%sUnsignedCorr"%saccNr] = dm["endX%sCorrNorm"%saccNr]
	
	# For the left-handle trials, reverse the sign, such that
	# minus always indicates away from the handle:
	dm["endX%sUnsigned"%saccNr][np.where(dm["handle_side"] == 'left')]= dm["endX%sNorm"%saccNr]*-1
	
	# TODO: check whether this is correct:
	dm["endX%sUnsignedCorr"%saccNr][np.where(dm["handle_side"] == 'left')]= dm["endX%sCorrNorm"%saccNr]*-1
	

	ovp(dm, binVar = "endX%sUnsigned" %saccNr, nBin = nBin, nRows = nRows, \
		nCols = nCols, rt = rt, binVar2 = "endX%sUnsignedCorr"%saccNr, ws = ws)
##	plt.show()
	
	
	



if __name__ == "__main__":
	
	
	for nBin in (3, 5):
		for exp in ["004A", "004B"]:
			
			if exp == "004A":
				nRows = 2
				binVar2 = "endX1CorrNorm"
				#figSize = (15,8)
			if exp == "004B":
				nRows = 1
				binVar2 = None
				#figsize = (15,4)
			
			# Get dm:
			dm = getDM.getDM(exp, driftCorr = True)
			
			# Remove trials on which the first saccade did not land on the object
			# (because the normalised on-object landing positions are used
			# for binning):
			dm = dm.select('endX1Norm < .5')
			dm = dm.select('endX1Norm > -.5')
			
			# OVP effects on normalised landing positions:
			ovp(dm, ws = True, nRows = nRows, binVar2 = binVar2, nBin = nBin)
			
			# OVP effects on landing positions normalised across orientation:
			#ovpUnsigned(dm, nBin = nBin, ws = False)
		
		
		#for factor in ['mask_side', 'visual_field', 'response_hand','comp']:
			
			#if factor != 'comp':
				#continue
			
			#ovpOtherFactor(dm, factor, ws = True)
		#ovpSingleFix(dm)
	