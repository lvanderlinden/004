"""
DESCRIPTION:
Analyses for 004C
"""

import parse
from exparser.Cache import cachedDataMatrix, cachedArray
from exparser.PivotMatrix import PivotMatrix
from exparser.RBridge import R
from matplotlib import pyplot as plt
from exparser.TangoPalette import *
import numpy as np
import sys
import constants
import getDm
import getSaccDm

def yNormDist(y):
	
	"""
	Normalizes y axis distribution plots such that it ranges between 0 and 1.
	
	Arguments:
	y		--- y axis values
	"""

	# Normalise:
	y = abs(y)
	
	_min = float(np.min(y))
	_max = float(np.max(y))
	
	yNorm = (y-_min)/(_max-_min)
	
	return yNorm

def oneDist(dm, dv, col=None, label=None, bins = 10):
	
	"""
	Arguments:
	dm		--- DataMatrix instance
	dv		--- dependent variable
	
	Keyword arguments:
	col 	--- color or None
	label	--- label for the legend; string or None
	bins	--- number of bins
	"""
	
	if col == None:
		col = blue[1]

	# Determine y:
	y, edges = np.histogram(dm[dv], bins = bins)
	yNorm = yNormDist(y)
	
	# Determine x:
	x = .5*edges[1:] + .5*edges[:-1]
	
	# Plot:
	plt.plot(x, yNorm, marker='.', color = col, markeredgecolor = col,\
		markerfacecolor = col, markeredgewidth = 1, label = label)



def gap(dm, dv = "saccLat1", nBins = 10, norm=True, removeOutliers = True):
	
	"""
	Plots sacc lat distributions as a function of gap condition.
	
	Arguments:
	dm		--- DataMatrix instance
	
	Keyword arguments:
	norm	--- Boolean indicating whether or not to remove BS variance.
	"""

	fig = plt.figure()
	nPlot = 0
	
	saccDm = getSaccDm.getSaccDm(dm, dv = dv, nBins = nBins, norm = norm, \
		removeOutliers = removeOutliers)
	
	if norm:
		dv = "ws_%s" % dv

	
	for stimType in dm.unique("stim_type"):
		stimDm = saccDm.select("stim_type == '%s'" % stimType)
		nPlot +=1
		plt.subplot(1,2,nPlot)
		plt.title(stimType)
		lCols = [blue[1], orange[1]]
		for gap in dm.unique("gap"):
			gapDm = stimDm.select("gap == '%s'" % gap)
			col = lCols.pop()
			oneDist(gapDm, dv, col=col, label = gap, bins = nBins)
			plt.xlim(0,450)
			plt.ylim(0,1.1)
			plt.xlabel(dv)


def lpDistribution(dm, dvId, norm = True, removeOutliers = True, nBinsSaccLat = 3, \
	nBinsLps = 15):

	"""
	Plots landing positions of first and second fixation as a function of
	stimulus type
	
	Arguments:
	dm
	dvId		--- {xNorm, xNormAbsCenter}, of which the latter only holds for
				exp 1.
	"""
	
	exp = dm["expId"][0]

	nCols = 2
	nRows = 2
	
	plotCount = 0
	
	for sacc in (1, 2):
		fig = plt.figure(figsize = (5,5))
		
		dv = "%s%s" % (dvId,sacc)
		binVar = "saccLat%s" % sacc
		
		saccDm = getSaccDm.getSaccDm(dm, dv, nBins = nBinsSaccLat, binVar = None, \
			norm=norm, removeOutliers = removeOutliers)
		
		if norm:
			dv = "ws_%s" % dv

		for stimType in dm.unique("stim_type"):
			stimDm = saccDm.select("stim_type == '%s'" % stimType)
			
			if stimType == "object":
				col = blue[1]
			elif stimType == "non-object":
				col = orange[1]
			oneDist(stimDm, dv, col=col, bins = nBinsLps, label = stimType)
			plt.axvline(0, color = gray[3], linestyle = "--")
			plt.xlim(-.7, .7)
			plt.ylim(0,1.1)
		plt.xlabel("Normalized LP")
		plt.ylabel("Normalized frequency")
		plt.legend(frameon = False)
		plt.savefig("./plots/%s_sacc_%s.svg" % (exp, sacc))
		plt.savefig("./plots/%s_sacc_%s.png" % (exp, sacc))

def lpTimecourse(dm, dvId, norm = True,  removeOutliers = True, nBins = 10):
	
	"""
	Arguments:
	dm				--- DataMatrix instance
	dvId		--- {xNorm, xNormAbsCenter}, of which the latter only holds for
					exp 1.
	
	Keyword arguments:
	norm			--- Boolean indicating whether or not to remove the bs-variance
						from the variable on the y axis (for the variable on the x
						axis, we already do this by giving the keyword argument 
						'key' in calcPerc() the value "file".
	removeOutliers	--- Boolean indicating whether or not to trim on 2.5 SDs
						from mean
	nBins			--- number of bins.
	"""
	
	exp = dm["expId"][0]
	
	fig = plt.figure(figsize = (10,4))

	for sacc in (1,2):
	
		dv = "%s%s" % (dvId, sacc)
		binVar = "saccLat%s" % sacc
		saccDm = getSaccDm.getSaccDm(dm, dv, nBins = nBins, binVar = binVar, \
			norm=True, removeOutliers=True)
		
		if norm:
			dv = "ws_%s" % dv
		
		for stimType in dm.unique("stim_type"):
			
			if stimType == "object":
				col = blue[1]
			elif stimType == "non-object":
				col = orange[1]
			
			stimDm = saccDm.select("stim_type == '%s'" % stimType)

			cmX = stimDm.collapse(['bin_%s' % binVar], binVar)
			cmY = stimDm.collapse(['bin_%s' % binVar], dv)
			
			plt.plot(cmX['mean'], cmY['mean'], marker = 'o', color=col, \
				markerfacecolor='white', markeredgecolor=col, \
				markeredgewidth=1, label = stimType)
		plt.axhline(0, color = gray[3], linestyle = "--")
	
	plt.axhline(0, color = gray[5], linestyle = "--")
	plt.ylim(-.25, .05)
	plt.legend(frameon =False)
	plt.xlabel("Normalized saccade latency")
	plt.ylabel("Normalized LP")
	plt.savefig("./plots/%s_timecourse.svg" % exp)
	plt.savefig("./plots/%s_timecourse.png" % exp)

if __name__ == "__main__":
	
	norm = True
	removeOutliers = True

	for exp in ["004A", "004C"]:
		dvId = "xNorm"

		dm = getDm.getDm(exp = exp, cacheId = "%s_final" % exp)
		dm.save("DM_%s.csv" % exp)
		
		## DISTRIBUTIONS:
		lpDistribution(dm, dvId, norm = norm, removeOutliers = removeOutliers)
		
		## BINS:
		lpTimecourse(dm, dvId, norm = norm, \
			removeOutliers = removeOutliers)


	