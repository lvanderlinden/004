"""
DESCRIPTION:
Analyses for 004C
"""

import parse
from exparser.Cache import cachedDataMatrix, cachedArray
from exparser.PivotMatrix import PivotMatrix
from exparser.DataMatrix import DataMatrix
from exparser.RBridge import R
from matplotlib import pyplot as plt
from exparser.TangoPalette import *
import numpy as np
import sys
import constants
import getDm
import getSaccDm
import lme

# Set font:
plt.rc("font", family="arial")
plt.rc("font", size=8)


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

def distributions004A(dm, dvId, norm = True, removeOutliers = True, nBinsSaccLat = 3, \
	nBinsLps = 15):

	"""
	Plots landing positions of first and second fixation for exp 004A:
	
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
		
		#print dv
		#sys.exit()

		
		binVar = "saccLat%s" % sacc
		
		saccDm = getSaccDm.getSaccDm(dm, dv, nBins = nBinsSaccLat, binVar = None, \
			norm=norm, removeOutliers = removeOutliers)
		
		if norm:
			dv = "ws_%s" % dv

		if sacc == 1:
			col = green[0]
			if "Corr" in dv:
				col = blue[0]
			label = "initial saccade"
		elif sacc == 2:
			col = green[2]
			if "Corr" in dv:
				col = blue[2]
			label = "refixation"
			
		
		oneDist(saccDm, dv, col=col, bins = nBinsLps, label = label)
		plt.axvline(0, color = gray[3], linestyle = "--")
		plt.xlim(-.7, .7)
		plt.ylim(0,1.1)
	plt.xlabel("Normalized LP")
	plt.ylabel("Normalized frequency")
	plt.legend(frameon = False, prop={'size':7})

def plotRegression(lmerDm, sacc, col, stimType):
	
	"""
	lmerDm	--- dm containing results lmer
	"""
	
	if sacc == 1:
		minLat = 120
		maxLat = 280
	if sacc == 2:
		minLat = 250
		if exp == "004C":
			maxLat = 600
		elif exp == "004A":
			maxLat = 550


	# Plot regression:
	if exp == "004A":
		# Determine intercept and slope
		intercept = lmerDm['est'][0]
		slope = lmerDm['est'][1]
		se = lmerDm['se'][0]
		
	if exp == "004C":
		
		# Non-object = reference
		intercept = lmerDm['est'][0]
		slope = lmerDm['est'][1]
		se = lmerDm['se'][0]
		
		if stimType == "object":
			intercept += lmerDm['est'][2] # Main effect stim_type
			slope += lmerDm['est'][3] # interaction
		
	xData = np.array([minLat, maxLat])		
	yData = intercept + slope * xData
	yMax = intercept + 1.96*se + slope*xData
	yMin = intercept - 1.96*se + slope*xData		
	plt.fill_between(xData, yMin, yMax, alpha=.15, color=col)
	#plt.plot(xData, yData, linestyle='--', color=col)
	plt.plot(xData, yData, color=col)

def timecourse(dm, dvId, norm = True,  removeOutliers = True, nBins = 10, \
	fullModel = False,center = False):
	
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
	
	plt.subplots_adjust(bottom = .1)

	plt.axhline(0, color = "black", linestyle = "--")

	for sacc in (1,2):
	
		dv = "%s%s" % (dvId, sacc)
		binVar = "saccLat%s" % sacc
		saccDm = getSaccDm.getSaccDm(dm, dv, nBins = nBins, binVar = binVar, \
			norm=True, removeOutliers=True)
		
		lmerDm = lme.lmePerSacc(saccDm, sacc = sacc, dvId = dvId, \
			fullModel = fullModel, center = center)
		
		if norm:
			dv = "ws_%s" % dv
		
		for stimType in dm.unique("stim_type"):
			if stimType == "object":
				col = blue[1]
				if exp == "004A" and not "Corr" in dv:
					col = green[1]

			elif stimType == "non-object":
				col = orange[1]
			
			stimDm = saccDm.select("stim_type == '%s'" % stimType)
			
			plotRegression(lmerDm, sacc, col, stimType)
			
			# Plot bins:
			cmX = stimDm.collapse(['bin_%s' % binVar], binVar)
			cmY = stimDm.collapse(['bin_%s' % binVar], dv)
			plt.scatter(cmX['mean'], cmY['mean'], marker = 'o', color="white",\
				edgecolors=col)

	if exp == "004C":
		plt.ylim(-.2, .07)
	else:
		plt.ylim(-.32, .1)
	plt.xlabel("Normalized saccade latency")
	plt.ylabel("Normalized LP")
	if exp == "004C":
		plt.xlim(100, 600)
	elif exp == "004A":
		plt.xlim(100, 550)
	
	if not fullModel and not center:
		if "Corr" in dv:
			plt.savefig("./plots/%s_timecourse_Corr.svg" % exp)
			plt.savefig("./plots/%s_timecourse_Corr.png" % exp)
		else:
			plt.savefig("./plots/%s_timecourse.svg" % exp)
			plt.savefig("./plots/%s_timecourse.png" % exp)


if __name__ == "__main__":
	
	norm = True
	removeOutliers = True
	
	exp = "004A"
	
	dm = getDm.getDm(exp = exp, cacheId = "%s_final" % exp)
	
	for center in [True, False]:
		
		#if center == False:
		#	continue

		for dvId in ["xNorm", "xNormCorr"]:

			fig = plt.figure(figsize = (10,4))
			plt.subplots_adjust(wspace = .3, bottom = .3, left = .05, right = .95)
			ax0 = plt.subplot2grid((1, 3), (0, 0))#, colspan=2)
			plt.title("a) Distributions")
			#plt.subplot(121)
			distributions004A(dm, dvId, norm = norm, \
				removeOutliers = removeOutliers)
			
			#plt.subplot(122)
			ax1 = plt.subplot2grid((1, 3), (0, 1), colspan = 2)
			plt.title("b) Timecourse")
			timecourse(dm, dvId, norm = norm, \
				removeOutliers = removeOutliers, center=center)
			if not center:
				plt.savefig("%s_%s.png" % (exp, dvId))