#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: saccLat.py

"""
DESCRIPTION:
Plots several condition effects on saccade latencies.
- Distributions as a function of gap condition and VF
	(split per VF because saccade direction can influence gap 
	effect - Goldring & Fischer, 1997)
- ANOVA with Gap and VF as factor and initial sacc latency as
	dv
- ANOVA with contrast manipulation -> faster if more
	contrast on display?

TODO:
Fit line through distribution
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


def gapEffect(dm, saccCount = "1"):
	
	"""
	Plots dist hist of sacc latencies as a function of gap condition.
	
	Arguments:
	dm
	
	Keyword arguments:
	saccCount	--- Default = "1"
	
	"""
	
	# Define keys:
	factors = ["visual_field", "gap"]
	pp = ["file"]
	dv = "saccLat%s" % saccCount
	
	exp = dm["exp"][0]
	# Apply selections:
	dm = dm.select("%s != ''" % dv)
	dm = dm.selectByStdDev(keys = factors + pp, dv = dv)
	
	# Create figure:
	fig = plt.figure()
	plt.subplots_adjust(hspace = .4)
	figName = "%s: Latencies sacc %s as a function of Gap and Visual Field" % (exp, saccCount)
	plt.suptitle(figName)
	nPlots = 0

	for vf in ["upper", "lower"]:
		
		vf_dm = dm.select("visual_field == '%s'" % vf)
		
		#plt.subplot(nRows, nCols, nPlots)
		plt.subplot2grid((3,2), (nPlots, 0))
		
		for gap in ["zero", "overlap"]:
			
		
			if gap == "zero":
				col = "#ef2929"
			else:
				col = "#8ae234"
			
			plt.title("%s visual field" % vf)

			gap_dm = vf_dm.select("gap == '%s'" % gap)
			plt.hist(gap_dm[dv], bins = 30, color = col, alpha = .3)
			plt.xlim(0, 400)
			plt.ylabel('freq')
			plt.xlabel('initial saccade latencies')
				
		if vf == "lower":
			plt.legend(["zero", "overlap"], loc = 'best')
		nPlots +=1

	plt.subplot2grid((3,2), (0, 1), rowspan=2)
	pm = PivotMatrix(dm, factors, pp, dv, colsWithin = True)
	pm.linePlot(fig = fig)
	plt.ylabel("saccade latency")
	am = AnovaMatrix(dm, factors = factors, dv = dv, \
		subject = pp[0])._print(maxLen=10, ret=True)
	plt.subplot2grid((3,2), (2, 0), colspan=2)
	plt.text(0.1,0.1,am, family='monospace')
	plt.savefig("%s.png"%figName)

def contrastEffect(dm, saccCount):
	
	"""
	Plots dist hist of sacc latencies as a function of gap condition.
	
	Arguments:
	dm
	saccCount
	"""
	
	# Define keys:
	factors = ["contrast_side", "gap"]
	pp = ["file"]
	dv = "saccLat%s" % saccCount
	
	exp = dm["exp"][0]
	
	
	# Apply selections:
	dm = dm.select("%s != ''" % dv)
	dm = dm.selectByStdDev(keys = factors + pp, dv = dv)
	
	# Create figure:
	fig = plt.figure()
	plt.subplots_adjust(hspace = .4)
	figName = "%s: Latencies sacc %s as a function of Gap and Contrast" % (exp, saccCount)
	plt.suptitle(figName)
	plt.subplot2grid((2,2), (0, 0))
	
	pm = PivotMatrix(dm, factors, pp, dv, colsWithin = True)
	pm.linePlot(fig = fig,xLabel = factors[-1], legendTitle = factors[0], lLabels = ["left", "contrast", "right"])
	# NOTE why I have to give the lLabels as a parameter: the underscore of "_left" gives problems for plotting
	## the legend.??
	plt.ylabel(dv)
	
	am = AnovaMatrix(dm, factors = factors, dv = dv, \
		subject = pp[0])._print(maxLen=10, ret=True)
	plt.subplot2grid((2,2), (1, 0), colspan=2)
	plt.text(0.1,0.1,am, family='monospace')
	plt.savefig("%s.png"%figName)
	
	return fig
	
	
	

if __name__ == "__main__":
	
	for exp in ["004A", "004B"]:

		dm = getDM.getDM(exp = exp, driftCorr = True)

		gapEffect(dm)
		contrastEffect(dm)


	