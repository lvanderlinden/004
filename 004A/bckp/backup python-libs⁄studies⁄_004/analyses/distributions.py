#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: distributions.py

"""
DESCRIPTION:
Distribution analyses for experiment 004
"""

# Import Python modules:
import math
import numpy as np
import scipy
from matplotlib import cm
from matplotlib import pyplot as plt
import sys
import os
import random


# Import own modules:
from exparser.EyelinkAscFolderReader import EyelinkAscFolderReader
from exparser.DataMatrix import DataMatrix
from exparser.PivotMatrix import PivotMatrix
from exparser.AnovaMatrix import AnovaMatrix
from exparser import Constants
import msg.userMsg
import hexTango

# Set font
plt.rc("font", family=Constants.fontFamily)
plt.rc("font", size=12)

outputFolder = "."


# Define functions:


def distHist(dm, dv, nBin = 100, showFig = False, saveFig = True, \
	col = "#f57900", cousineau = True, saveExt = ".jpg", zTransform = True,\
	subjectID = "file", trim = True, figName = None):
	
	"""
	Plots a distribution histogram for a given dv
	
	Arugments:
	dm
	dv

	
	Keyword arguments:
	nBin			--- Number of bins. Default = 50.
	showFig
	saveFig
	cousineau	--- Boolean indicating whether or not to remove between-subjects
					variability (i.e. vincentizing?). Default = True
	saveFig		--- Boolean indicating whether or not to save the figure.
					Default = True.
	saveExt		---	extension of the to-be-saved figure. Default = ".svg"
	zTransform	--- Boolean indicating whether or not to do a z-transformation.
	colList
	"""
	# Check whether 'factor' and 'dv' are column headers in the spread sheet:
	vNames = dm.asArray()[0]
	
	# Determine whether experiment 004 or 004B is analysed.
	# This can be done by checking whether the variable 'durCheck1' exists,
	# which is only the case for experiment 004:
	if "durCheck1" in vNames:
		exp = "004"
	else:
		exp = "004B"
	
	if not dv in vNames:
		msg.userMsg.userMsg("The dv %s is not a column header."%dv, __file__)
		return
	
	if trim:
		dm = dm.selectByStdDev(keys = [subjectID], dv = dv)
	
	fig = plt.figure()
	
	if figName == None:
		figName = "Exp %s: DistHist	%s nBin = %s cousineau = %s zTransform = %s trim = %s" %\
			(exp, dv, nBin, cousineau, zTransform, trim)
	plt.suptitle(figName)

	# Get DM according to keyword arguments:
	if cousineau:
		new_var = "new_%s" % (dv)
		dm = dm.addField(new_var, dtype=float)
		dm.withinize(dv, new_var,subjectID,whiten=zTransform,verbose=False)


	if cousineau:
		data = dm[new_var]
	else:
		data = dm[dv]

	perBin = plt.hist(data, nBin, normed=1,facecolor=col)
		#, alpha=0.2)[1]
	
	if showFig:
		plt.show()
		saveFig = False
	if saveFig:
		plt.savefig(os.path.join(outputFolder, "%s%s"%(figName,saveExt)))


def distHistSplit(dm, dv, factor, nBin =50, showFig = False, saveFig = True, \
		cousineau=True, saveExt = ".jpg", zTransform = True, subjectID = "file",\
		trim = True, figName = None):

	"""
	Plots a distribution histogram for a dv, split by a given factor.
	
	Arugments:
	dm
	dv
	factor

	
	Keyword arguments:
	nBin			--- Number of bins. Default = 50.
	showFig
	saveFig
	cousineau	--- Boolean indicating whether or not to remove between-subjects
					variability (i.e. vincentizing?). Default = True
	saveFig		--- Boolean indicating whether or not to save the figure.
					Default = True.
	saveExt		---	extension of the to-be-saved figure. Default = ".svg"
	zTransform	--- Boolean indicating whether or not to do a z-transformation.
	colList
	"""
	# Check whether 'factor' and 'dv' are column headers in the spread sheet:
	vNames = dm.asArray()[0]
	
	# Determine whether experiment 004 or 004B is analysed.
	# This can be done by checking whether the variable 'durCheck1' exists,
	# which is only the case for experiment 004:
	if "durCheck1" in vNames:
		exp = "004"
	else:
		exp = "004B"

	
	if not factor in vNames:
		msg.userMsg.userMsg("The factor %s is not a column header."%factor, __file__)
		return
	if not dv in vNames:
		msg.userMsg.userMsg("The dv %s is not a column header."%dv, __file__)
		return
	
	lvlList = np.unique(dm[factor])

	# Determine number of columns:
	if factor == subjectID:
		nCols = 3
		nRows = 4
		nBin = 20
		fig = plt.figure(figsize = (30,20))
		colList = hexTango.hexTango[:]

	else:
		nCols = 1 # 4 muscles
		nRows = len(lvlList)
		fig = plt.figure()
		colList = hexTango.hexTangoSelection[:]

	plotNr = 0
	
	
	if trim:
		if factor == subjectID:
			dm = dm.selectByStdDev(keys = [subjectID], dv = dv)
		else:
			dm = dm.selectByStdDev(keys = [factor] + [subjectID], dv = dv)

	if cousineau:
		new_var = "new_%s" % (dv)
		dm = dm.addField(new_var, dtype=float)
		dm.withinize(dv, new_var,subjectID,whiten=zTransform,verbose=False)

	if figName == None:
		figName = "Exp %s: DistHist %s split by %s nBin = %s cousineau = %s zTransform = %s trim = %s" %\
			(exp, dv, factor, nBin, cousineau, zTransform, trim)
	plt.suptitle(figName)

	# Get DM according to keyword arguments:
	for lvl in lvlList:
		
		_dm = dm.select("%s =='%s'" % (factor, lvl))
		
		
		if cousineau:
			data = _dm[new_var]
		else:
			data = _dm[dv]

		plt.hist(data, nBin, normed=1,facecolor=colList.pop(),alpha = .2)
	
	if zTransform:
		plt.xlim(-5, 5)
	plt.legend(lvlList)
	if showFig:
		plt.show()
		saveFig = False
	if saveFig:
		plt.savefig(os.path.join(outputFolder, "%s%s"%(figName,saveExt)))
	
def distHistTwoVars(dm, dvList, nBin =50, showFig = False, saveFig = True, \
		cousineau=True, saveExt = ".jpg", zTransform = True, subjectID = "file",\
		trim = True, figName = None, xLabel = None):

	"""
	Plots a distribution histogram for a dv, split by a given factor.
	
	Arugments:
	dm
	dvList		--- list of dv's
	factor

	
	Keyword arguments:
	nBin			--- Number of bins. Default = 50.
	showFig
	saveFig
	cousineau	--- Boolean indicating whether or not to remove between-subjects
					variability (i.e. vincentizing?). Default = True
	saveFig		--- Boolean indicating whether or not to save the figure.
					Default = True.
	saveExt		---	extension of the to-be-saved figure. Default = ".svg"
	zTransform	--- Boolean indicating whether or not to do a z-transformation.
	colList
	"""
	# Check whether 'factor' and 'dv' are column headers in the spread sheet:
	vNames = dm.asArray()[0]

	# Determine whether experiment 004 or 004B is analysed.
	# This can be done by checking whether the variable 'durCheck1' exists,
	# which is only the case for experiment 004:
	if "durCheck1" in vNames:
		exp = "004"
	else:
		exp = "004B"


	driftCorr = dm["driftCorr"][0]
	
	colList = hexTango.hexTangoSelection[:]

	for dv in dvList:
		
		if not dv in vNames:
			msg.userMsg.userMsg("The dv %s is not a column header."%dv, __file__)
			return

	
		if trim:
			new_dm = dm.selectByStdDev(keys = [subjectID], dv = dv)

		if cousineau:
			new_var = "new_%s" % (dv)
			new_dm = new_dm.addField(new_var, dtype=float)
			new_dm.withinize(dv, new_var,subjectID,whiten=zTransform,verbose=False)

		if figName == None:
			figName = "Exp %s: DistHist	 %s and %s nBin = %s cousineau = %s zTransform = %s trim = %s" %\
				(exp, dvList[0], dvList[1], nBin, cousineau, zTransform, trim)
		plt.suptitle(figName)

		if cousineau:
			data = new_dm[new_var]
		else:
			data = new_dm[dv]

		plt.hist(data, nBin, normed=1,facecolor=colList.pop(),alpha = .2)
		
	if zTransform:
		plt.xlim(-5, 5)
	plt.legend(dvList)
	
	if xLabel == None:
		xLabel = dv
	plt.xlabel(xLabel)

	
	if ('endX' or 'startX') in dvList[0] or ('endX' or 'startX') in dvList[1]:
		plt.axvline(0, linestyle = '--', color = "gray")
	if showFig:
		plt.show()
		saveFig = False
	if saveFig:
		plt.savefig(os.path.join(outputFolder, "%s%s"%(figName,saveExt)))



if __name__ == "__main__":
	
	pass