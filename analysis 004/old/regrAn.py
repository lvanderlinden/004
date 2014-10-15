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
from exparser import Constants
import msg.userMsg

# Set font
plt.rc("font", family=Constants.fontFamily)
plt.rc("font", size=12)

outputFolder = "/home/lotje/Documents/PhD Marseille/Studies/004 - One-object experiment - Orienation effect/Analysis/plots/plots regressions"

def regrAn(dm, dvList, showFig = False, subjectID = ["file"], trim = False,\
		saveFig = True, printStats = True, saveExt = ".jpg", figName = None,\
		cousineau = True):
	
	"""
	Performs and plots regression analyses for two dependent variables.
	
	Arguments:
	dm			--- Data matrix.
	dvList		--- List of two dependent variables (x,y).
	
	Keyword arguments:
	subjectID	
	showFig		--- Boolean indicating whether or not to show the plots. 
					Default = False.
	saveFig 	--- Boolean indicating whehter or not to save the plot. Default = 
					True.
	printStats	--- Boolean indicating whether or not to print stats.
	"""
	
	# Check whether trim is not set to True:
	if trim:
		msg.userMsg.userMsg("Trimming is not possible yet. Set to False.", \
			__file__)
	
	dv1, dv2 = dvList
	
	if cousineau:
		
		for new_var in [dv1, dv2]:
			dm = dm.addField("cousineau_%s"%new_var, dtype = None)
			dm = dm.withinize(new_var, "cousineau_%s"%new_var, subjectID, verbose = True, \
				whiten=False)
		
		dv1 = "cousineau_%s"%dv1
		dv2 = "cousineau_%s"%dv2

	x = dm[dv1]
	y = dm[dv2]
		
	
	fit = scipy.polyfit(x,y,1)
	fit_fn = scipy.poly1d(fit)
	
	slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(x,y)
	stats = "slope = %.2f, intercept = %.2f, R = %.2f, p = %.3f, SE = %.2f" \
		% (slope, intercept, r_value, p_value, std_err)
	
	if printStats:
		print stats
	
	fig = plt.figure()
	if figName == None:
		figName = "Correlation between %s and %s cousineau = %s" % (dvList[0], dvList[1], \
		cousineau)
	
	plt.plot(x,y, 'yo', x, fit_fn(x), '--k')
	
	plt.xlabel(dvList[0])
	plt.ylabel(dvList[1])
	plt.title("%s\n%s"%(figName,stats))
	if showFig:
		plt.show()
		saveFig = False
	if saveFig:
		plt.savefig("%s%s"%(figName, saveExt))
		
	return fig

if __name__ == "__main__":
	
	import getDM
	import onObject
	
	exp = "004B"
	
	dm = getDM.getDM(exp)
	
	dm1 = onObject.onObject(dm, "1")
	dm2 = onObject.onObject(dm, "2")
	
	
		

	
	
