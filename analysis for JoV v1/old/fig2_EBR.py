#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: landOnHandle.py

"""
Fig 2:
	- The statistical tests (one-sample t-tests) are performed on pp's
		overall means. This does not take WS variance into account,
		and therefore I did NOT use PivotMatrix and WS error bars,
		but the means and error terms as derived from the collapsed
		dm's.
"""

# Import Python modules:
import numpy as np
import os
import sys
from matplotlib import pyplot as plt
import scipy.stats

os.chdir('/home/lotje/Documents/PhD Marseille/Studies/004 - Single-object experiment - Handle-orientation effect/analysis 004')


# Import own modules:
from exparser.DataMatrix import DataMatrix
from exparser.PivotMatrix import PivotMatrix
from exparser.AnovaMatrix import AnovaMatrix
from exparser import Constants
import getDM
import onObject
import constants

plt.rc("font", family="arial")
plt.rc("font", size=7)


dst = "/home/lotje/Documents/PhD Marseille/Studies/004 - Single-object experiment - Handle-orientation effect/manuscript/sources"

fig = plt.figure(figsize = (5,7))
plt.subplots_adjust(wspace = 0, hspace = .3)
figName= "Figure2"

# Plot 1 and 2:
yLim = [-.25,.2]
spacing = .5
xLabels = ["1", "2", "3"]
xTitle = "Saccade"
yTitle = "Normalised landing position"
nRows = 1
nCols = 3


# Subplot 1:
lLegend = ["Relative to center", "Relative to CoG"]
lineStyles = ["--", "-"]
subTitle = "a) Experiment 1"
ax = plt.subplot2grid((3,2),(0, 0), rowspan = 2)
plt.title(subTitle)
exp = "004A"	
dvList = ["abs", "corr"]
dm = getDM.getDM(exp)
#colList = ["#ef2929","#8ae234"]
lStyles = ["--", "-"]
col = "#3465a4"
for dvType in dvList:
	
	lMeans = []
	errMeans = []
	
	for sacc in ["1", "2", "3"]:
		
		
		if dvType == "corr":
			dv = "endX%sCorrNormToHandle" % sacc
		else:
			dv = "endX%sNormToHandle" % sacc
	
		# dv must not contain ''s:
		on_dm = onObject.onObject(dm, sacc)
		trim_dm = on_dm.selectByStdDev(keys = ["file"], dv = dv)
		
		# Determine avg landing position:
		cm = trim_dm.collapse(["file"], dv)
		print len(cm)
		m = cm["mean"].mean()
		se = cm['mean'].std() / np.sqrt(len(cm))
		ci = se * constants.critVal
		lMeans.append(m)
		errMeans.append(ci)

	# Plot landing positions of all 3 saccadesL
	#col = colList.pop()
	
	xData = range(len(lMeans))
	yData = lMeans
	yErr = errMeans
	lineStyle = lineStyles.pop()
	plt.errorbar(xData, yData, yerr=yErr, fmt='o-',\
		linewidth = 1.5, marker = "o", color = col, linestyle = \
		lineStyle, markerfacecolor='white', markeredgecolor=col, \
		markeredgewidth=2)
	plt.ylim(yLim)	

	# Modify plot:
	plt.legend(lLegend, frameon = False)
	xTicks = range(0,3)
	plt.xticks(xTicks, xLabels, rotation = .5)
	plt.xlabel(xTitle)
	plt.xlim(min(xTicks)-spacing, max(xTicks)+spacing)
	plt.ylabel(yTitle)

plt.axhline(0, color = "#888a85", linestyle = "--", linewidth = 1.5)

# Subplot 2:
nPlots = 1
lLegend = ["Relative to CoG", "Saliency simulation"]
subTitle = "b) Experiment 2"
ax = plt.subplot2grid((3,2),(0, 1), rowspan = 2)
plt.title(subTitle)
dvList = "abs"
col = "#f57900"
#colList = ["#f57900", "#3465a4"]	
lStyles = ["--", "-"]

for exp in ["004B", "004C"]:
	dm = getDM.getDM(exp)

	lMeans = []
	errMeans = []
	
	for sacc in ["1", "2", "3"]:
		
		dv = "endX%sNormToHandle" % sacc
	
		# dv must not contain ''s:
		on_dm = onObject.onObject(dm, sacc)
		trim_dm = on_dm.selectByStdDev(keys = ["file"], dv = dv)
		
		# Determine avg landing position:
		cm = trim_dm.collapse(["file"], dv)
		m = cm["mean"].mean()
		se = cm['mean'].std() / np.sqrt(len(cm))
		ci = se * constants.critVal
		lMeans.append(m)
		errMeans.append(ci)
	
	# Plot landing positions of all 3 saccadesL
	#col = colList.pop()
	lineStyle = lStyles.pop()
	
	xData = range(len(lMeans))
	yData = lMeans
	yErr = errMeans
	
	plt.errorbar(xData, yData, yerr=yErr, fmt='o-',\
		linewidth = 1.5, marker = "o", color = col, linestyle = \
		lineStyle, markerfacecolor='white', markeredgecolor=col, \
		markeredgewidth=2)
	
# Modify plot:
plt.ylim(yLim)	
plt.legend(lLegend, frameon = False)
xTicks = range(0,3)
plt.xticks(xTicks, xLabels, rotation = .5)
plt.xlabel(xTitle)
plt.xlim(min(xTicks)-spacing, max(xTicks)+spacing)
ax.yaxis.set_ticklabels([])

plt.axhline(0, color = "#888a85", linestyle = "--", linewidth = 1.5)


# Plot 3:
ax = plt.subplot2grid((3,2),(2, 0), colspan = 2)
yLim = [-.25,.05]
dm_sim = getDM.getDM("004C")
dm = getDM.getDM(exp = "004B")

col = "#73d216"
colList = ["#edd400", "#ad7fa8"]
lineStyles = ["--", "-"]
xTitle = "Binned saccade latency"
subTitle = "c) Time course"
plt.title(subTitle)

for sacc in ["1", "2"]:
	
	lX = []
	lY = []
	
	dv = "endX%sNormToHandle" % sacc
	nBin = 10

	#sim_avg = dm_sim["endX%sNormToHandle" % sacc].mean()
		
	# Only on-object:
	on_dm = onObject.onObject(dm, sacc)

	# Trim on both variables:
	dm_trim1 = on_dm.selectByStdDev(["file"], dv)
	dm_trim1 = dm_trim1.removeField("__dummyCond__")
	dm_trim1 = dm_trim1.removeField("__stdOutlier__")
	dm_trim2 = dm_trim1.selectByStdDev(["file"], "saccLat%s" % sacc)

	# Make bins, only for the first dv (for the second dv, the binned 
	# variable is the same and therefore already exists:
	saccLat = "saccLat%s" % sacc
	varToBin = saccLat
	binnedVar = "binnend%s" % varToBin
	binned_dm = dm_trim2.addField(binnedVar)
	binned_dm = binned_dm.calcPerc(varToBin, binnedVar ,keys = ["file"], nBin = nBin)
	
	for _bin in binned_dm.unique(binnedVar):  
		# Filter out all but one bin
		_dm = binned_dm.select('%s == %f' % (binnedVar, _bin))
				
		x = _dm["saccLat%s"%sacc].mean()
		y = _dm["endX%sNormToHandle"%sacc].mean()
		
		# TODO: error bars
		lY.append(y)
		lX.append(x)		
	
	lineStyle = lineStyles.pop()
	#col = colList.pop()
	plt.plot(lX,lY, color = col, marker = 'o', linestyle = lineStyle, \
		linewidth = 1.5, markerfacecolor="white", markeredgecolor=col, \
		markeredgewidth=2)

plt.xlabel(xTitle)
#plt.xscale('log')
plt.ylabel(yTitle)
plt.ylim(yLim)

#xLabels = range(100,550, 25)
#xTicks= range(0,len(xLabels))
#plt.xticks(xTicks, xLabels, rotation = .5)
plt.xlabel(xTitle)
#plt.xlim(min(xTicks), max(xTicks))

#plt.xticks([])
# Indicate reference point:
plt.axhline(0, color = "#888a85", linestyle = "--", linewidth = 1.5)

plt.legend(["Saccade 1", "Saccade 2"], loc = 'best', frameon = False)
plt.savefig(os.path.join(dst, "Figure_2_EBR.png"))
#plt.show()
	
