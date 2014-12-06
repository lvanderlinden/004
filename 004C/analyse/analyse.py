"""
DESCRIPTION:
Analyses for 004C
"""

import parse
from exparser.Cache import cachedDataMatrix, cachedArray
from exparser.PivotMatrix import PivotMatrix
from matplotlib import pyplot as plt
from exparser.TangoPalette import *
import numpy as np
import sys
import constants
import getDm

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

def plotDist(dm, dv, col=None, label=None, bins = 10):
	
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
	
	saccDm = getSaccDm(dm, dv = dv, nBins = nBins, norm = norm, \
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
			plotDist(gapDm, dv, col=col, label = gap, bins = nBins)
			plt.xlim(0,450)
			plt.ylim(0,1.1)
			plt.xlabel(dv)


def lpDist(dm, dvId, norm = True, removeOutliers = True, nBinsSaccLat = 3, \
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
		
		dv = "%s%s" % (dvId,sacc)
		binVar = "saccLat%s" % sacc
		
		saccDm = getSaccDm(dm, dv, nBins = nBinsSaccLat, binVar = binVar, \
			norm=norm, removeOutliers = removeOutliers)
		
		if norm:
			dv = "ws_%s" % dv

		for stimType in dm.unique("stim_type"):
			stimDm = saccDm.select("stim_type == '%s'" % stimType)
			
			plotCount +=1
			plt.subplot(nRows,nCols,plotCount)
			plt.title("stim = %s sacc = %s" % (stimType, sacc))

			# Make 3 bins:
			lCols = [blue[1], orange[1], green[1]]
			for _bin in stimDm.unique("bin_%s" % binVar):
				col = lCols.pop()
				binDm = stimDm.select("bin_%s == %s" % (binVar, _bin))
				plotDist(binDm, dv, col=col, bins = nBinsLps, label = _bin)
			plt.axvline(0, color = gray[3], linestyle = "--")
			#plt.ylabel(dv)
			plt.xlim(-.7, .7)
			plt.ylim(0,1.1)
		plt.xlabel("Normalized LP (neg. = action-performing, pos. = handle)")

def timecourse(dm, dvId, norm = True,  removeOutliers = True, nBins = 10):
	
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
	
	for sacc in (1,2):
	
		dv = "%s%s" % (dvId, sacc)
		binVar = "saccLat%s" % sacc
		saccDm = getSaccDm(dm, dv, nBins = nBins, binVar = binVar, \
			norm=True, removeOutliers=True)
		
		if norm:
			dv = "ws_%s" % dv

		lCols = [orange[1], blue[1]]

		for stimType in dm.unique("stim_type"):
			col = lCols.pop()
			stimDm = saccDm.select("stim_type == '%s'" % stimType)
		
			cmX = stimDm.collapse(['bin_%s' % binVar], binVar)
			cmY = stimDm.collapse(['bin_%s' % binVar], dv)
			
			plt.plot(cmX['mean'], cmY['mean'], marker = 'o', color=col, \
				markerfacecolor='white', markeredgecolor=col, \
				markeredgewidth=1, label = stimType)
		plt.axhline(0, color = gray[3], linestyle = "--")
	
def getSaccDm(dm, dv, nBins, binVar = None ,norm=True, removeOutliers=True):
	
	"""
	Apply selection criteria to sacc dm.
	
	NOTE: I made this a separate function just to be sure that the time course
	and distribution plots come from exactly the same data set.
	
	Arguments:
	dm
	dv
	binVar
	nBins
	"""

	saccDm = dm.select("%s != ''" % dv)
	saccDm = saccDm.select("%s != -1000" % dv)

	if removeOutliers:
		# Remove outliers:
		# LPs:
		saccDm = saccDm.selectByStdDev(keys=["file"], dv = dv)
		saccDm  = saccDm.removeField("__dummyCond__")
		saccDm  = saccDm.removeField("__stdOutlier__")
		if binVar != None:
			# Latencies:
			saccDm  = saccDm.selectByStdDev(keys=["file"], dv =binVar)
			
	if norm:
		# Normalize LPs:
		saccDm = saccDm.addField("ws_%s" % dv)
		saccDm = saccDm.withinize(dv, "ws_%s" % dv, "file")
		dv = "ws_%s" % dv

	if binVar != None:
		# Bin the bin var in the desired number of bins:
		saccDm = saccDm.addField("bin_%s" % binVar)
		
		if norm:
			saccDm = saccDm.calcPerc(binVar, "bin_%s" % binVar, keys=["file"], \
				nBin=nBins)
		else:
			saccDm = saccDm.calcPerc(binVar, "bin_%s" % binVar, nBin=nBins)

	return saccDm

if __name__ == "__main__":
	
	norm = True
	removeOutliers = True
	
	for exp in ["004A", "004C"]:
		if exp == "004A":
			continue
			lDv = ["xNorm", "xNormCorr"]
		if exp == "004C":
			lDv = ["xNorm"]

		dm = getDm.getDm(exp = exp, cacheId = "%s_final" % exp)
		dm = dm.select("subject_nr != 8")
		dm = dm.select("subject_nr != 19")

		for dvId in lDv:
			
			#if dvId == "xNormCorr":
			#	continue
			# DISTRIBUTIONS:
			fig = plt.figure(figsize = (8,8))
			plt.subplots_adjust(hspace = .3, wspace = .3)
			lpDist(dm, dvId, norm = norm, removeOutliers = removeOutliers)
			plt.legend(["early", "medium", "late"], loc='best',frameon = False)
			
			plt.savefig("LP_dist_%s_%s_norm_%s_trim_%s.svg" % (exp, dvId, norm, \
				removeOutliers))
			
			# BINS:
			fig = plt.figure()
			plt.subplots_adjust(hspace = .3)
			timecourse(dm, dvId, norm = norm, \
				removeOutliers = removeOutliers)
			plt.axhline(0, color = gray[5], linestyle = "--")
			plt.ylim(-.4, .1)
			plt.legend(loc='best', frameon =False)
			plt.xlabel("Normalized saccade latency")
			plt.ylabel("Normalized LP (pos. = handle, neg. = action-performing)")
			plt.savefig("Bins_%s_%s_norm_%s_trim_%s.svg" % (exp, dvId, norm, \
				removeOutliers))

	