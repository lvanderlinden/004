#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Filename: distrAnComp.py

"""
DESCRIPTION:
Experiment 004B
Calculates effect size per bin (split per participant and condition)
in order to investigate whether the effect size changes as a function of time.

TODO: 
- trim and test

NOTE:
- most useful for factors like congruency, where the effect size is a difference
score
""" 

# Import Python modules:
import numpy as np
from matplotlib import pyplot as plt
import sys
import os

# Import own modules:
from exparser.DataMatrix import DataMatrix
from exparser.PivotMatrix import PivotMatrix
from exparser.AnovaMatrix import AnovaMatrix
from exparser import Constants
import msg.userMsg

# Set font
plt.rc("font", family=Constants.fontFamily)
plt.rc("font", size=Constants.fontSize)

# Output folder:
dst = "."


def binAnalyses(dm, dv, varToBin, factor, subjectID = "file",
		nBin = 10, saveFig = True, showFig = False, saveExt = ".jpg", 
		fileName = None, trim = True):
	
	"""
	Plots effect size of a given dv as a function of a given binned dv.
	
	Arguments:
	dm 			--- experiment
	dv
	varToBin
	factor
	
	
	Keyword arguments:
	nBin 		--- number of bins. Default = 10
	saveFig		--- Boolean indicating whether or not to save the figure.
					Default = True.
	showFig 		--- 
	saveExt		--- Default = .svg
	trim
	"""
	
	driftCorr = dm["driftCorr"][0]
	
	# Check whether 'factor' and 'dv' are column headers in the spread sheet:
	vNames = dm.asArray()[0]
	
	if not dv in vNames:
		msg.userMsg.userMsg("The dv %s is not a column header."%dv,\
			factor, __file__)
		return
	
	if not dv in vNames:
		msg.userMsg.userMsg("The factor %s is not a column header."%factor,\
			factor, __file__)
		return
	
	if not dv in vNames:
		msg.userMsg.userMsg("The varToBin %s is not a column header."%varToBin,\
			factor, __file__)
		return

	levelList = np.unique(dm[factor])
	
	# Difference scores can only be calculated when the factor has only two 
	# levels, e.g. congr, incongr.
	if len(levelList) > 2:
		msg.userMsg.userMsg("The factor %s has more than two levels.",__file__)
		return

	if trim:
		dm = dm.selectByStdDev(keys = [factor, subjectID], dv = dv)
	
	
	binID = '%sBin'%varToBin
	binKeys = [subjectID, factor] # Bin by subject and condition

	dm = dm.addField(binID)
	dm = dm.calcPerc(varToBin, binID, keys=binKeys, nBin=nBin)

	lY = []
	lX = []
	# Walk through all bins
	for _bin in dm.unique(binID):  
		# Filter out all but one bin
		_dm = dm.select('%s == %f' % (binID, _bin))
				
		# Get the mean for both conditions. Note that using this method, the mean
		# is across all subjects, and not the mean of the mean of the subjects.
		# But this will not make any real difference for the overall pattern. You
		# can prevent this by withinizing the data first.
		m1 = _dm.select('%s == "%s"'%(factor, levelList[0]),\
			verbose=False)[dv].mean()
		
		m2 = _dm.select('%s == "%s"'%(factor, levelList[1]), \
			verbose=False)[dv].mean()
		
		#sys.exit()

		y = m2 - m1 # We are going to plot the difference score on the Y-axis
		# The bin average will be on the X-axis, so you can see how the bins are
		# distributed (i.e. the the bins in the middle are closer together than
		# the bins in the end, at least usually)               
		x = _dm[varToBin].mean()
		
		
		lY.append(y)
		lX.append(x)
		
	# Plot:
	fig = plt.figure()
	figName = "004B: Effect size (%s - %s) as a function of binned %s - dv = %s trim = %s driftCorr = %s"\
		%(levelList[1],levelList[0],varToBin, dv, trim, driftCorr)
	plt.suptitle(figName)

	plt.ylabel("Effect size (%s-%s) in ms (dv = %s)"%(levelList[1], levelList[0], dv))
	plt.xlabel("Binned %s in ms"%varToBin)
	color = "#729FCF"

	plt.plot(lX, lY, marker = "o", linewidth = "2", color = color)
	plt.axhline(0, color = "#555753", linestyle = "--")
	
	if saveFig:
		if fileName == None:
			plt.savefig(os.path.join(dst,"%s%s" % (figName, saveExt)))
		else:
			plt.savefig("%s%s" % (fileName, saveExt))
	if showFig:
		plt.show()

def binAnalysesSepLines(dm, dv, varToBin, factor, subjectID = "file",
		nBin = 10, saveFig = True, showFig = False, saveExt = ".jpg", 
		fileName = None, trim = True, colList = \
		["#f57900","#73d216", "#3465a4", "#ef2929"]):
	
	"""
	Plots effect size of a given dv as a function of a given binned dv. NOTE that
	here a given effect (e.g. left vs right) is not a difference score, but 
	just two lines
	
	Arguments:
	dm 			--- experiment
	dv
	varToBin
	factor		
	
	
	Keyword arguments:
	nBin 		--- number of bins. Default = 10
	saveFig		--- Boolean indicating whether or not to save the figure.
					Default = True.
	showFig 		--- 
	saveExt		--- Default = .svg
	trim
	"""
	
	# Check whether 'factor' and 'dv' are column headers in the spread sheet:
	colList = colList[:]
	
	vNames = dm.asArray()[0]
	
	if not dv in vNames:
		msg.userMsg.userMsg("The dv %s is not a column header."%dv,\
			factor, __file__)
		return
	
	if not dv in vNames:
		msg.userMsg.userMsg("The factor %s is not a column header."%factor,\
			factor, __file__)
		return
	
	if not dv in vNames:
		msg.userMsg.userMsg("The varToBin %s is not a column header."%varToBin,\
			factor, __file__)
		return

	driftCorr = dm["driftCorr"][0]

	levelList = np.unique(dm[factor])
	
	# Difference scores can only be calculated when the factor has only two 
	# levels, e.g. congr, incongr.
	#if len(levelList) > 2:
	#	msg.userMsg.userMsg("The factor %s has more than two levels.",__file__)
	#	return

	if trim:
		dm = dm.selectByStdDev(keys = [factor, subjectID], dv = dv)
	
	
	
	binID = '%sBin'%varToBin
	binKeys = [subjectID, factor] # Bin by subject and condition

	dm = dm.addField(binID)
	dm = dm.calcPerc(varToBin, binID, keys=binKeys, nBin=nBin)

	# Plot:
	fig = plt.figure()
	figName = "004B: %s as a function of %s and binned %s - trim = %s driftCorr = %s"\
		%(dv,factor, varToBin, trim, driftCorr)
	plt.suptitle(figName)

	plt.ylabel("%s" % dv)
	plt.xlabel("Binned %s in ms"%varToBin)


	for lvl in levelList:
		col = colList.pop()
		lY = []
		lX = []
		# Walk through all bins
		for _bin in dm.unique(binID):  
			# Filter out all but one bin
			_dm = dm.select('%s == %f' % (binID, _bin))
				
			# Get the mean for both conditions. Note that using this method, the mean
			# is across all subjects, and not the mean of the mean of the subjects.
			# But this will not make any real difference for the overall pattern. You
			# can prevent this by withinizing the data first.
			y = _dm.select('%s == "%s"'%(factor, lvl),\
				verbose=False)[dv].mean()
		
			x = _dm[varToBin].mean()
		
			lY.append(y)
			lX.append(x)

		plt.plot(lX, lY, marker = "o", linewidth = "2", color = col)
	
	plt.axhline(0, color = "#555753", linestyle = "--")
	
	if factor == "mask_side":
		if "control" in np.unique(dm["mask_side"]):
			legendLabels = ["control", "more contrast right", "more contrast left"]
		else:
			legendLabels = ["more contrast right", "more contrast left"]
	else:
		legendLabels = levelList
	plt.legend(legendLabels)
	if saveFig:
		if fileName == None:
			plt.savefig(os.path.join(dst,"%s%s" % (figName, saveExt)))
		else:
			plt.savefig("%s%s" % (fileName, saveExt))
	if showFig:
		plt.show()

def binAnalysesTwoFactors(dm, dv, varToBin, factor, subjectID = "file",
		nBin = 10, saveFig = True, showFig = False, saveExt = ".jpg", 
		fileName = None, trim = True, colList = \
		["#f57900","#73d216", "#3465a4", "#ef2929"]):
	
	"""
	Plots effect size of a given dv as a function of a given binned dv. NOTE that
	here a given effect (e.g. left vs right) is not a difference score, but 
	just two lines
	
	Arguments:
	dm 			--- experiment
	dv
	varToBin
	factor		
	
	
	Keyword arguments:
	nBin 		--- number of bins. Default = 10
	saveFig		--- Boolean indicating whether or not to save the figure.
					Default = True.
	showFig 		--- 
	saveExt		--- Default = .svg
	trim
	"""
	
	# Check whether 'factor' and 'dv' are column headers in the spread sheet:
	colList = colList[:]
	
	vNames = dm.asArray()[0]
	
	driftCorr = dm["driftCorr"][0]
	
	if not dv in vNames:
		msg.userMsg.userMsg("The dv %s is not a column header."%dv,\
			factor, __file__)
		return
	
	if not dv in vNames:
		msg.userMsg.userMsg("The factor %s is not a column header."%factor,\
			factor, __file__)
		return
	
	if not dv in vNames:
		msg.userMsg.userMsg("The varToBin %s is not a column header."%varToBin,\
			factor, __file__)
		return

	levelList = np.unique(dm[factor])
	
	# Difference scores can only be calculated when the factor has only two 
	# levels, e.g. congr, incongr.
	if len(levelList) > 2:
		msg.userMsg.userMsg("The factor %s has more than two levels.",__file__)
		return

	if trim:
		dm = dm.selectByStdDev(keys = [factor, subjectID], dv = dv)
	
	
	
	binID = '%sBin'%varToBin
	binKeys = [subjectID, factor] # Bin by subject and condition

	dm = dm.addField(binID)
	dm = dm.calcPerc(dv, binID, keys=binKeys, nBin=nBin)

	# Plot:
	fig = plt.figure()
	figName = "004B: Effect size (%s - %s) as a function of binned %s - trim = %s driftCorr = %s"\
		%(levelList[1],levelList[0],dv, trim, driftCorr)
	plt.suptitle(figName)

	plt.ylabel("Effect size in ms")
	plt.xlabel("Binned %s in ms"%dv)


	for lvl in levelList:
		col = colList.pop()
		lY = []
		lX = []
		# Walk through all bins
		for _bin in dm.unique(binID):  
			# Filter out all but one bin
			_dm = dm.select('%s == %f' % (binID, _bin))
				
			# Get the mean for both conditions. Note that using this method, the mean
			# is across all subjects, and not the mean of the mean of the subjects.
			# But this will not make any real difference for the overall pattern. You
			# can prevent this by withinizing the data first.
			y = _dm.select('%s == "%s"'%(factor, lvl),\
				verbose=False)[dv].mean()
		
			x = _dm[varToBin].mean()
		
		
			lY.append(y)
			lX.append(x)
		plt.plot(lX, lY, marker = "o", linewidth = "2", color = col)
	
	plt.axhline(0, color = "#555753", linestyle = "--")
	plt.legend(levelList)
	if saveFig:
		if fileName == None:
			plt.savefig(os.path.join(dst,"%s%s" % (figName, saveExt)))
		else:
			plt.savefig("%s%s" % (fileName, saveExt))
	if showFig:
		plt.show()

	
if __name__ == "__main__":
	
	pass