#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: regressionAnalyses.py

"""
DESCRIPTION:

TODO:
- trim multiple dv's

NOTE:
"""

# Import Python modules:
import math
import numpy as np
import scipy.stats
from matplotlib import cm
from matplotlib import pyplot as plt
import sys
import os
import pylab

# Import own modules:
from exparser.EyelinkAscFolderReader import EyelinkAscFolderReader
from exparser.DataMatrix import DataMatrix
from exparser.PivotMatrix import PivotMatrix
from exparser.AnovaMatrix import AnovaMatrix
from exparser import Constants
import getDM
import onObject


# Set font
plt.rc("font", family=Constants.fontFamily)
plt.rc("font", size=12)

outputFolder = "/home/lotje/Documents/PhD Marseille/Studies/004 - One-object experiment - Orienation effect/Analysis/plots/plots regressions"

def regrAn(showFig = False, subjectID = ["file"], trim = False,\
		saveFig = True, printStats = True, saveExt = ".jpg", figName = None,\
		cousineau = True, col = "blue", scatter = False):
	
	"""
	Performs and plots regression analyses for two dependent variables.
	
	Arguments:
	dm			--- Data matrix.
	dvList		--- List of two dependent variables (x,y).
	
	Keyword arguments:
	subjectID	
	showFig		--- Boolean indicating whether or not to show the plots. Default 
					= False.
	saveFig 	--- Boolean indicating whehter or not to save the plot. Default = 
					True.
	printStats	--- Boolean indicating whether or not to print stats.
	"""
	
	for exp in ["004A", "004B"]:
		
		if exp != "004B":
			continue
		
		fig = plt.figure()
		
		dm = getDM.getDM(exp)
		
		colList1 = ["#fcaf3e", "#8ae234", "#729fcf"]
		colList2 = ["#ce5c00", "#4e9a06", "#204a87"]
		
		figName = "Regression %s - cousineau = %s scatter = %s" % (exp, cousineau, scatter)
		
		for sacc in ["1", "2", "3"]:
			if sacc != "1":
				continue
			
			dv2 = "endX%sNormToHandle" % sacc
			dv1 = "saccLat%s" % sacc
			
			on_dm = onObject.onObject(dm, sacc, exclY = False)
			
			filter_dm = on_dm.select('saccLat%s > 80' % sacc)
			#filter_dm = filter_dm.select('saccLat%s < 500' % sacc)
			#filter_dm = on_dm
			
			trim_dm = filter_dm.selectByStdDev(keys = ["file"], dv = dv1)

			col1 = colList1.pop()
			col2 = colList2.pop()
			
			if cousineau:
				for new_var in [dv1, dv2]:
					trim_dm = trim_dm.addField("cousineau_%s"%new_var, dtype = None)
					trim_dm = trim_dm.withinize(new_var, "cousineau_%s"%new_var, subjectID, verbose = True, \
						whiten=False)
				
				dv1 = "cousineau_%s"%dv1
				dv2 = "cousineau_%s"%dv2

			x = trim_dm[dv1]
			y = trim_dm[dv2]
			
			slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(x,y)
			stats = "slope = %.2f, intercept = %.2f, R = %.2f, p = %.3f, SE = %.2f" \
				% (slope, intercept, r_value, p_value, std_err)
			
			if printStats:
				print "Exp = ", exp
				print "DV = ", dv1
				print stats
				#raw_input()
			if scatter:
				pylab.plot(x, y, ',', color = col1)#, alpha = .3)
				
			fitX = np.array([x.mean()-2*x.std(), x.mean()+2*x.std()])
			pylab.plot(fitX, intercept + slope*fitX, color = col2, linewidth = 2, marker = 'o')
		
		if scatter:
			plt.ylim([-.7,.7])
		else:
			plt.ylim([-.4, .4])
			plt.legend(["sacc1", "sacc2", "sacc3"])
		plt.axhline(0, color = '#888a85', linestyle = "--", linewidth = 2)
		
		plt.savefig("%s.png" % figName)
	
if __name__ == "__main__":
	
	for scatter in [True, False]:
		regrAn(scatter = scatter)
