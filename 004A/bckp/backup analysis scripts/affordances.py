#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: affordances.py

"""
DESCRIPTION:
There is a trend towards an affordance effect with rtFromLanding
as dependent variable. This one is therefore used for further analyses.

The dm is generated with the default keyword arugments for 
getDM(), except that error trials are excluded.

There is no affordance effect on accuratesse.

For affordance effect over time (i.e. distribution analysis):
see studies._004.analyses.binAnalyses
"""

# Import Python modules:
import numpy as np
import os, sys
from matplotlib import pyplot as plt

# Import own modules:
from exparser.DataMatrix import DataMatrix
from exparser.PivotMatrix import PivotMatrix
from exparser.AnovaMatrix import AnovaMatrix
import getDM


def affordanceEffect(dm, nRows = None, nCols = None, \
		rowCount = None, fig = None):
	
	"""
	RT as a function of handle side and response handle
	
	Note: this two-way interaction should be identical
	to a main effect of compatibility.
	
	Arguments:
	dm
	
	Keyword arguments:
	nRows
	nCols
	rowCount
	fig
	"""

	# Select only handled objects:
	dm = dm.select("symm == 'asymm'")
	
	# Select only trials on which there was no mask applied:
	dm = dm.select("contrast_side == 'control'")
	
	#fig = plt.figure()
	nPlot = 0
	
	factors = ["response_hand", "handle_side"]
	pp = ["file"]
	dv = "rtFromLanding"
		
	# Trim:
	_dm = dm.selectByStdDev(keys = factors + pp, dv = dv)
	
	
	am = AnovaMatrix(_dm, factors = factors, dv = dv, \
		subject = pp[0])._print(maxLen=10, ret=True)
	
	plt.subplot2grid((nRows,nCols), (rowCount, 0))
	pm = PivotMatrix(_dm, factors, pp, dv = dv, colsWithin = True)
	pm.linePlot(fig = fig, legendTitle = factors[0], xLabel = factors[1])

	plt.subplot2grid((nRows,nCols), (rowCount, 1), colspan=2)
	plt.text(0.1,0.1,am, family='monospace')
	
def affOtherFactor(dm, factor2, nRows = None, nCols = None, \
		rowCount = None, fig = None):
	
	"""
	RT as a function of compatibility and something else (e.g. category).
	
	Arguments:
	dm
	factor2
	"""	
	
	# Declare keys:
	factors = ["comp"] + [factor2]
	pp = ["file"]
	dv = "rtFromLanding"
	

	# Select only handled objects:
	dm = dm.select("symm == 'asymm'")
	# Trim:
	dm = dm.selectByStdDev(keys = factors + pp, dv = dv)

	# Create figure:
	#fig = plt.figure()
	nPlot = 0
	
	
	# Stats:
	am = AnovaMatrix(dm, factors = factors, dv = dv, \
		subject = pp[0])._print(maxLen=10, ret=True)
	
	# Plot:
	plt.subplot2grid((nRows, nCols), (rowCount, 0))
	pm = PivotMatrix(dm, factors, pp, dv = dv, colsWithin = True)
	pm.linePlot(fig = fig, lLabels = None,legendTitle = factors[0], xLabel = factors[1])
	plt.subplot2grid((nRows,nCols), (rowCount, 1), colspan=2)
	plt.text(0.1,0.1,am, family='monospace')
	
def affOverTime(dm):
	
	"""
	Affordance effect as a function of binned RT
	
	"""
	import studies._004.analyses.binAnalyses as binning
	dv = 'rtFromLanding'
	varToBin = dv
	factor = 'comp'
	binning.binAnalyses(dm, dv, varToBin, factor, showFig = True)
	

if __name__ == "__main__":
	
	
	for exp in ["004A", "004B"]:
		
		if exp == '004A':
			continue
	
		dm = getDM.getDM(exp = exp, driftCorr = True, excludeErrors = True)#, fixCheck1TooLong = 200, fixCheck2TooLong = 200)
	
		fig = plt.figure(figsize = (9,15))
		plt.subplots_adjust()
		
		nRows = 5
		nCols = 3
		
		affordanceEffect(dm, nRows = nRows, nCols = nCols, rowCount = 0, fig = fig)
		#affOtherFactor(dm, "visual_field", nRows = nRows, nCols = nCols, rowCount = 1, fig = fig)
		#affOtherFactor(dm, "cat", nRows = nRows, nCols = nCols, rowCount = 2, fig = fig)
		#affOtherFactor(dm, "half", nRows = nRows, nCols = nCols, rowCount = 3, fig = fig)
		#affOtherFactor(dm, "contrast_side", nRows = nRows, nCols = nCols, rowCount = 4, fig = fig)
		plt.savefig("%s: Affordance effects.png" % exp)
		plt.clf()
