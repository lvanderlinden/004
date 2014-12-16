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


def distributions004C(dm, dvId, norm = True, removeOutliers = True, nBinsSaccLat = 3, \
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
	
	fig = plt.figure(figsize = (8,4))
	
	for stimType in dm.unique("stim_type"):
		stimDm = dm.select("stim_type == '%s'" % stimType)
		
		plotCount +=1
		
		plt.subplot(1,2,plotCount)
		plt.title(stimType)

		for sacc in [1, 2]:
			dv = "%s%s" % (dvId,sacc)
			
			
			binVar = "saccLat%s" % sacc
			
			saccDm = getSaccDm.getSaccDm(stimDm, dv, nBins = nBinsSaccLat, binVar = None, \
				norm=norm, removeOutliers = removeOutliers)
			
			if norm:
				dv = "ws_%s" % dv

			if sacc == 1:
				label = "initial saccade"
				if stimType == "object":
					col = blue[0]
				elif stimType == "non-object":
					col = orange[0]

			elif sacc == 2:
				label = "refixation"
				if stimType == "object":
					col = blue[2]
				elif stimType == "non-object":
					col = orange[2]
			
			oneDist(saccDm, dv, col=col, bins = nBinsLps, label = label)
			plt.axvline(0, color = gray[3], linestyle = "--")
			plt.xlim(-.7, .7)
			plt.ylim(0,1.1)
		
		if stimType == "object":
			plt.ylabel("Normalized frequency")
		
		plt.xlabel("Normalized LP")
		plt.ylabel("Normalized frequency")
		
		plt.legend(frameon = False)
		
	plt.savefig("./plots/Distribution_004C.svg")
	plt.savefig("./plots/Distribution_004C.png")

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

def timecourse(dm, dvId, norm = True,  removeOutliers = True, nBins = 15, \
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
	
	fig = plt.figure(figsize = (8,4))
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
					col = green[0]

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
		plt.ylim(-.4, .1)
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

def saliency():
	
	"""
	Plots avg LPs simulation
	"""
	
	fig = plt.figure(figsize = (1.5,4))
	
	dm = DataMatrix(np.load(".cache/dm_sim_select_driftcorr.npy"))

	for stimType in dm.unique("stim_type"):
		
		if stimType == "object":
			col = blue[1]
		elif stimType == "non-object":
			col = orange[1]
		
		lSacc = []
		for sacc in [1,2]:
			stimDm = dm.select("stim_type == '%s'" % stimType)
		
			m = stimDm["xNorm%s" % sacc].mean()
			lSacc.append(m)
			
		plt.plot([1,2], lSacc, color = col, marker = 'o', markerfacecolor = 'white',
			markeredgecolor = col, markeredgewidth = 1)
	
	plt.axhline(0, linestyle = "--", color = gray[3])
	plt.ylim(-.2, .07)
	plt.xlim(0.8, 2.2)
	plt.savefig("./plots/simulation.png")
	plt.savefig("./plots/simulation.svg")

	#plt.show()
	

if __name__ == "__main__":
	
	#saliency()
	#sys.exit()
	
	norm = True
	removeOutliers = True
	center = False
	
	exp = "004C"
	dvId = "xNorm"

	dm = getDm.getDm(exp = exp, cacheId = "%s_final" % exp)

	distributions004C(dm, dvId, norm = norm, \
		removeOutliers = removeOutliers)
	timecourse(dm, dvId, norm = norm, \
		removeOutliers = removeOutliers, center=center)
	saliency()


	