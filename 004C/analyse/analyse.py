"""
DESCRIPTION:
Analyses for 004C
"""

import getDm
import parse
from exparser.Cache import cachedDataMatrix, cachedArray
from exparser.PivotMatrix import PivotMatrix
from matplotlib import pyplot as plt
from exparser.TangoPalette import *
import numpy as np
import sys
import selectDm

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



def gap(dm, norm=True, dv = "saccLat1", bins = 10):
	
	"""
	Plots sacc lat distributions as a function of gap condition.
	
	Arguments:
	dm		--- DataMatrix instance
	
	Keyword arguments:
	norm	--- Boolean indicating whether or not to remove BS variance.
	"""

	fig = plt.figure()
	lCols = [orange[1], blue[1]]
	
	if not norm:
		dv = dv
	
	elif norm:
		dm = dm.addField("ws_%s" % dv)
		dm = dm.withinize(dv, "ws_%s" % dv, "file")
		dv = "ws_%s" % dv
	
	for gap in dm.unique("gap"):
		_dm = dm.select("gap == '%s'" % gap)
		col = lCols.pop()
		plotDist(_dm, dv, col=col, label = gap, bins = bins)
	plt.legend(loc = 'best', frameon =False)
	plt.savefig("gap.png")


def lpDist(dm,  norm = True):

	"""
	Plots landing positions of first and second fixation as a function of
	stimulus type
	"""
	
	fig = plt.figure()
	plotCount = 0
	for sacc in (1, 2):
		saccDm = dm.select("xNorm%s != ''" % sacc)
		saccDm = saccDm.select("xNorm%s != -1000" % sacc)
		
		dv = "xNorm%s" % sacc
		binVar = "saccLat%s" % sacc
		
		if not norm:
			dv = dv
	
		elif norm:
			saccDm = saccDm.addField("ws_%s" % dv)
			saccDm = saccDm.withinize(dv, "ws_%s" % dv, "file")
			dv = "ws_%s" % dv

		for stimType in dm.unique("stim_type"):
			stimDm = saccDm.select("stim_type == '%s'" % stimType)
			
			plotCount +=1
			plt.subplot(2,2,plotCount)
			plt.title("stim = %s sacc = %s" % (stimType, sacc))

			# Make 3 bins:
			stimDm = stimDm.addField("bin_%s" % binVar)
			stimDm = stimDm.calcPerc(binVar, "bin_%s" % binVar, keys="file", nBin=3)
			
			lCols = [blue[1], orange[1], green[1]]
			for _bin in stimDm.unique("bin_%s" % binVar):
				col = lCols.pop()
				binDm = stimDm.select("bin_%s == %s" % (binVar, _bin))
				plotDist(binDm, dv, col=col, bins = 10, label = _bin)
			plt.axvline(0, color = gray[3], linestyle = "--")
			plt.ylabel(dv)
		
		plt.legend(frameon=False, loc = 'best', title = binVar)
		plt.savefig("lp.png")

def timecourse(dm, dv1, dv2, norm = False,  bins = 10):
	
	"""
	Arguments:
	dm		--- DataMatrix instance
	var1	--- bin variable (x axis)
	var2	--- dependent variable (y axis)
	
	Keyword arguments:
	norm	--- Boolean indicating whether or not to remove the bs-variance
				from the variable on the y axis (for the variable on the x
				axis, we already do this by giving the keyword argument 
				'key' in calcPerc() the value "file".
	bins	--- number of bins.
	"""
	
	fig = plt.figure()
	
	if not norm:
		dv2 = dv2
	
	elif norm:
		dm = dm.addField("ws_%s" % dv2)
		dm = dm.withinize(dv2, "ws_%s" % dv2, "file")
		dv2 = "ws_%s" % dv2

	lCols = [orange[1], blue[1]]

	for stimType in dm.unique("stim_type"):
		col = lCols.pop()
		stimDm = dm.select("stim_type == '%s'" % stimType)
		stimDm = stimDm.addField("bin_%s" % dv1)
		stimDm = stimDm.calcPerc(dv1, "bin_%s" % dv1, keys=["file"], nBin=10)
	
		cmX = stimDm.collapse(['bin_%s' % dv1], dv1)
		cmY = stimDm.collapse(['bin_%s' % dv1], dv2)
		
		plt.plot(cmX['mean'], cmY['mean'], marker = 'o', color=col, \
			markerfacecolor='white', markeredgecolor=col, \
			markeredgewidth=1, label = stimType)
	plt.axhline(0, color = gray[3], linestyle = "--")
	plt.legend()
	plt.savefig("bin.png")
	
	

if __name__ == "__main__":

	dm = parse.parseAsc(cacheId = "parsed")
	dm = getDm.addCoord(dm,cacheId = "with_coord")
	dm = getDm.addLat(dm, cacheId = "with_lat")
	dm = selectDm.selectDm(dm, cacheId = "selection")
	
	#gap(dm)
	lpDist(dm)
	#timecourse(dm, "saccLat1", "xNorm1")
	
