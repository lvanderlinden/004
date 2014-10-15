#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: analyse.py

"""
Landing positions as a function of object orientation (across and
per 'object group').

ANOVA's
Bin analyses
"""

def _import():
	
	"""
	"""
	
	pass
	
# Import Python modules:
import numpy as np
import os
import sys
from matplotlib import pyplot as plt

# Import own modules:
from exparser.DataMatrix import DataMatrix
from exparser.PivotMatrix import PivotMatrix
from exparser.AnovaMatrix import AnovaMatrix
import getDM

def perSaccPerObject(addExp2 = True, trim = True, spacing = .5, addSimulation = True, \
		exclOverlap = True):
	
	"""
	Landing position as a funciton of orientation, across or per object stimulus.
	
	Arguments:
	
	Keyword arguments:
	addExp2			--- Add experiment 004B. Default = True
	trim			--- 
	perGroup		---
	"""

	
	fig = plt.figure()
	plt.subplots_adjust(wspace = .5)
	#fig = plt.figure(figsize = (10,10))
	title = "Average towards-handle landings per stimulus exclOverlap = %s" % exclOverlap
	plt.suptitle(title)
	
	
	# Exp 1:
	dm1 = getDM.getDM(exp = "004A", excludeErrors = True, driftCorr = True)
	
	subPlot = 1
	
	for stim in dm1.unique("object"):

		# New subplot:
		plt.subplot(2,7,subPlot)
		#plt.title(stim)
		_dm1 = dm1.select("object == '%s'" % stim)

		lLandingsAbs = []
		lLandingsCorr = []
		
		for sacc in ["1", "2", "3"]:
			
			# This is the same for corrected landing positions (the saccade
			# doesn't change; only the reference point does)
			_dm = _dm1.select("endX%sNorm != ''" % sacc)
			_dm = _dm.select("endX%sNorm > -.5" % sacc)
			_dm = _dm.select("endX%sNorm < .5" % sacc)
			
			if trim:
				_dmAbs = _dm.selectByStdDev(keys = ["file"], dv = "endX%sNormToHandle" % sacc)
				_dmCorr = _dm.selectByStdDev(keys = ["file"], dv = "endX%sCorrNormToHandle" % sacc)
			
			# Determine avg landing position:
			avgAbs = _dmAbs["endX%sNormToHandle" % sacc].mean()
			avgCorr = _dmCorr["endX%sCorrNormToHandle" % sacc].mean()
			
			# TODO: determine error bars:
			
			
			lLandingsAbs.append(avgAbs)
			lLandingsCorr.append(avgCorr)
		
		plt.plot(lLandingsAbs, color = "#f57900", linewidth = 2, marker = "o")
		plt.plot(lLandingsCorr, color = "#73d216", linewidth = 2, marker = "o")
		plt.ylabel(stim)
		
		# The other 2 experiments can be treated equally:
		colList = ["#ef2929", "#3465a4"]
		
		for exp in ["004B", "004C"]:
			
			if not addExp2:
				if exp == "004B":
					continue
			if not addSimulation:
				if exp == "004C":
					continue

			dm = getDM.getDM(exp = exp, excludeErrors = True, driftCorr = True)
			_dm = dm.select("object == '%s'" % stim)
			
			if exp == "004C":
				if exclOverlap:
					_dm = _dm.select("gap == 'zero'")
			
			lLandingsAbs = []
			
			for sacc in ["1", "2", "3"]:
				
				# TODO: how to filter only on-object saccades exp 2??
				sacc_dm = _dm.select("endX%sNorm != ''" % sacc)
				sacc_dm = sacc_dm.select("endX%sNorm > -.5" % sacc)
				sacc_dm = sacc_dm.select("endX%sNorm < .5" % sacc)
				
				if trim:
					sacc_dm = sacc_dm.selectByStdDev(keys = ["file"], dv = "endX%sNormToHandle" % sacc)
				
				# Determine avg landing position:
				avgAbs = sacc_dm["endX%sNormToHandle" % sacc].mean()
				
				# TODO: determine error bars:
				
				lLandingsAbs.append(avgAbs)
			col = colList.pop()
			plt.plot(lLandingsAbs, color = col, linewidth = 2, marker = "o")
			
		# Modify plot:
		#plt.legend(["Exp1 abs", "Exp1 corr", "Exp2", "Sim"])
			
		plt.axhline(0, color = "#888a85", linestyle = "--", linewidth = 2)
		xLabels = ["sacc 1", "sacc 2", "sacc 3"]
		xTicks = range(0,3)
		#plt.xticks(xTicks, xLabels, rotation = .5)
		plt.ylim([-.5, .5])
		plt.yticks([])
		plt.xticks([])
		plt.xlim(min(xTicks)-spacing, max(xTicks)+spacing)
		
		subPlot +=1
		
	plt.savefig("%s.png" % title)

def perSaccPerGroup(addExp2 = True, trim = True, spacing = .5, addSimulation = True, \
		exclOverlap = True):
	
	"""
	Landing position as a funciton of orientation, across or per object group.
	
	Arguments:
	
	Keyword arguments:
	addExp2			--- Add experiment 004B. Default = True
	trim			--- 
	perGroup		---
	"""

	fig = plt.figure(figsize = (10,10))
	title = "Average towards-handle landings per group - exclOverlap = %s" % exclOverlap
	plt.title(title)
	
	
	# Exp 1:
	dm1 = getDM.getDM(exp = "004A", excludeErrors = True, driftCorr = True)
	
	
	subPlot = 1
	
	for group in dm1.unique("corrDirection"):

		# New subplot:
		plt.subplot(1,2,subPlot)
		plt.title(group)
		_dm1 = dm1.select("corrDirection == '%s'" % group)

		lLandingsAbs = []
		lLandingsCorr = []
		
		for sacc in ["1", "2", "3"]:
			
			# This is the same for corrected landing positions (the saccade
			# doesn't change; only the reference point does)
			_dm = _dm1.select("endX%sNorm != ''" % sacc)
			_dm = _dm.select("endX%sNorm > -.5" % sacc)
			_dm = _dm.select("endX%sNorm < .5" % sacc)
			
			if trim:
				_dmAbs = _dm.selectByStdDev(keys = ["file"], dv = "endX%sNormToHandle" % sacc)
				_dmCorr = _dm.selectByStdDev(keys = ["file"], dv = "endX%sCorrNormToHandle" % sacc)
			
			# Determine avg landing position:
			avgAbs = _dmAbs["endX%sNormToHandle" % sacc].mean()
			avgCorr = _dmCorr["endX%sCorrNormToHandle" % sacc].mean()
			
			# TODO: determine error bars:
			
			
			lLandingsAbs.append(avgAbs)
			lLandingsCorr.append(avgCorr)
		
		plt.plot(lLandingsAbs, color = "#f57900", linewidth = 2, marker = "o")
		plt.plot(lLandingsCorr, color = "#73d216", linewidth = 2, marker = "o")
		
		# The other 2 experiments can be treated equally:
		colList = ["#ef2929", "#3465a4"]
		
		for exp in ["004B", "004C"]:
			
			if not addExp2:
				if exp == "004B":
					continue
			if not addSimulation:
				if exp == "004C":
					continue

			dm = getDM.getDM(exp = exp, excludeErrors = True, driftCorr = True)
			_dm = dm.select("corrDirection == '%s'" % group)

			if exp == "004C":
				if exclOverlap:
					_dm = _dm.select("gap == 'zero'")

			
			lLandingsAbs = []
			
			for sacc in ["1", "2", "3"]:
				
				# TODO: how to filter only on-object saccades exp 2??
				sacc_dm = _dm.select("endX%sNorm != ''" % sacc)
				sacc_dm = sacc_dm.select("endX%sNorm > -.5" % sacc)
				sacc_dm = sacc_dm.select("endX%sNorm < .5" % sacc)
				
				if trim:
					sacc_dm = sacc_dm.selectByStdDev(keys = ["file"], dv = "endX%sNormToHandle" % sacc)
				
				# Determine avg landing position:
				avgAbs = sacc_dm["endX%sNormToHandle" % sacc].mean()
				
				# TODO: determine error bars:
				
				lLandingsAbs.append(avgAbs)
			col = colList.pop()
			plt.plot(lLandingsAbs, color = col, linewidth = 2, marker = "o")
			
		# Modify plot:
		plt.legend(["Exp1 abs", "Exp1 corr", "Exp2", "Sim"])
			
		plt.axhline(0, color = "#888a85", linestyle = "--", linewidth = 2)
		xLabels = ["sacc 1", "sacc 2", "sacc 3"]
		xTicks = range(0,3)
		plt.xticks(xTicks, xLabels, rotation = .5)
		plt.ylim([-.5, .5])
		plt.xlim(min(xTicks)-spacing, max(xTicks)+spacing)
		
		subPlot +=1
		
	plt.savefig("%s.png" % title)


def perSaccAcrossGroups(addExp2 = True, trim = True, spacing = .5, \
		addSimulation = True, exclOverlap = True, exclY = True):
	
	"""
	Landing position as a funciton of orientation, across or per object group.
	
	Arguments:
	
	Keyword arguments:
	addExp2			--- Add experiment 004B. Default = True
	trim			--- 
	perGroup		---
	"""
	
	fig = plt.figure(figsize = (5,10))
	title = "Average towards-handle landings across groups - exclOverlap = %s - exclY = %s" % (exclOverlap, exclY)
	plt.suptitle(title)
	
	# The first experiment has to be treated differently, because
	# it contains two dependent variables: absolute and corrected
	dm1 = getDM.getDM(exp = "004A", excludeErrors = True, driftCorr = True)
	lLandingsAbs = []
	lLandingsCorr = []
	
	for sacc in ["1", "2", "3"]:
		
		# This is the same for corrected landing positions (the saccade
		# doesn't change; only the reference point does)
		_dm = dm1.select("endX%sNorm != ''" % sacc)
		_dm = _dm.select("endX%sNorm > -.5" % sacc)
		_dm = _dm.select("endX%sNorm < .5" % sacc)
		
		if exclY:
			_dm = _dm.select("endY%sNorm != ''" % sacc)
			_dm = _dm.select("endY%sNorm > -.5" % sacc)
			_dm = _dm.select("endY%sNorm < .5" % sacc)
		
		
		if trim:
			_dmAbs = _dm.selectByStdDev(keys = ["file"], dv = "endX%sNormToHandle" % sacc)
			_dmCorr = _dm.selectByStdDev(keys = ["file"], dv = "endX%sCorrNormToHandle" % sacc)
		
		# Determine avg landing position:
		avgAbs = _dmAbs["endX%sNormToHandle" % sacc].mean()
		avgCorr = _dmCorr["endX%sCorrNormToHandle" % sacc].mean()
		
		# TODO: determine error bars:

		lLandingsAbs.append(avgAbs)
		lLandingsCorr.append(avgCorr)
	
	plt.plot(lLandingsAbs, color = "#f57900", linewidth = 2, marker = "o")
	plt.plot(lLandingsCorr, color = "#73d216", linewidth = 2, marker = "o")
	
	# The other 2 experiments can be treated equally:
	colList = ["#ef2929", "#3465a4"]

	for exp in ["004B", "004C"]:
		
		continue
		
		if not addExp2:
			if exp == "004B":
				continue
		if not addSimulation:
			if exp == "004C":
				continue

		dm = getDM.getDM(exp = exp, excludeErrors = True, driftCorr = True)
		
		if exp == "004C":
			print 'xxx'
			if exclOverlap:
				dm = dm.select("gap == 'zero'")

		lLandingsAbs = []
		
		for sacc in ["1", "2", "3", '4']:
			
			# TODO: how to filter only on-object saccades exp 2??
			_dm = dm.select("endX%sNorm != ''" % sacc)
			_dm = _dm.select("endX%sNorm > -.5" % sacc)
			_dm = _dm.select("endX%sNorm < .5" % sacc)
			
			if exclY:
			
				_dm = _dm.select("endY%sNorm != ''" % sacc)
				_dm = _dm.select("endY%sNorm > -.5" % sacc)
				_dm = _dm.select("endY%sNorm < .5" % sacc)

			if trim:
				_dm = _dm.selectByStdDev(keys = ["file"], dv = "endX%sNormToHandle" % sacc)
			
			# Determine avg landing position:
			avgAbs = _dm["endX%sNormToHandle" % sacc].mean()
			lLandingsAbs.append(avgAbs)
			
			
		col = colList.pop()
		plt.plot(lLandingsAbs, color = col, linewidth = 2, marker = "o")
	
	# Modify plot:
	plt.legend(["Exp1 abs", "Exp1 corr", "Exp2", "Sim"])
		
	plt.axhline(0, color = "#888a85", linestyle = "--", linewidth = 2)
	xLabels = ["sacc 1", "sacc 2", "sacc 3"]
	xTicks = range(0,3)
	plt.xticks(xTicks, xLabels, rotation = .5)
	plt.xlim(min(xTicks)-spacing, max(xTicks)+spacing)
	
	plt.ylim([-.5, .5])
	
	plt.savefig("%s.png" % title)

def contrastSide(trim = True, exclOverlap = False, exclY = True):
	
	"""
	Landing position as a function of contrast.
	
	Positive values indicate landing position to the right,
	negative values indicate landing pos to the left
	
	NOTE: be careful with using --shortcut, because
	for the contrast analyses the contrast manipulations
	should not be excluded.
	
	TODO: make a ToContrast variable, such that we have more observations
	per cell and can do the on-object filter on the y axis as well?
	The disadvantage is that we can't use the no-contrast-trials in this case
	#(because 'ToContrast' should be a difference score between two bins).
	"""
	
	fig = plt.figure()
	title = "Effect of contrast - exclOverlap = %s - exclY = %s" % (exclOverlap, exclY)
	plt.suptitle(title)
	
	for sacc in ["1", "2", "3"]:
		
		colList = ["#ef2929", "#3465a4","#73d216", "#f57900"]
		plt.subplot(1,3, int(sacc))
		plt.title("sacc = %s"% (sacc))
		
		# Exp 1:
		exp = "004A"
		dm1 = getDM.getDM(exp = exp, driftCorr = True, onlyControl = False)

		# This is the same for corrected landing positions (the saccade
		# doesn't change; only the reference point does)
		dm1 = dm1.select("endX%sNorm != ''" % sacc, verbose = False)
		dm1 = dm1.select("endX%sNorm > -.5" % sacc, verbose = False)
		dm1 = dm1.select("endX%sNorm < .5" % sacc, verbose = False)
		
		if exclY:
			dm1 = dm1.select("endY%sNorm != ''" % sacc)
			dm1 = dm1.select("endY%sNorm > -.5" % sacc)
			dm1 = dm1.select("endY%sNorm < .5" % sacc)
			
		for dv in ["endX%sNorm" % sacc, "endX%sCorrNorm" % sacc]:
			
			#If wanted, trim the data
			if trim:
				_dm1 = dm1.selectByStdDev(keys = ["contrast_side", "file"], dv = dv)

			# For experiment 1 there are not enough third fixations anyway,
			# not even when not filtering on-object on the y-axis.
			if exp == "004A" and sacc == "3":
				
				colList = ["#ef2929", "#3465a4"]
				continue
			
			# Get pivot matrix:
			pm = PivotMatrix(_dm1, ["contrast_side"], ["file"], dv=dv, colsWithin=True)#, xLabels = ["left", "control", "right"])
			col = colList.pop()
			pm.plot(fig = fig, nLvl1 = 1, colors = [col])

		# Experiment 2 and 3:
		dv = "endX%sNorm" % sacc
		
		for exp in ["004B", "004C"]:
			if exclY and exp == "004B" and sacc == "3":
				colList = ["#ef2929"]
			   
				continue
			
			if exp == "004C" and exclOverlap:
				dm = dm.select("gap == 'zero'")
			
			print "EXP = ", exp
			
			dm = getDM.getDM(exp = exp, driftCorr = True, onlyControl = False)
			
			# This is the same for corrected landing positions (the saccade
			# doesn't change; only the reference point does)
			dm = dm.select("endX%sNorm != ''" % sacc, verbose = False)
			dm = dm.select("endX%sNorm > -.5" % sacc, verbose = False)
			dm = dm.select("endX%sNorm < .5" % sacc, verbose = False)
			
			if exclY:
				dm = dm.select("endY%sNorm != ''" % sacc)
				dm = dm.select("endY%sNorm > -.5" % sacc)
				dm = dm.select("endY%sNorm < .5" % sacc)

			
			#If wanted, trim the data
			if trim:
				_dm = dm.selectByStdDev(keys = ["contrast_side", "file"], dv = dv)
			# Get pivot matrix:
			pm = PivotMatrix(_dm, ["contrast_side"], ["file"], dv=dv, colsWithin=True)
			col = colList.pop()
			pm.plot(fig = fig, nLvl1 = 1, colors = [col])
		
		# Modify plot:
		plt.ylim(-.2, .2)
		
		plt.legend(["Exp1 (abs)", "Exp1 (corr)", "Exp2 (abs)", "Exp2 (sim)"])
		if sacc == "3":
			plt.legend(["Exp2 (abs)", "Exp2 (sim)"])
			if exclY:
				plt.legend(["Exp2 (sim)"])
		
		plt.axhline(0, color = "#888a85", linestyle = "--", linewidth = 2)
	
	plt.savefig("%s.png" % title)

def affordancePerSacc(trim = True, exclY = True, dv = "RT"):
	
	"""
	"""


	fig = plt.figure()
	title = "Affordance effect per sacc - dv = %s" % dv
	plt.suptitle(title)
	plotNr = 1
	
	for exp in ["004A", "004B"]:
		
		colList = ["red", "blue"]
	
		plt.subplot(1,2,plotNr)
		
		plt.title("Exp = %s" % exp)
		
		dm = getDM.getDM(exp)
	
		for sacc in ["1", "2"]:
			
			# Only on-object saccades:
			_dm = onObject.onObject(dm, sacc)
			
			trimmed_dm = _dm.selectByStdDev(keys =["comp", "file"], dv = dv)
		
		
			for val in trimmed_dm.unique("comp"):
				print val
				print trimmed_dm["RT"][trimmed_dm.where("comp == '%s'" % val)].mean()
			
			pm = PivotMatrix(trimmed_dm, ["comp"], ["file"], dv = dv, colsWithin = True)
			
			am = AnovaMatrix(trimmed_dm, ["comp"], dv = dv, \
				subject = "file")._print(ret=True)

			print am
			
			col = colList.pop()
			pm.plot(nLvl1=1, fig = fig, colors = [col])
			plt.show()
		plt.legend(["data sacc 1", "data sacc 2"])
		plotNr +=1
			
	plt.show()
	
def affordances(trim = True, exclY = True, dv = "RT"):
	
	"""
	"""

	fig = plt.figure()
	title = "Affordance effect per Exp"
	plt.suptitle(title)
	plotNr = 1
	
	for exp in ["004A", "004B"]:
		
		plt.subplot(1,2,plotNr)
		
		plt.title("Exp = %s" % exp)
		
		dm = getDM.getDM(exp)
		
		trimmed_dm = dm.selectByStdDev(keys =["handle_side", "response_hand", "file"], dv = dv)

		for val in trimmed_dm.unique("comp"):
			print val
			print trimmed_dm["RT"][trimmed_dm.where("comp == '%s'" % val)].mean()

		pm = PivotMatrix(trimmed_dm, ["handle_side", "response_hand"], ["file"], dv = dv, colsWithin = True)
		pm.linePlot(fig = fig)
		plt.show()


		pm = PivotMatrix(trimmed_dm, ["comp"], ["file"], dv = dv, colsWithin = True)
		pm.plot(nLvl1 = 1, fig = fig)
		plt.show()
		

		plotNr +=1
		
		###am = AnovaMatrix(trimmed_dm, ["comp"], dv = dv, \
			###subject = "file")._print(ret=True)

		###print am
		
			
	plt.show()
	
def timeCourse(direction = "ToHandle", cousineau = True,nBin = 8,trim = False, \
		usePm = True, yLim = [-.25,.25], onlyExp2 = False, exclY = True):

	"""
	"""
	
	if direction != "ToHandle":
		print "Only ToHandle at the moment!!"
		return

	titleList = ["Exp1: relative to center", "Exp1: relative to CoG", \
		"Exp2: relative to CoG"]

	fig = plt.figure(figsize = (9,7))
	
	title = "Time course per saccade - cousineau = %s trim = %s - exclY = %s" % \
		(direction, cousineau,exclY)
	plt.title(title)
			
	nRows = 1
	nCols = 3
	plotNr = 0
	
	for exp in ["004A", "004B"]:
		
		if exp == "004A":
			corrList = ["uncorrected", "corrected"]
		if exp == "004B":
			corrList = ["uncorrected"]
		
		for corr in corrList:
			subTitle = titleList[plotNr]
			
			plotNr +=1
			
			colList = [["#f57900"], ["#73d216"], ["#3465a4"]]
			
			for sacc in ["1", "2", "3"]:
				
				dm = getDM.getDM(exp = exp)
				
				#if sacc == "3":
				#	continue
				
				if sacc== "1":
					nBin = 3
				if sacc== "2":
					nBin = 3
				if sacc== "3":
					nBin = 2
					if exp == "004B":
						nBin = 1
				
				print '\n\tsacc count = %s\n' % sacc
				
				if corr == "uncorrected":
					dv = "endX%sNorm%s"%(sacc, direction)
				elif corr == "corrected":
					dv = "endX%sCorrNorm%s"%(sacc, direction)
					
				print "\tDV = %s\n" % dv

				# This is the same for corrected landing positions (the saccade
				# doesn't change; only the reference point does)
				dm = dm.select("endX%sNorm != ''" % sacc)
				dm = dm.select("endX%sNorm > -.5" % sacc)
				dm = dm.select("endX%sNorm < .5" % sacc)
		
				if exclY:
					dm = dm.select("endY%sNorm != ''" % sacc)
					dm = dm.select("endY%sNorm > -.5" % sacc)
					dm = dm.select("endY%sNorm < .5" % sacc)
				
				saccLat = "saccLat%s" % sacc
				
				# Trim the data matrix such that the most extreme latencies are excluded:
				if trim:
					_dm = dm.selectByStdDev(keys = ["file"], dv = saccLat, verbose = False)
				else:
					_dm = dm
				
				# Withinize sacc latencies, if wanted:
				print "\n\tcousineau = %s\n" % cousineau
				if cousineau:
					
					_dm = _dm.addField("cousineau_%s"%saccLat, dtype = None)
					_dm = _dm.withinize(saccLat, "cousineau_%s"%saccLat, "file", verbose = False, whiten=False)
					saccLat = "cousineau_%s"%saccLat
					
				col = colList.pop()

				# Make bins, only for the first dv (for the second dv, the binned variable is the same and
				# therefore already exists:
				varToBin = saccLat
				binnedVar = "binnend%s" % varToBin
				binned_dm = _dm.addField(binnedVar)
				binned_dm = binned_dm.calcPerc(varToBin, binnedVar ,keys = ["file"], nBin = nBin)
				
				# Disadvantages of pm: 
					# - There SHOULD be enough observations per participant to be able to plot
					# - bin number (instead of bin mean) on x axis
				plt.subplot(nRows,nCols,plotNr)
				plt.title(subTitle)
				pm = PivotMatrix(binned_dm, binnedVar, "file", dv, colsWithin = True, err = 'se')
				pm.plot(nLvl1=1, fig = fig, colors = col)
			
			if plotNr != "1":
				plt.yticks([])
			plt.xticks([])
			plt.ylim(yLim)
			plt.legend(["initial saccade", "refixation 1", "refixation 2"])
			plt.axhline(0, color = "#555753", linestyle = "--", linewidth = 2)
		#plt.show()
	plt.savefig(os.path.join('%s.png' % title))
	plt.savefig(os.path.join('%s.svg' % title))
	
def perHandle(trim = True, exclY = True):
	
	"""
	"""
	
	fig = plt.figure()
	title = "Per handle side - exclY = %s" % exclY
	
	for sacc in ["1", "2", "3"]:
		
		if sacc == "3":
			continue
		colList = ["#3465a4","#73d216", "#f57900"]
		
		plt.subplot(1,3,int(sacc))
		for exp in ["004A", "004B"]:
			
			dm = getDM.getDM(exp = exp)
			
			# Only include on-object saccades:
			dm = dm.select("endX%sNorm != ''" % sacc)
			dm = dm.select("endX%sNorm > -.5" % sacc)
			dm = dm.select("endX%sNorm < .5" % sacc)
			
			if exclY:
				dm = dm.select("endY%sNorm != ''" % sacc)
				dm = dm.select("endY%sNorm > -.5" % sacc)
				dm = dm.select("endY%sNorm < .5" % sacc)
			
			if exp == "004A":
				dvList = ["endX%sNorm" % sacc, "endX%sCorrNorm" % sacc]
			else:
				dvList = ["endX%sNorm" % sacc]
				
				for dv in dvList:
					
					print dv
					
					if trim:
						dm = dm.selectByStdDev(keys = ["file"], dv = dv)
					
					pm = PivotMatrix(dm, ["handle_side"], ["file"], dv=dv, colsWithin=True)
					pm._print()
					sys.exit()
					col = colList.pop()
					pm.plot(nLvl1 = 1,fig = fig, colors = [col])
		# Modify plot:
		plt.xlabel("handle side")
		plt.ylabel("normalised landing position")
		plt.axhline(0, linestyle = "--", color = "#888a85")
		
	plt.savefig("%s.png" % title)
	
	


if __name__ == "__main__":
	
	def run():
		
		pass
	
	#perHandle()
	# Affordance effects:
	perSaccAcrossGroups()
	#affordancePerSacc()
	#timeCourse()
	#for excl in [True, False]:
	#	for y in [True, False]:
	#	
	#		contrastSide(exclOverlap = excl, exclY = y)
		
		#perSaccPerObject(exclOverlap = excl)
		#perSaccPerGroup(exclOverlap = excl)
		#perSaccAcrossGroups(exclY = excl)