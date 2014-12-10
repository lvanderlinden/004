"""
DESCRIPTION:
Analyses for 004C
"""

#import parse
#from exparser.Cache import cachedDataMatrix, cachedArray
#from exparser.PivotMatrix import PivotMatrix
#from exparser.RBridge import R
#from matplotlib import pyplot as plt
#from exparser.TangoPalette import *
#import numpy as np
#import sys
#import constants
#import getDm

def getSaccDm(dm, dv, nBins = 10, binVar = None ,norm=True, removeOutliers=True):
	
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
		saccDm = saccDm.selectByStdDev(keys=["file"], dv = dv, verbose = True)
		saccDm  = saccDm.removeField("__dummyCond__")
		saccDm  = saccDm.removeField("__stdOutlier__")
		if binVar != None:
			# Latencies:
			saccDm  = saccDm.selectByStdDev(keys=["file"], dv =binVar)
		#print
		#print "....."
		#raw_input()	
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
	