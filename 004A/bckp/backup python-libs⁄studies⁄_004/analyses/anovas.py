#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: anovas.py

"""
DESCRIPTION:
Functions for performing 1,2, or 3 factorial ANOVA's.

NOTE:
- filtering (e.g. exclude filler objects, exclude control contrast manipulation
	etc. should be done somewhere else because its not handled by the
	functions in this package.

TODO:
- line plots for one-factorial designs
- is it possible to make this one big function?
- trimming should be done here!
- share y axis!
- check if vars are column headers -> more efficient?
"""

# Import Python modules:
import math
import numpy as np
import scipy
from matplotlib import cm
from matplotlib import pyplot as plt
import sys
import os


# Import own modules:
from exparser.EyelinkAscFolderReader import EyelinkAscFolderReader
from exparser.DataMatrix import DataMatrix
from exparser.PivotMatrix import PivotMatrix
from exparser.AnovaMatrix import AnovaMatrix
from exparser.MixedEffectsMatrix import MixedEffectsMatrix

from exparser import Constants
import msg.userMsg

# Set font
plt.rc("font", family=Constants.fontFamily)
plt.rc("font", size=12)

outputFolder = "."

# Define functions:

def statSubplot(am,nRows = 1, nCols = 2, plotNr = 2, flip = True):

	"""
	Plots stats in a subplot.
	
	Arguments:
	am	--- the stats as a string.
	nrRows
	nrCols
	plotNr
	flip
	"""
	# Print the stats:
	plt.subplot(nRows, nCols, plotNr)
	plt.xticks([])
	plt.yticks([])
	#plt.title("stats")
	plt.ylim(0,1)
	plt.xlim(0,1)
	if flip:
		plt.text(.35,.75,am, rotation = "vertical", family='monospace')
	else:
		plt.text(0,.5,am, family='monospace')

def prettyStats(am):
	
	"""
	Creates pretty strings containing stats from one-factorial ANOVA.
	
	Arguments:
	am		--- AnovaMatrix instance.
	varName	--- Identifier for dv
	
	Returns:
	A string containing pretty (APA-like) stats.
	"""
	
	am = am.asArray()
	stats = "F(%d,%d) = %.2f, p = %.4f" % (float(am[1,1]), \
		float(am[2,1]), float(am[2,2]), float(am[2,3]))
	
	return stats
	
def oneFactor(dm, dv, factor, subjectID = ["file"], trim = True, 
		printStats = True, showFig=False, saveFig = True,  figName = None, 
		saveExt = ".jpg", xLabel = None, xLabels = None, yLabel = None, 
		yLim = None, exControlMask = False, exFiller = False):
	
	"""
	Performs and plots a one-factorial ANOVA.
	
	NOTE: The resulting plots are bar plots because 'pm.linePlot()' doesn't
	work with one factor yet.
	
	Arguments:
	dm			--- Data matrix.
	dv			--- Dependent variable.
	factor	 	--- Independent variable.
	
	Keyword arguments:
	subjectID	--- Default = ["file"]
	showFig		--- Boolean indicating whether or not to show the plots. Default 
					= False.
	saveFig		--- Boolean indicating whehter or not to save the plot. Default = 
					True.
	printStats	--- TODO Boolean indicating whether or not to print stats.
	figName	--- Will be used as suptitle and save path, of provided. 
					Default = None.
	saveExt		---
	xLabel		---
	xLabels		---
	yLabel		---
	yLim		--- 
	"""
	
	driftCorr = dm["driftCorr"][0]
	
	# Check whether 'factor' and 'dv' are column headers in the spread sheet:
	vNames = dm.asArray()[0]
	
	if not factor in vNames:
		msg.userMsg.userMsg("The factor %s is not a column header."%factor,\
			__file__)
		return
	
	if not dv in vNames:
		msg.userMsg.userMsg("The dv %s is not a column header."%dv, __file__)
		return
	
	if exControlMask:
		dm = dm.select("mask_side != 'control'")
	
	if exFiller:
		dm = dm.select("symm == 'asymm'")

	# If wanted, trim the data:
	if trim:
		dm = dm.selectByStdDev(keys = factor + subjectID, dv = dv)

	# Get pivot matrix:
	pm = PivotMatrix(dm, factor, subjectID, dv=dv, colsWithin=True)
	
	# Get anova matrix:
	am = AnovaMatrix(dm, factors = factor, dv = dv, \
		subject = subjectID[0])._print(maxLen=10, ret=True)
		
	if printStats:
		print am
	
	# Create figure:
	fig = plt.figure()
	if figName == None:
		name = "%s effect on %s - trim = %s exControlMask = %s exFiller = %s driftCorr = %s"%(\
			factor, dv, trim, exControlMask, exFiller, driftCorr)
	else:
		name = figName
	
	plt.suptitle(name)
	
	# Plot the effect:
	plt.subplot(121)
	
	# Determine some plot properties:
	if yLabel == None:
		yLabel = dv
	if xLabel == None:
		xLabel = factor

	# Change the labels if one of the factors is 'mask_side':
	if factor == ["mask_side"]:
		if "control" in np.unique(dm["mask_side"]):
			xLabels = ["control", "more contrast right", "more contrast left"]
		else:
			xLabels = ["more contrast right", "more contrast left"]

	pm.barPlot(fig = fig, yLabel = yLabel, xLabel = xLabel, xLabels = xLabels, \
		yLim = yLim)
	
	if dv in ["endX", "endXCorr", "endXCorrMask", "endXDegr","endXCorrDegr", "endXCorrMaskDegr"]:
		plt.axhline(0, linestyle = "--", color = "#555753")
	
	statSubplot(am, nRows = 1, nCols = 2, plotNr = 2)

	if showFig:
		plt.show()
		saveFig = False
	if saveFig:
		plt.savefig(os.path.join(outputFolder,"%s%s"%(name,saveExt)))

	

def twoFactor(dm, dv, factors, subjectID = ["file"], trim = True, printStats = True, 
		showFig=False, saveFig = True,  figName = None, 
		saveExt = ".jpg", legendTitle = None, lLabels = None, xLabel = None, 
		xLabels = None, yLabel = None,exControlMask = False, exFiller = False, \
		mixedEffects = False, exMask = False, yLim = None):
	
	"""
	Performs and plots a two-factorial ANOVA.
	
	Arguments:
	dm			--- Data matrix.
	dv			--- Dependent variable.
	factors 	--- List containing two factor identifiers.
	
	Keyword arguments:
	subjectID	--- Default = ["file"]
	showFig		--- Boolean indicating whether or not to show the plots. Default 
					= False.
	saveFig		--- Boolean indicating whehter or not to save the plot. Default = 
					True.
	printStats	--- TODO Boolean indicating whether or not to print stats.
	figName	--- Will be used as suptitle and save path, of provided. 
					Default = None.
	saveExt		---
	legendTitle	---
	lLabels 	---
	xLabel		---
	xLabels		---
	yLabel		---
	"""
	
	driftCorr = dm["driftCorr"][0]
	
	# Check whether 'factor' and 'dv' are column headers in the spread sheet:
	vNames = dm.asArray()[0]
	
	for factor in factors:
		if not factor in vNames:
			msg.userMsg.userMsg("The factor %s is not a column header."%factor,\
				factor, __file__)
			return
	if not dv in vNames:
		msg.userMsg.userMsg("The dv %s is not a column header."%dv, __file__)
		return
	
	# If wanted, trim the data:
	if trim:
		dm = dm.selectByStdDev(keys = factors + subjectID, dv = dv)

	# Apply selection criteria:
	if exControlMask:
		dm = dm.select("mask_side != 'control'")
	if exMask:
		dm = dm.select("mask_side == 'control'")
	
	if exFiller:
		dm = dm.select("symm == 'asymm'")

	# Get pivot matrix:
	pm = PivotMatrix(dm, factors, subjectID, dv=dv, colsWithin=True)
	
	# Get anova matrix:
	am = AnovaMatrix(dm, factors = factors, dv = dv, \
		subject = subjectID[0])._print(maxLen=10, ret=True)
	if mixedEffects:
		mem = MixedEffectsMatrix(dm, dv, factors, subjectID)._print(maxLen=10, ret=True)
	
	if printStats:
		if mixedEffects:
			print "MIXED EFFECTS:"
			print mem
		print "ANOVA:"
		print am
	
	# Create figure:
	fig = plt.figure()
	if figName == None:
		name = "%s by %s effect on %s - trim = %s exControlMask = %s exMask = %s exFiller = %s driftCorr = %s"%(\
			factors[0], factors[1], dv, trim, exControlMask, exMask, exFiller, driftCorr)
	else:
		name = figName
	
	# Determine some plot properties:
	if yLabel == None:
		yLabel = dv
	if legendTitle == None:
		legendTitle = factors[0]
	if xLabel == None:
		xLabel = factors[1]
	
	# Change the labels if one of the factors is 'mask_side':
	if "mask_side" == factors[0]:
		if "control" in np.unique(dm["mask_side"]):
			lLabels = ["control", "more contrast right", "more contrast left"]
		else:
			lLabels = ["more contrast right", "more contrast left"]
	if "mask_side" == factors[1]:
		if "control" in np.unique(dm["mask_side"]):
			xLabels = ["control", "more contrast right", "more contrast left"]
		else:
			xLabels = ["more contrast right", "more contrast left"]
	
	# Plot effect:
	plt.subplot(121)
	plt.suptitle(name)
	pm.linePlot(fig = fig, legendTitle = legendTitle, xLabel = xLabel, \
		lLabels = lLabels, xLabels = xLabels, yLabel = yLabel, yLim = yLim)
	
	if dv in ["endX", "endXCorr", "endXCorrMask", "endXDegr","endXCorrDegr", "endXCorrMaskDegr"]:
		plt.axhline(0, linestyle = "--", color = "#555753")

	
	# Print the stats:
	if mixedEffects:
		statSubplot(mem)
	else:
		statSubplot(am)
	if showFig:
		plt.show()
		saveFig = False
	if saveFig:
		plt.savefig(os.path.join(outputFolder,"%s%s"%(name,saveExt)))

def threeFactor(dm, dv, factors, subjectID = ["file"], trim = True, printStats = True, 
		showFig=False, saveFig = True,  figName = None, 
		saveExt = ".jpg", legendTitle = None, lLabels = None, xLabel = None, 
		xLabels = None, yLabel = None,exControlMask = False, exFiller = False):
	
	"""
	Performs and plots a three-factorial ANOVA
	
	dm			--- Data matrix.
	dv			--- Dependent variable.
	factors 	--- List containing three factor identifiers. Note that the first
					factor in the list is used to split the effects per subplot.
	
	Keyword arguments:
	subjectID	--- Default = ["file"]
	showFig		--- Boolean indicating whether or not to show the plots. Default 
					= False.
	saveFig		--- Boolean indicating whehter or not to save the plot. Default = 
					True.
	printStats	--- TODO Boolean indicating whether or not to print stats.
	figName		--- Will be used as suptitle and save path, of provided. 
					Default = None.
	saveExt		---
	legendTitle	---
	lLabels 	---
	xLabel		---
	xLabels		---
	yLabel		---
	"""
	
	driftCorr = dm["driftCorr"][0]
	
	# Check whether 'factor' and 'dv' are column headers in the spread sheet:
	vNames = dm.asArray()[0]
	
	for factor in factors:
		if not factor in vNames:
			msg.userMsg.userMsg("The factor %s is not a column header."%factor,\
				factor, __file__)
			return
	if not dv in vNames:
		msg.userMsg.userMsg("The dv %s is not a column header."%dv, __file__)
		return
	
	# Apply selection criteria:
	if exControlMask:
		dm = dm.select("mask_side != 'control'")
	
	if exFiller:
		dm = dm.select("symm == 'asymm'")

	
	if trim:
		dm = dm.selectByStdDev(keys = factors + subjectID, dv = dv)

	# Get anova matrix:
	am = AnovaMatrix(dm, factors = factors, dv = dv, subject = \
		subjectID[0])._print(maxLen=20,ret=True)

	if printStats:
		print am


	# One of the factors is used to split the dm (for plotting purposes only,
	# the anova is carried out 'correctly').
	splitFactor = factors[0]
	twoFactors = factors[1:]
	lvlList = np.unique(dm[splitFactor])
	
	# Create the figure:
	fig = plt.figure()
	name = "%s by %s by %s effect on %s - Trim = %s exControlMask = %s exFiller = %s driftCorr = %s" %(factors[0], factors[1], \
		factors[2], dv, trim, exControlMask, exFiller, driftCorr)
	plt.suptitle(name)
	
	nRows = 1
	nCols = len(lvlList)+1 # 1 for the stats
	plotNr = 0
	
	# Create the subplots:
	for lvl in lvlList:
		
		# Select one level:
		_dm = dm.select('%s == "%s"' % (splitFactor, lvl))
		
		# Get pivot matrix:
		pm = PivotMatrix(_dm, twoFactors, subjectID, dv = dv, colsWithin=True)

		# Plot:
		plotNr +=1

		if legendTitle == None:
			legendTitle = twoFactors[0]
		if xLabel == None:
			xLabel = twoFactors[1]
		if yLabel == None:
			yLabel = dv

		plt.subplot(nRows, nCols, plotNr)
		plt.title(lvl)
		pm.linePlot(fig = fig, xLabel = xlabel, xLabels = xLabels, \
			legendTitle = legendTitle, lLabels = lLabels, yLabel = yLabels)
		
		if dv in ["endX", "endXCorr"]:
			plt.axhline(0, linestyle = "--", color = "#555753")

	
	# Plot stats:
	statSubplot(am, nRows = nRows, nCols = nCols, plotNr = nCols)
	
	if showFig:
		plt.show()
		saveFig = False
	
	if saveFig:
		plt.savefig(os.path.join(outputFolder,"%s%s" % (name, saveExt)))
