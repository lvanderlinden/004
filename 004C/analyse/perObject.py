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

def lpTimecourse(dm, dvId, norm = True,  removeOutliers = True, nBins = 3):
	
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
		
		print
		print
		print "Sacc = ", sacc
		
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
		
		dvId = "xNorm"

		dm = getDm.getDm(exp = exp, cacheId = "%s_final" % exp)
		
		for stimName in dm.unique("stim_name"):
			
			_dm = dm.select("stim_name == '%s'" % stimName)
			cogDegr = _dm.select("flip == 'right'", verbose = False).unique("xCogScaledDegr")[0]

			fig = plt.figure(figsize = (10,4))
			plt.title("%s: CoG %s" % (stimName, cogDegr))
			lpTimecourse(_dm, dvId, norm = norm, \
				removeOutliers = removeOutliers)
			plt.axhline(0, color = gray[5], linestyle = "--")
			plt.ylim(-.5, .5)
			#plt.legend(frameon =False)
			plt.xlabel("Normalized saccade latency")
			plt.ylabel("Normalized LP")
			plt.savefig("%s_timecourse.png" % stimName)

	