#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: fig5.py

"""
Created on Wed Jan 22 13:16:37 2014

@author: lotje

Fig 5:
- Distributions of landing positions Exp. 2 per saccade.
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

# Set font.
# For guidelines, see:
# http://www.journalofvision.org/site/misc/peer_review.xhtml#style
plt.rc("font", family="arial")
plt.rc("font", size=7)


# Some constant vars:
dst = "/home/lotje/Studies/004 - Single-object experiment - Handle-orientation effect/manuscript/Versions/5th draft/Figures JoV"


def fig5(trim, blinkRemov):
	
	"""
	"""
	
	fig = plt.figure(figsize = (8,2))
	
	figName= "fig5_trim=%s_blinkRemov=%s" % (trim, blinkRemov)
	
	plt.subplots_adjust(wspace=0.1, hspace = 0.1, left = .2, bottom = .15)

	nPlot = 0
	nCols = 3
	nRows = 1
	
	letList = ["c", "b", "a"]
	
	exp = "004B"
	nBins= 100
	col = "#3465a4"
	# Data processing:
	dm = getDM.getDM(exp)
	
	lMeans = []
	
	for sacc in ["1", "2", "3"]:
		
		dv = "endX%sNormToHandle" % sacc
	
		# dv must not contain ''s:
		on_dm = onObject.onObject(dm, sacc)
		
		if blinkRemov:
			on_dm = on_dm.select("n_blink == 0")		
		
		if trim:	
			trim_dm = on_dm.selectByStdDev(keys = ["file"], dv = dv)
		else:
			trim_dm = on_dm
		
		nBins = int(len(trim_dm)/20)
		#nBins = 100
	
		samp = trim_dm[dv]
	
		nPlot +=1
		ax = plt.subplot(nRows, nCols, nPlot)
		if exp == "004A" and dv == "endX%sNormToHandle" % sacc:
			plt.title('%s) Saccade %s' % (letList.pop(), sacc))
	
		a, edges = np.histogram(samp, bins = nBins)
	
		# NORMALISE:	
		a = abs(a)
		
		k = 3
		maxVal = a.mean() + a.std() * k
		i = np.where(a > maxVal)
		a[i] = maxVal
		
		_min = float(np.min(a))
		_max = float(np.max(a))
		
		y = (a-_min)/(_max-_min)			
		
		x = .5*edges[1:] + .5*edges[:-1]
		
		if sacc == "1":
			plt.ylabel("Normalised frequency")
		else:
			ax.yaxis.set_ticklabels([])			
		col = "#3465a4"
		plt.plot(x, y, '-', color = col)				
		plt.axvline(0, linestyle = "--", color = "black")
		plt.xlim([-.7, .7])
		if sacc == "2":
			plt.xlabel("Normalised landing position")
		plt.ylim([0, 1.1])
	
	plt.savefig(os.path.join(dst, "%s.svg" % figName))
	plt.savefig(os.path.join(dst, "%s.png" % figName))

if __name__ == "__main__":
	trim = True
	blinkRemov = False
	fig5(trim,blinkRemov)		