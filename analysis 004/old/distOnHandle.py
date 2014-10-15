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

def dist(trim = True, spacing = .5, exclOverlap = False, \
	exclY = False, colList = ["#ef2929", "#3465a4", "#f57900", "#73d216"],\
		lLegend = ["Exp1: relative to center", "Exp1: relative to CoG", \
		"Exp2: relative to CoG", "Exp3: relative to CoG"], yLim = [-.3, .3],\
		xLabels = ["1", "2", "3"], xTitle = "saccade", \
		yTitle = "normalised landings towards handle"):
	
	"""
	Landing position as a funciton of orientation, across or per object group.
	
	Arguments:
	
	Keyword arguments:
	trim			--- 
	exclOverlap		--- indicates whether or not to exclude gap-overlap trials
						in the simulation.
	"""
	
	fig = plt.figure(figsize = (10,10))
	
	nPlot = 0
	nCols = 3
	nRows = 4

	for exp in ["004A", "004B", "004C"]:
		
		
		dm = getDM.getDM(exp)
		
		if exp == "004A":
			dvList = ["abs", "corr"]
		else:
			dvList = ["abs"]
			
		if exp == "004C":
			nBins = 20
		else:
			nBins= 100
		
		for dvType in dvList:
			lMeans = []
			
			for sacc in ["1", "2", "3"]:
				
				if dvType == "corr":
					dv = "endX%sCorrNormToHandle" % sacc
				else:
					dv = "endX%sNormToHandle" % sacc
			
				# dv must not contain ''s:
				on_dm = onObject.onObject(dm, sacc)
			
				if trim:
					trim_dm = on_dm.selectByStdDev(keys = ["file"], dv = dv)
				else:
					trim_dm = on_dm
				
				nBins = int(len(trim_dm)/15)
#				if exp == "004C":
#					nBins = 10
#				if sacc == "3":
#					nBins = 10
				#print nBins
				#nBins = 10
				
				# TODO TODO TODO: cousineau??
				# See:http://glowingpython.blogspot.fr/2012/07/distribution-fitting-with-scipy.html
				samp = trim_dm[dv]
				param = norm.fit(samp) # distribution fitting
				
				x = linspace(-.5,.5,nBins)
				# fitted distribution
				pdf_fitted = norm.pdf(x,loc=param[0],scale=param[1])
				# original distribution
				pdf = norm.pdf(x)
				nPlot +=1
				plt.subplot(nRows, nCols, nPlot)
				plt.title('Exp = %s dv = %s sacc = %s nBins = %s' % \
					(exp, dv, sacc, nBins))
				#plt.plot(x,pdf_fitted,tango.orange[1]) #,x,pdf,'b-')
				#plt.show()
				hist, edges = np.histogram(samp, bins = nBins)
				print hist.shape, edges.shape
				x = .5*edges[1:] + .5*edges[:-1] #linspace(-.5,.5,nBins)				
				#plt.hist(samp,normed=1,alpha=.3,bins = nBins, color = "#729fcf")
				plt.plot(x, hist, color = tango.skyBlue[1], alpha = .5)				
				plt.axvline(0, linestyle = "--", color = "#2e3436", \
					linewidth = 2)
				plt.xlim([-.7, .7])				
				#plt.show()
	plt.savefig("distributions.png")
	plt.show()
if __name__ == "__main__":
	
	dist()	