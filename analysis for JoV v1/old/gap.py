# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 11:39:42 2014

@author: lotje
"""

import getDM
import onObject
from exparser.CsvReader import CsvReader
from exparser.TangoPalette import *
import numpy as np
import re
import sys
from matplotlib import pyplot as plt

# Set font:
plt.rc("font", family="arial")
plt.rc("font", size=7)

def normY(a, flatten=False):
	
	# Normalise:
	a = abs(a)
	
	if flatten:
		k = 3
		maxVal = a.mean() + a.std() * k
		i = np.where(a > maxVal)
		a[i] = maxVal
	
	_min = float(np.min(a))
	_max = float(np.max(a))
	
	y = (a-_min)/(_max-_min)
	
	return y

def plotGap(exp, dv = "saccLat1", trim = False, norm=True, nBins = 50, \
	exclFastSacc = False):
	
	"""
	"""
	
	src = 'selected_dm_%s_WITH_drift_corr_onlyControl_True.csv' % exp
	dm = CsvReader(src).dataMatrix()

	# Determine sacc:
	sacc = [int(x.group()) for x in re.finditer(r'\d+', dv)][0]
	dm = onObject.onObject(dm, sacc)
	
	# Exclude very fast saccades:
	dm = dm.select("%s > 80" % dv)	
	
	colList = [orange[1], blue[1]]

	# Trim the data
	if trim:
		
		dm = dm.removeField("__dummyCond__")
		dm = dm.removeField("__stdOutlier__")

		dm = dm.selectByStdDev(["file"], dv, \
			verbose=False)
		dm = dm.removeField("__dummyCond__")
		dm = dm.removeField("__stdOutlier__")
		dm = dm.selectByStdDev(["file"], "endX%sNormToHandle" % sacc, \
			verbose=False)
		
		if exp == "004A":
			dm = dm.removeField("__dummyCond__")
			dm = dm.removeField("__stdOutlier__")
			dm = dm.selectByStdDev(["file"], "endX%sCorrNormToHandle" % sacc, \
				verbose=False)
				
	else:
		dm = dm.select("%s < 1000" % dv)
	
	# Normalize saccade latencies 
	if norm:
		dm= dm.addField("normSacc", dtype = float)
		dm= dm.withinize(dv, "normSacc", \
				["file"], whiten=False)
		dv = "normSacc"
		
	for gap in dm.unique("gap"):
		
		_dm = dm.select("gap == '%s'" % gap)

		samp = _dm[dv]
	
		y, edges = np.histogram(samp, bins = nBins)
		y = normY(y)
				
		x = .5*edges[1:] + .5*edges[:-1]
		col = colList.pop()
		plt.plot(x, y, color = col)
		plt.fill_between(x, 0, y, alpha=.3, color=col)	
	plt.legend(dm.unique("gap"))
	plt.ylim([0,1.1])
	#plt.xlim([0,350])
		

if __name__ == "__main__":
	
	
	trim=True
	exclFastSacc=False
	for norm in [True, False]:

		fig = plt.figure(figsize = (5,5))
		plt.subplots_adjust(left=.2, bottom=.15)
	
		nRows = 2
		nCols = 1
		nPlot = 0
		lTitle = ["Exp 2", "Exp 1"]
		for exp in ["004A", "004B"]:
	
			nPlot +=1
			plt.subplot(nRows, nCols,nPlot)
			plt.title(lTitle.pop())
			plotGap(exp,norm=norm,trim=trim,exclFastSacc=exclFastSacc)
		plt.savefig("Gap_effect_norm_%s_trim_%s_exclFastSacc_%s.png" % \
			(norm, trim,exclFastSacc))
