#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: plotsEBR.py

"""
Plots for manuscript.
"""

src = "/home/lotje/Documents/PhD Marseille/Studies/004 - Single-object experiment - Handle-orientation effect/analysis/plots manuscript EBR"

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

plt.rc("font", family="Liberation Sans")
plt.rc("font", size=12)
	


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


def perSacc(addExp1 = True, addExp2 = True, trim = True, spacing = .5, \
		addSimulation = True, exclOverlap = True, exclY = True, \
		singleCol = "black", singleLineWidth = 1, markerExp1 = 'o', \
		markerExp2 = '^', yLim = [-.25, .25], hLineStyle = ':',\
		figSize = (5,8)):
	
	"""
	Landing position as a funciton of orientation, across or per object group.
	
	Arguments:
	
	Keyword arguments:
	addExp2			--- Add experiment 004B. Default = True
	trim			--- 
	perGroup		---
	"""
	
	alphaExp1 = 1
	alphaExp2 = 1
	if not addExp2 and not addSimulation:
		title = "Figure 1"
		lLegends = ["exp1: relative to center", "exp1: to relative CoG"]
	if addExp2 and not addSimulation:
		title = "Figure 2"
		lLegends = ["exp1: relative to center", "exp1: relative CoG", \
			"exp2: relative to CoG"]
		alphaExp1 = .3
		
	if addExp2 and addSimulation:
		title = "Figure 3"
		lLegends = ["exp1: relative to center", "exp1: relative CoG", \
			"exp2: relative to CoG", "exp3: simulation"]
		alphaExp1 = .3
		alphaExp2 = .3
		
	xLabels = ["1", "2", "3"]
	xLabel = "saccade count"

	fig = plt.figure(figsize = figSize)
	
	if addExp1:
		
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
				_dmAbs = _dm.selectByStdDev(keys = ["file"], \
					dv = "endX%sNormToHandle" % sacc)
				_dmCorr = _dm.selectByStdDev(keys = ["file"], \
					dv = "endX%sCorrNormToHandle" % sacc)
			
			# Determine avg landing position:
			avgAbs = _dmAbs["endX%sNormToHandle" % sacc].mean()
			avgCorr = _dmCorr["endX%sCorrNormToHandle" % sacc].mean()
			
			# TODO: determine error bars:

			lLandingsAbs.append(avgAbs)
			lLandingsCorr.append(avgCorr)
		
		plt.plot(lLandingsAbs, color = singleCol, linewidth = \
			singleLineWidth, marker = markerExp1, alpha = alphaExp1)
		plt.plot(lLandingsCorr, color = singleCol, linestyle = '--', \
			linewidth = singleLineWidth, marker = markerExp1, \
				alpha = alphaExp1)
	
	# The other 2 experiments can be treated equally:
	colList = [singleCol, singleCol]

	for exp in ["004B", "004C"]:
		
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
		
		for sacc in ["1", "2", "3"]:
			
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
		if exp == "004B":
			lStyle = "-"
			alphaLvl = alphaExp2
		if exp == "004C":
			lStyle = "--"
			alphaLvl = 1
		plt.plot(lLandingsAbs, color = col, linewidth = singleLineWidth, \
			marker = markerExp2, linestyle = lStyle, alpha = alphaLvl)
	
	plt.legend(lLegends)
	plt.axhline(0, color = singleCol, linestyle = hLineStyle, linewidth = singleLineWidth)
	plt.xlabel(xLabel)
	xTicks = range(0,3)
	plt.xticks(xTicks, xLabels, rotation = .5)
	plt.xlim(min(xTicks)-spacing, max(xTicks)+spacing)
	
	plt.ylim(yLim)
	plt.ylabel("normalised landing positions")
	
	plt.savefig(os.path.join(src,"%s.png" % title))
	plt.savefig(os.path.join(src,"%s.svg" % title))
	
def contrastSide(trim = True, exclOverlap = False):
	
	"""
	Landing position as a function of contrast.
	
	Positive values indicate landing position to the right,
	negative values indicate landing pos to the left
	"""
	
	fig = plt.figure()
	title = "Effect of contrast - exclOverlap = %s" % exclOverlap
	plt.suptitle(title)
	
	for sacc in ["1", "2", "3"]:
		
		colList = ["#ef2929", "#3465a4","#73d216", "#f57900"]
		plt.subplot(1,3, int(sacc))
		plt.title("sacc = %s"% (sacc))
		
		# Exp 1:
		exp = "004A"
		dm_004A = getDM.getDM(exp = exp, driftCorr = True, onlyControl = False)

		# This is the same for corrected landing positions (the saccade
		# doesn't change; only the reference point does)
		dm_004A = dm_004A.select("endX%sNorm != ''" % sacc, verbose = False)
		dm_004A = dm_004A.select("endX%sNorm > -.5" % sacc, verbose = False)
		dm_004A = dm_004A.select("endX%sNorm < .5" % sacc, verbose = False)
			
		for dv in ["endX%sNorm" % sacc, "endX%sCorrNorm" % sacc]:
			
			#If wanted, trim the data
			if trim:
				_dm = dm_004A.selectByStdDev(keys = ["contrast_side", "file"], dv = dv)

			# For experiment 1 there are not enough third fixations:
			if exp == "004A" and sacc == "3":
				
				colList = ["#ef2929", "#3465a4"]
				continue
			
			# Get pivot matrix:
			pm = PivotMatrix(_dm, ["contrast_side"], ["file"], dv=dv, colsWithin=True)#, xLabels = ["left", "control", "right"])
			col = colList.pop()
			pm.plot(fig = fig, nLvl1 = 1, colors = [col])

		# Experiment 2 and 3:
		dv = "endX%sNorm" % sacc
		
		for exp in ["004B", "004C"]:
			
			if exp == "004C" and exclOverlap:
				dm = dm.select("gap == 'zero'")
			
			print "EXP = ", exp
			
			dm = getDM.getDM(exp = exp, driftCorr = True, onlyControl = False)
			
			# This is the same for corrected landing positions (the saccade
			# doesn't change; only the reference point does)
			dm = dm.select("endX%sNorm != ''" % sacc, verbose = False)
			dm = dm.select("endX%sNorm > -.5" % sacc, verbose = False)
			dm = dm.select("endX%sNorm < .5" % sacc, verbose = False)
			
			#If wanted, trim the data
			if trim:
				_dm = dm.selectByStdDev(keys = ["contrast_side", "file"], dv = dv)
			# Get pivot matrix:
			pm = PivotMatrix(_dm, ["contrast_side"], ["file"], dv=dv, colsWithin=True)
			col = colList.pop()
			pm.plot(fig = fig, nLvl1 = 1, colors = [col])
		
		# Modify plot:
		plt.ylim(-.2, .2)
		
		#if sacc == "1":
		plt.legend(["Exp1 (abs)", "Exp1 (corr)", "Exp2 (abs)", "Exp2 (sim)"])
		if sacc == "3":
			plt.legend(["Exp2 (abs)", "Exp2 (sim)"])
		
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
			
			_dm = dm.select("endX%sNorm != ''" % sacc)
			_dm = _dm.select("endX%sNorm > -.5" % sacc)
			_dm = _dm.select("endX%sNorm < .5" % sacc)

			if exclY:
				_dm = _dm.select("endY%sNorm != ''" % sacc)
				_dm = _dm.select("endY%sNorm > -.5" % sacc)
				_dm = _dm.select("endY%sNorm < .5" % sacc)
			
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
	
	

if __name__ == "__main__":
	
	def run():
		
		pass
	
	perSacc(addExp2 = False, addSimulation = False)
	perSacc(addSimulation = False)
	
	perSacc()
	sys.exit()
	affordancePerSacc()
	sys.exit()

	for excl in [True, False]:
		
		#contrastSide(exclOverlap = excl)
		
		#perSaccPerObject(exclOverlap = excl)
		#perSaccPerGroup(exclOverlap = excl)
		perSaccAcrossGroups(exclY = excl)