#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: landOnHandle.py

"""
Landing positions as a function of object orientation (across and
per 'object group').

ANOVA's
Bin analyses
"""

# Import Python modules:
import numpy as np
import os
import sys
from matplotlib import pyplot as plt
import scipy.stats
from scipy.stats import norm
from numpy import linspace
from pylab import plot,show,hist,figure,title


# Import own modules:
from exparser.DataMatrix import DataMatrix
from exparser.PivotMatrix import PivotMatrix
from exparser.AnovaMatrix import AnovaMatrix
from exparser import TangoPalette as tango
import getDM
import onObject
import constants

dst = "/home/lotje/Documents/PhD Marseille/Studies/004 - Single-object experiment - Handle-orientation effect/manuscript/sources"

def ovp(nBin = 5, toHandle = False, onlyControl = True):
	
	"""
	Plots dv as a function of binned other variable.
	
	Arguments:
	dm
	dvList
	
	Keyword arguments:
	binVar
	nBin

	"""
	
	if toHandle:
		add = "ToHandle"
	else:
		add = ""
		
	plt.figure(figsize = (20,8))
	#fig = plt.figure(figsize = (15,5))
	plt.subplots_adjust(hspace = .5, wspace = .2)
	
	nRows = 3
	nCols = 6
	plotCount = 0
	
	colList = ["red", "blue", "green"]
	
	for exp in ["004A", "004B"]:
		
		if toHandle:
			dm = getDM.getDM(exp = exp, onlyControl = onlyControl, excludeFillers =\
				True)
		else:
			dm = getDM.getDM(exp = exp, onlyControl = onlyControl, excludeFillers =\
				False)

		if exp == "004A":
			lBinVar = ["endX1Norm"+add, "endX1CorrNorm"+add]
		if exp == "004B":
			lBinVar = ["endX1Norm"+add]

	
		for binVar in lBinVar:
			
			if exp == "004A" and "Corr" in binVar:
				lVars = ["endX2CorrNorm"+add, "refixProb", "saccCount", \
					"durationFix1", "gazeDur", "RT"]

			else:
				lVars = ["endX2Norm"+add, "refixProb", "saccCount", \
					"durationFix1", "gazeDur", "RT"]
				
		
			col = colList.pop()
	
			if "1" in binVar:
				sacc = "1"
			if "2" in binVar:
				sacc = "2"
			if "3" in binVar:
				sacc = "3"
		
			#plotCount = 0
			for dv in lVars:
				
				plotCount +=1
			
				# Only trials on which the variables of interest exist:
				on_dm = onObject.onObject(dm, sacc)
				on_dm = on_dm.select("%s != ''" % dv)
				
				# Make bins, only for the first dv (for the second dv, the binned 
				# variable is the same and therefore already exists:
				binnedVar = "binnend%s" % binVar
				binned_dm = on_dm.addField(binnedVar)
				binned_dm = binned_dm.calcPerc(binVar, binnedVar ,keys = ["file"], \
					nBin = nBin)
				
				lX = []
				lY = []	
				
				for _bin in binned_dm.unique(binnedVar):
					
					print 'bin = ', _bin
					
					# Filter out all but one bin
					_dm = binned_dm.select('%s == %f' % (binnedVar, _bin))
					
					x = _dm[binVar].mean()
			
					y = _dm[dv].mean()
		
					lY.append(y)
					lX.append(x)		
				
				plt.subplot(nRows, nCols, plotCount)
				#plt.title("Exp = %s - binVar = %s" % (exp, binVar))
				plt.plot(lX,lY, color = col, marker = 'o', linewidth = 1.5, \
					markerfacecolor="white", markeredgecolor=col, \
					markeredgewidth=2)
				plt.axvline(0, color = "gray")
				if "endX" in dv:
					plt.axhline(0, color = "gray")
				plt.xlabel(binVar)
				plt.ylabel(dv)
			
	plt.savefig("OVP_effects_ToHandle = %s onlyControl = %s.png" % (toHandle, onlyControl))

if __name__ == "__main__":
	
	ovp(onlyControl=False)
	
