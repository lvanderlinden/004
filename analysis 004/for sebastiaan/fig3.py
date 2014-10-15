#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: fig2.py
"""
Created on Wed Jan 22 11:54:37 2014

@author: lotje

Fig 3:
- Distributional analysis first and second saccade
"""

# Import Python modules:
import numpy as np
import os
import sys
from matplotlib import pyplot as plt
import scipy.stats

# Import own modules:
from exparser.DataMatrix import DataMatrix
from exparser.PivotMatrix import PivotMatrix
from exparser.AnovaMatrix import AnovaMatrix
from exparser import Constants
import getDM
import onObject
import constants

# Boolean:

# Set font.
# For guidelines, see:
# http://www.journalofvision.org/site/misc/peer_review.xhtml#style
plt.rc("font", family="arial")
plt.rc("font", size=7)

# Some constant vars:
dst = "/home/lotje/Studies/004 - Single-object experiment - Handle-orientation effect/manuscript/Versions/5th draft/Figures JoV"

def fig3(trim, blinkRemov):
	
	"""
	"""

	fig = plt.figure(figsize = (3,3))
	plt.subplots_adjust(left=.2, bottom=.15)

	yLim = [-.21,.05]
	xTitle = "Saccade"
	yTitle = "Normalised landing position"
	
	#colList = ["#4e9a06", "#3465a4"]
	colList = ["#3465a4"]*2

	
	# Plot 3:
	dm = getDM.getDM(exp = "004B")
	
	xTitle = "Binned saccade latency"
	
	figName= "fig3_trim=%s_blinkRemov=%s" % (trim, blinkRemov)

	#lineStyles = ["-", "-"]
	lineStyles = ["-", "-"]
	
	markerColList = ["#3465a4", "white"]
	
	# Data processing:
	for sacc in ["1", "2"]:
		
		lX = []
		lY = []
		
		dv = "endX%sNormToHandle" % sacc
		nBin = 10
	
		#sim_avg = dm_sim["endX%sNormToHandle" % sacc].mean()
			
		# Only on-object:
		on_dm = onObject.onObject(dm, sacc)
		
		if blinkRemov:
			on_dm = on_dm.select("n_blink == 0")		

	
		# Trim on both variables:
		if trim:
			dm_trim1 = on_dm.selectByStdDev(["file"], dv)
			dm_trim1 = dm_trim1.removeField("__dummyCond__")
			dm_trim1 = dm_trim1.removeField("__stdOutlier__")
			dm_trim2 = dm_trim1.selectByStdDev(["file"], "saccLat%s" % sacc)
		else:
			dm_trim2 = on_dm
	
		# Make bins, only for the first dv (for the second dv, the binned 
		# variable is the same and therefore already exists:
		saccLat = "saccLat%s" % sacc
		varToBin = saccLat
		binnedVar = "binnend%s" % varToBin
		binned_dm = dm_trim2.addField(binnedVar)
		binned_dm = binned_dm.calcPerc(varToBin, binnedVar ,keys = ["file"], nBin = nBin)
		
		for _bin in binned_dm.unique(binnedVar):  
			# Filter out all but one bin
			_dm = binned_dm.select('%s == %f' % (binnedVar, _bin))
					
			x = _dm["saccLat%s"%sacc].mean()
			y = _dm["endX%sNormToHandle"%sacc].mean()
			
			# TODO: error bars
			lY.append(y)
			lX.append(x)		
		
		lineStyle = lineStyles.pop()
		#markerCol = colList.pop()
		#markerCol = "white"
		markerCol = markerColList.pop()
		col = colList.pop()
		plt.plot(lX,lY, color = col, marker = 'o', linestyle = lineStyle, \
			markerfacecolor=markerCol, markeredgecolor=col, \
			markeredgewidth=1)
			
	plt.xlabel(xTitle)
	plt.ylabel(yTitle)
	plt.ylim(yLim)
	plt.xlabel(xTitle)
	plt.axhline(0, color = "black", linestyle = "--")
	plt.legend(["Saccade 1", "Saccade 2"],loc='best',frameon=False)

	plt.savefig(os.path.join(dst, "%s.svg" % figName))
	plt.savefig(os.path.join(dst, "%s.png" % figName))

if __name__ == "__main__":
	
	trim = True
	blinkRemov = False
	fig3(trim,blinkRemov)	
