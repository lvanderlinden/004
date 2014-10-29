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
plt.rc("font", size=7)

# Some constant vars:
dst = "/home/lotje/Studies/004 - Single-object experiment - Handle-orientation effect/manuscript/Versions/5th draft/Figures JoV"


def normY(a, flatten=False):
	
	# Normalise:
	a = abs(a)
	
	if flatten:
		k = 3
		maxVal = a.mean() + a.std() * k
		i = np.where(a > maxVal)
		a[i] = maxVal
	
	_min = float(np.min(a))
	_max = float(np.max(a))
	
	y = (a-_min)/(_max-_min)
	
	return y

def distr(dm, dv, saccVar, trim=True, withinize=True, binSize = 50, \
	col = blue[1]):
	
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
	
	if "1" in saccVar:
		sacc = "1"
	elif "2" in saccVar:
		sacc = "2"
	
	# landing position should not be "":
	dm = onObject.onObject(dm, sacc)	
	
	# Normalize initial-saccade latencies across pp:
	dm = dm.addField("newSacc", dtype = float)
	dm = dm.withinize("saccLat1", "newSacc", ["file"])
	
	# Exclude outliers:
	dm = dm.selectByStdDev(keys=[], dv = "newSacc")
	
	# Divide sacc latency into 8 equal bins:
	dm = dm.addField("binnedSaccLat")
	dm= dm.calcPerc("newSacc", "binnedSaccLat",keys = ["file"],\
		nBin = 8)

	# Normalize landing positions across binned latency and handle side:
	dm= dm.addField("newLanding", dtype = float)
	dm= dm.withinize(dv, "newLanding", \
		["binnedSaccLat", "handle_side"])
	
	dm= dm.removeField("__dummyCond__")
	dm= dm.removeField("__stdOutlier__")
	#dm = dm.selectByStdDev(keys=[], dv ="newLanding")

	#samp = dm[dv]
	samp = dm["newLanding"]
	#nBins = len(samp)/binSize
	nBins = 50
	
	plt.axvline(0, linestyle = "--", color = gray[3])
	y, edges = np.histogram(samp, bins = nBins)
	
	y = normY(y)
			
	x = .5*edges[1:] + .5*edges[:-1]
	plt.plot(x, y, '-', color = col)
	#plt.show()
	plt.savefig("test.png")
	
if __name__ == "__main__":


	for exp in ["004B"]: #, "004B"]:

		# Data processing:
		src = 'selected_dm_%s_WITH_drift_corr.csv' % exp
		main_dm = CsvReader(src).dataMatrix()

		fig = plt.figure(figsize = (7,3))
		plt.subplots_adjust(wspace=0)#, left = .2, bottom = .15)
	
		nCols = 2
		nRows = 1
		nPlot = 0

		for sacc in ["1", "2"]:
			
			colList = [orange[1], blue[1]]
			
			nPlot +=1
			plt.subplot(nRows, nCols, nPlot)

			if exp == "004B":
				varList = ["endX%sNormToHandle" % sacc]
			if exp == "004A":
				varList = ["endX%sNormToHandle" %sacc, \
					"endX%sCorrNormToHandle" % sacc]
			
			for dv in varList:			
				distr(main_dm, dv, "saccLat%s" % sacc, col=colList.pop())
			plt.axvline(0, color = gray[3])
			plt.xlabel("Normalized landing positions")
			plt.ylabel("Frequency")
			
		plt.savefig(os.path.join(dst,"Distr_%s.png" % exp))