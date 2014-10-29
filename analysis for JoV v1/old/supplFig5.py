#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: supplFig5.py

"""
Distributions of landing positions per experiment.

TODO:
- Normalise such that y axes have the same range
- Fit?
- 0's in saliency simulation
- 
"""

# Import Python modules:
import numpy as np
import os
import sys
from matplotlib import pyplot as plt
import scipy.stats
from scipy.stats import norm
from numpy import linspace
from pylab import plot,show,hist,figure,title


# Import own modules:
from exparser.DataMatrix import DataMatrix
from exparser.PivotMatrix import PivotMatrix
from exparser.AnovaMatrix import AnovaMatrix
from exparser import TangoPalette as tango
import getDM
import onObject

plt.rc("font", family="arial")
plt.rc("font", size=7)

dst = "/home/lotje/Documents/PhD Marseille/Studies/004 - Single-object experiment - Handle-orientation effect/manuscript/sources"

fig = plt.figure(figsize = (6,6))
plt.subplots_adjust(wspace=0.1, hspace = 0.1)
nPlot = 0
nCols = 3
nRows = 4

colList = ["#3465a4", "#f57900", "#73d216", "#ef2929"]
letList = ["c", "b", "a"]

for exp in ["004A", "004B", "004C"]:
	
	dm = getDM.getDM(exp,onlyControl=False)
	#print dm.unique("contrast_side")
	
	if exp == "004A":
		dvList = ["abs", "corr"]
	else:
		dvList = ["abs"]
		
	if exp == "004C":
		nBins = 20
	else:
		nBins= 100
	
	for dvType in dvList:
		col = colList.pop()
		lMeans = []
		
		for sacc in ["1", "2", "3"]:
			
			if dvType == "corr":
				dv = "endX%sCorrNormToHandle" % sacc
			else:
				dv = "endX%sNormToHandle" % sacc
		
			# dv must not contain ''s:
			on_dm = onObject.onObject(dm, sacc)
			trim_dm = on_dm.selectByStdDev(keys = ["file"], dv = dv)
		
			nBins = int(len(trim_dm)/20)
			nBins = 100

			samp = trim_dm[dv]

			nPlot +=1
			ax = plt.subplot(nRows, nCols, nPlot)
			if exp == "004A" and dv == "endX%sNormToHandle" % sacc:
				plt.title('%s) Saccade %s' % (letList.pop(), sacc))

			a, edges = np.histogram(samp, bins = nBins)
#			
			a = abs(a)
			
			k = 3
			maxVal = a.mean() + a.std() * k
			i = np.where(a > maxVal)
			a[i] = maxVal
			
			_min = float(np.min(a))
			_max = float(np.max(a))
			
			y = (a-_min)/(_max-_min)			
			
			
			x = .5*edges[1:] + .5*edges[:-1]
			
			if sacc == "1":
				plt.ylabel("Normalised frequency")
			else:
				ax.yaxis.set_ticklabels([])			
			
			plt.plot(x, y, color = col, linewidth = 1.5)				
			plt.axvline(0, linestyle = "--", color = "#888a85", \
				linewidth = 2)
			plt.xlim([-.7, .7])				

			if exp != "004C":
				plt.xticks([])
				
plt.savefig("distributions.png")
plt.savefig("distributions.svg")

plt.show()
	