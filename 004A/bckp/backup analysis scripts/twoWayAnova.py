#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: twoWayAnova.py

"""
DESCRIPTION:
Does tendency to land towards CoG fade over time?

TODO:

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


def twoWayAnova(dm, dv, factor1, factor2, onlyControl = True, addStats = True, figTitle = True):
	
	"""
	Plots landing positions as a function of gap condition.
	
	Arguments:
	dm
	dv		--- dv
	factor2	-- second IV
	"""
	
	if onlyControl and (factor2 == "contrast_side" or factor1 == "contrast_side"):
		print "You can't exclude contrast manipulation if one of the IV's is contrast_side"
		return
	
	if onlyControl:
		dm = dm.select("contrast_side == 'control'")
	
	# Define keys:
	factors = [factor2, factor1]
	pp = ["file"]
	
	exp = dm["exp"][0]
	
	if addStats:
		nCols = nRows = 2
		fig = plt.figure()
		
	else:
		nCols = nRows = 1
		fig = plt.figure(figsize = (3,5))
		
	# Apply selections:
	dm = dm.select("%s != ''" % dv)
	dm = dm.selectByStdDev(keys = factors + pp, dv = dv)
	
	# Create figure:
	plt.subplots_adjust(hspace = .4)
	
	figName = "%s: %s as a function of %s and %s onlyControl = %s" % (exp, dv, factor1, factor2, onlyControl)
	if figTitle:
		plt.suptitle(figName)
	plt.subplot2grid((nRows,nCols), (0, 0))
	
	pm = PivotMatrix(dm, factors, pp, dv, colsWithin = True)

	# Note why I have to give the lLabels as a parameter: the underscore of "_left" gives problems for plotting
	# the legend.??
	if factor2 == "contrast_side":
		lLabels = ["left", "contrast", "right"]
	else:
		lLabels = None
	pm.linePlot(fig = fig,xLabel = factors[-1], legendTitle = factors[0], lLabels = lLabels)
	
	plt.ylabel(dv)
	plt.axhline(0, color = "#555753", linestyle = "--", linewidth = 2)
	
	if addStats:
		am = AnovaMatrix(dm, factors = factors, dv = dv, \
			subject = pp[0])._print(maxLen=10, ret=True)
		plt.subplot2grid((nRows,nCols), (1, 0), colspan=2)
		plt.text(0.1,0.1,am, family='monospace')
		plt.savefig("%s.png"%figName)
	
	return fig
	
