#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: affordances.py

"""
DESCRIPTION:
Check for Simon effects:
- Effect of hand and mask on RT
- Effect of hand and CoG on RT
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


def simonHeavySide(dm, nRows = None, nCols = None, \
		rowCount = None, fig=None):
	
	"""
	RT as a fucntion of hand and center of gravity (heavy side)
	
	Arugments:
	dm
	
	Keyword arguments:
	rowCount
	fig
	
	"""
	
	factors = ["response_hand", "heavySide"]
	pp = ["file"]
	dv = "rtFromLanding"
	
	dm = dm.selectByStdDev(keys = factors + pp, dv = dv)
	

	plt.subplot2grid((nRows,nCols), (rowCount, 0))#, colspan=2)
	pm = PivotMatrix(dm, factors, pp, dv, colsWithin = True)
	pm.linePlot(fig = fig, xLabel = 'heavy side')
	
	am = AnovaMatrix(dm, factors = factors, dv = dv, \
		subject = pp[0])._print(maxLen=8, ret=True)
	plt.subplot2grid((nRows,nCols), (rowCount, 1), colspan=2)
	plt.text(0.1,0.1,am, family='monospace')
	
def simonContrast(dm, nRows = None, nCols = None, rowCount = None, fig = None):
	
	"""
	RT as a fucntion of hand and mask side
	
	Arugments:
	dm
	
	Keyword arguments:
	rowCount
	fig
	"""
	
	
	factors = ["response_hand", "contrast_side"]
	pp = ["file"]
	dv = "rtFromLanding"
	
	dm = dm.selectByStdDev(keys = factors + pp, dv = dv)
	
	plt.subplot2grid((nRows,nCols), (rowCount, 0))#, colspan=2)
	pm = PivotMatrix(dm, factors, pp, dv, colsWithin = True)
	pm.linePlot(fig = fig, xLabel = 'most contrast')
	am = AnovaMatrix(dm, factors = factors, dv = dv, \
		subject = pp[0])._print(maxLen=8, ret=True)
	
	plt.subplot2grid((nRows,nCols), (rowCount, 1), colspan=2)
	plt.text(0.1,0.1,am, family='monospace')
	

def simonSaccDir(dm, nRows = None, nCols = None, \
		rowCount = None, fig = None):
	
	"""
	RT as a fucntion of hand and mask side
	
	Arugments:
	dm
	
	Keyword arguments:
	rowCount
	fig
	"""
	
	# Add variable indicating direction of the first saccade:
	dm = dm.addField('saccDir', dtype = str)
	dm = dm.select("endX1Norm != ''")
	dm['saccDir'] = 'left'
	dm['saccDir'][np.where(dm['endX1Norm'] >= 0.)] = 'right'
	
	factors = ["response_hand", "saccDir"]
	pp = ["file"]
	dv = "rtFromLanding"
	
	dm = dm.selectByStdDev(keys = factors + pp, dv = dv)
	
	plt.subplot2grid((nRows,nCols), (rowCount, 0))#, colspan=2)
	pm = PivotMatrix(dm, factors, pp, dv, colsWithin = True)
	pm.linePlot(fig = fig, xLabel = 'saccade direction')
	am = AnovaMatrix(dm, factors = factors, dv = dv, \
		subject = pp[0])._print(maxLen=8, ret=True)
	
	plt.subplot2grid((nRows,nCols), (rowCount, 1), colspan=2)
	plt.text(0.1,0.1,am, family='monospace')
	

if __name__ == "__main__":
	
	for exp in ["004A", "004B"]:
		dm = getDM.getDM(exp = exp, driftCorr = True, excludeErrors = True)
		
		fig = plt.figure()
		plt.subplots_adjust(hspace = .8)
		
		simonHeavySide(dm, nRows = 3, nCols = 3, rowCount = 0, fig = fig)
		simonContrast(dm, nRows = 3, nCols = 3, rowCount = 1, fig = fig)
		simonSaccDir(dm, nRows = 3, nCols = 3, rowCount =2, fig = fig)
		
		plt.savefig("%s: Simon effects on RT.png" % exp)
	
	