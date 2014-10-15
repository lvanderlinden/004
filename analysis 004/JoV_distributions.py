#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: fig2.py
"""
Created on Wed Jan 22 13:16:37 2014

@author: lotje

DESCRIPTION
Distribution of landing positions
- per saccade
- per reference point
- per experiment

TODO: 
Normalise per factor that might influence distributions, that we're not
interested in:
- Object


"""

# Import Python modules:
import numpy as np
import os
import sys
from matplotlib import pyplot as plt

# Import own modules:
from exparser.TangoPalette import *
from exparser.CsvReader import CsvReader
import getDM
import onObject

# Set font.
# For guidelines, see:
# http://www.journalofvision.org/site/misc/peer_review.xhtml#style
plt.rc("font", family="arial")
plt.rc("font", size=10)

# Some constant vars:
#dst = "/home/lotje/Documents/PhD Marseille/Studies/004 - Single-object experiment - Handle-orientation #effect/manuscript/Versions/5th draft/Figures JoV/Distributions"

dst = "/home/lotje/Documents/PhD Marseille/Studies/004 - Single-object experiment - Handle-orientation effect/manuscript/sources/JoV/Distributions"


def normY(a, flatten=False):
	
	# Normalise:
	a = abs(a)
	
	_min = float(np.min(a))
	_max = float(np.max(a))
	
	y = (a-_min)/(_max-_min)
	
	return y



def distr(main_dm, dv, saccVar, trim=True, binSize = 50, \
	col = blue[1], norm=True):
	
	"""
	Plots distribution per saccade (seperate subplots) per reference point
	(seperate lines) per experiment (seperate main plots)
	
	Arguments:
	exp
	
	Keyword arguments:
	trim
	blinkRemov
	withMarker
	"""
	
	dm = main_dm
	
	if "1" in saccVar:
		sacc = "1"
	elif "2" in saccVar:
		sacc = "2"
	if "ToHandle" in dv:
		withinizeFactor = "handle_side"
	elif "ToContrast" in dv:
		withinizeFactor="contrast_side"
	
	# landing position should not be "":
	dm = onObject.onObject(dm, sacc)	

	# Exclude outliers sacc lat:
	dm = dm.selectByStdDev(keys=["file"], dv = saccVar)

	# Remove outliers landing position:
	dm= dm.removeField("__dummyCond__")
	dm= dm.removeField("__stdOutlier__")
	dm = dm.selectByStdDev(keys=["file"], dv =dv)

	# Divide sacc latency into equal bins:
	# NORMALIZING OF SACC LAT per pp occurs here!
	dm = dm.addField("binnedSaccLat")
	dm= dm.calcPerc(saccVar, "binnedSaccLat",keys = ["file"],\
		nBin = 3)
		
	colList = [orange[1], green[1], blue[1]]
	
	nBins = 15

	for _bin in dm.unique("binnedSaccLat"):

		_dm = dm.select("binnedSaccLat == %s" % _bin)
		print norm
		if norm:
			# Normalize landing positions:
			_dm= _dm.addField("newLanding", dtype = float)
			_dm= _dm.withinize(dv, "newLanding", \
					[withinizeFactor], whiten=False)
			_dv = "newLanding"
		else:
			_dv = dv
			
			
		samp = _dm[_dv]
		#samp = _dm["newLanding"]
		y, edges = np.histogram(samp, bins = nBins)
		y = normY(y)
				
		x = .5*edges[1:] + .5*edges[:-1]
		col = colList.pop()
#		plt.plot(x, y, 'o-', color = col, markeredgecolor = col,\
#			markerfacecolor = "white", markeredgewidth = 1)
		plt.plot(x, y, marker='.', color = col, markeredgecolor = col,\
			markerfacecolor = col, markeredgewidth = 1)

		
	plt.ylim([0,1.1])
	plt.xlim([-.7, .7])
	
	
def plotPerExp(exp, direction, norm=True):
	
	
	"""
	"""
	
	print "exp = ", exp
	print "direction = ", direction
	
	legend = True
	
	# Get dm:
	if direction == "ToHandle":
		src = 'selected_dm_%s_WITH_drift_corr_onlyControl_True.csv' % exp
		#dm = getDM.getDM(exp, onlyControl=True)
	elif direction == "ToContrast":
		src = 'selected_dm_%s_WITH_drift_corr_onlyControl_False.csv' % exp
		#dm = getDM.getDM(exp, onlyControl=False)
#		
	main_dm = CsvReader(src).dataMatrix()

	
	
	if direction == "ToContrast":
		main_dm = main_dm.select("contrast_side != 'control'")

	nCols = 2
	
	if exp == "004B":
		nRows = 1
		fig = plt.figure(figsize = (8, 3))
		plt.subplots_adjust(wspace=0, hspace = 0.2, left = .2, bottom = .15)
		#plt.suptitle("Experiment 2", s)
		
		lTitles = ["a) Saccade 1 relative to CoG", \
			"b) Saccade 2 relative to CoG"]
		lTitles.reverse()
		
	if exp == "004A":
		nRows = 2
		fig = plt.figure(figsize = (8,6))
		plt.subplots_adjust(wspace=0, hspace = 0.2,\
			left = .2, bottom = .15)
		#plt.suptitle("Experiment 1")

		lTitles = ["a) Saccade 1 relative to absolute center", \
			"b) Saccade 2 relative to absolute center", 
			"c) Saccade 1 relative to CoG", "d) Saccade 2 relative to CoG"]
		lTitles.reverse()


	nPlot = 0
	
	if exp == "004A":
		varList = ["absolute center", "CoG"]
	elif exp == "004B":
		varList = ["absolute center"]
	
	for dvType in varList:

		for sacc in ["1", "2"]:

			if dvType == "absolute center":
				dv = "endX%sNorm%s" % (sacc, direction)
			elif dvType == "CoG":
				dv = "endX%sCorrNorm%s" % (sacc, direction)
			
			# Plot distr per saccade bin:
			nPlot +=1
			ax = plt.subplot(nRows, nCols, nPlot)
			plt.title(lTitles.pop(), size = 10)
			distr(main_dm, dv, "saccLat%s" % sacc, norm=norm)
			
			if legend:
				plt.legend(["Fast", "Medium", "Slow"],loc='best')
				legend=False

			if sacc == "2":
				ax.yaxis.set_ticklabels([])
			elif sacc == "1":
				plt.ylabel("Normalized frequency")
			if exp == "004A":
				if dvType == "absolute center":
					ax.xaxis.set_ticklabels([])
				elif dvType == "CoG":
					plt.xlabel("Normalized landing position")
			if exp == "004B":
				plt.xlabel("Normalized landing position")
			
				
			plt.axvline(0, linestyle = "--", color = gray[3])
	
	figName = "Distr_%s_%s_norm_%s.svg" % \
		(exp, direction, norm)
	plt.savefig(os.path.join(dst,figName))
	
	print
	print
	print "Done!"
	print figName, "is saved"
	print
	print
		
if __name__ == "__main__":

	for direction in ["ToHandle", "ToContrast"]:
		for exp in ["004A", "004B"]:
			plotPerExp(exp, direction,norm=False)
