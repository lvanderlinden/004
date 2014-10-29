#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: sources.py

"""
Plots for manuscript.
"""

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

dst = "/home/lotje/Documents/PhD Marseille/Studies/004 - Single-object experiment - Handle-orientation effect/manuscript/sources"
	

# Import Python modules:
import numpy as np
import os
#import sys
from matplotlib import pyplot as plt

# Import own modules:
from exparser.DataMatrix import DataMatrix
from exparser.PivotMatrix import PivotMatrix
from exparser.AnovaMatrix import AnovaMatrix
import getDM
import onObject
import constants

def landOnHandle(trim = True, spacing = .5, exclOverlap = False, \
	exclY = False, yLim = [-.22, .15],\
		xLabels = ["1", "2", "3"], xTitle = "Saccade", \
		yTitle = "Normalised landings positions"):
	
	"""
	Landing position as a funciton of orientation, across or per object group.
	
	Arguments:
	
	Keyword arguments:
	trim			--- 
	exclOverlap		--- indicates whether or not to exclude gap-overlap trials
						in the simulation.
						
	# TODO: error bars, markers
	"""
	
	fig = plt.figure()#figsize = (5,10))
	title = "Average towards-handle landings - exclOverlap = %s - exclY = %s" \
		% (exclOverlap, exclY)
	#plt.suptitle(title)
	
	
	#colList = ["#ef2929", "#3465a4", "#f57900", "#73d216"],\
	#copyColList = ["#3465a4", "#f57900", "#73d216", "#73d216"]
	copyColList = ["#73d216","#f57900","#3465a4","#3465a4"]
	
	markerList = ["s","^","o", "o"]
	
	lLegend = ["Experiment 1 (relative to center)", "Experiment 1 (relative to CoG)", \
		"Experiment 2 (relative to CoG)", "Saliency-model simulation"]
	
	
	for exp in ["004A", "004B", "004C"]:
		
		#if exp != "004A":
			#continue
		
		dm = getDM.getDM(exp)
	
		if exp == "004A":
			dvList = ["abs", "corr"]
		else:
			dvList = ["abs"]
		
		for dvType in dvList:
			lMeans = []
			
			for sacc in ["1", "2", "3"]:
				
				if dvType == "corr":
					dv = "endX%sCorrNormToHandle" % sacc
				else:
					dv = "endX%sNormToHandle" % sacc
				
				# Only on-object saccades:
				on_dm = onObject.onObject(dm, sacc, exclY = exclY, verbose = False)
				
				print "DV = ", dv
				if trim:
					trim_dm = on_dm.selectByStdDev(keys = ["file"], dv = dv)
				else:
					trim_dm = on_dm
					
					
				# Determine avg landing position:
				m = trim_dm[dv].mean()
				lMeans.append(m)
			
			# Plot landing positions of all 3 saccadesL
			col = copyColList.pop()
			_marker = markerList.pop()
			if "Corr" in dv:
				lineStyle = "--"
			else:
				lineStyle = "-"
			plt.plot(lMeans, color = col, linewidth = 2, marker = _marker, linestyle = lineStyle)
	
	# Modify plot:
	plt.legend(lLegend)
	plt.axhline(0, color = "#888a85", linestyle = "--", linewidth = 2)
	xTicks = range(0,3)
	plt.xticks(xTicks, xLabels, rotation = .5)
	plt.xlabel(xTitle)
	plt.xlim(min(xTicks)-spacing, max(xTicks)+spacing)
	plt.ylim(yLim)	
	plt.ylabel(yTitle)
	
	for ext in [".png", ".svg"]:
		plt.savefig(os.path.join(dst, "Figure1%s" % ext))
		
def timeCourse(yLim = [-.25,.25], exclY = False, nRows = 1, nCols = 3, \
	colList = ["#ef2929", "#3465a4","#73d216", "#f57900"],\
	lLegend = ["exp1: relative to center", "exp1: relative to CoG",\
	"exp2: relative to CoG"], binMax = 10, binMin = 2):

	"""
	Time course per saccade
	"""
	
	if exclY:
		binMax = 3
		binMin = 1

	fig = plt.figure()#figsize = (9,7))
	
	plt.subplots_adjust(wspace = 0)
	
	title = "Time course per saccade - exclY = %s -binMax = %s binMin = %s" \
		% (exclY, binMax, binMin)
	#plt.suptitle(title)
	plotNr = 0

	
	lLegend = ["Experiment 1 (relative to center)", "Experiment 1 (relative to CoG)", \
		"Experiment 2 (relative to CoG)", "Saliency-model simulation"]
	

	dm_sim = getDM.getDM("004C")
	
	for sacc in ["1", "2", "3"]:
		plotNr +=1
		
		copyColList = ["#73d216","#f57900","#3465a4","#3465a4"]
		markerList = ["s","^","o", "o"]		

		sim_avg = dm_sim["endX%sNormToHandle" % sacc].mean()
		
		for exp in ["004A", "004B"]:
			if exp == "004A":
				dvList = ["endX%sNormToHandle" % sacc, "endX%sCorrNormToHandle" % sacc]
			else:
				dvList = ["endX%sNormToHandle" % sacc]

			for dv in dvList:

				if sacc== "1":
					nBin = binMax
				if sacc== "2":
					nBin = binMax
				if sacc== "3":
					nBin = binMin

				
				dm = getDM.getDM(exp = exp)
				#dm = dm.select("corrDirection == 'correction awayHandle'")
					
				# Only on-object:
				_dm = onObject.onObject(dm, sacc, exclY = exclY)
			
				# Make bins, only for the first dv (for the second dv, the binned 
				# variable is the same and therefore already exists:
				saccLat = "saccLat%s" % sacc
				varToBin = saccLat
				binnedVar = "binnend%s" % varToBin
				binned_dm = _dm.addField(binnedVar)
				binned_dm = binned_dm.calcPerc(varToBin, binnedVar ,keys = ["file"], nBin = nBin)
				
				plt.subplot(nRows,nCols,plotNr)
				col = copyColList.pop()
				plt.title("sacc = %s" % sacc)
				pm = PivotMatrix(binned_dm, binnedVar, "file", dv, colsWithin = True, err = 'se')
				pm.plot(nLvl1=1, fig = fig, colors = [col])
		
		# Modify plot:
		if sacc != "1":
			plt.yticks([])
		if sacc == "3":
			plt.legend(lLegend)
		else:
			plt.legend([])
		plt.xticks([])
		plt.ylim(yLim)
		
		# Indicate reference point:
		plt.axhline(0, color = "#555753", linestyle = "--", linewidth = 2)
		# Indicate saliency peak:
		plt.axhline(sim_avg, color = "#ef2929", linestyle = "--", linewidth = 2)

	for ext in [".png", ".svg"]:
		plt.savefig(os.path.join(dst, "Figure2%s" % ext))
		
if __name__ == "__main__":
	
	landOnHandle()
	timeCourse()