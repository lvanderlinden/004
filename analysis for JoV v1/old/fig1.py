#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: fig1.py

"""
Created on Wed Jan 22 11:44:32 2014

@author: lotje

Fig 1:
	- Landing positions per saccade, relative to center and relative
		to CoG, for Experiment 1
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

# Import own modules:
import getDM
import onObject
import constants

# Set font.
# For guidelines, see:
# http://www.journalofvision.org/site/misc/peer_review.xhtml#style

plt.rc("font", family="arial")
plt.rc("font", size=7)


dst = "/home/lotje/Studies/004 - Single-object experiment - Handle-orientation effect/manuscript/Versions/5th draft/Figures JoV"

def fig1(trim, blinkRemov):
	
	"""
	Plots average landing position per sacc relative to center and CoG, for Exp 1
	"""
	
	fig = plt.figure(figsize = (3,5))
	plt.subplots_adjust(left=.2, bottom=.15)


	# Some constant vars:
	yLim = [-.25,.15]
	spacing = .5
	xLabels = ["1", "2", "3"]
	xTitle = "Saccade"
	yTitle = "Normalised landing position"
	#col = "black"
	
	# Data processing:
	exp = "004A"	
	dvList = ["abs", "corr"]
	dm = getDM.getDM(exp)
	
	for col in dm.columns():
		print col
	sys.exit()
	figName= "fig1_trim=%s_blinkRemov=%s" % (trim, blinkRemov)

	lLegend = ["Relative to center", "Relative to CoG"]
	lineStyles = ["-", "-"]
	colList = ["#3465a4", "#ce5c00"]
	
	for dvType in dvList:
		
		lMeans = []
		errMeans = []
		
		for sacc in ["1", "2", "3"]:
			
			if dvType == "corr":
				dv = "endX%sCorrNormToHandle" % sacc
			else:
				dv = "endX%sNormToHandle" % sacc
		
			# Dv must not contain ''s:
			on_dm = onObject.onObject(dm, sacc)

			if blinkRemov:
				on_dm = on_dm.select("n_blink == 0")		


			if trim:
				trim_dm = on_dm.selectByStdDev(keys = ["file"], dv = dv)
			else:
				trim_dm = on_dm
			
			# M's and error bars:
			# Determine avg landing position:
			cm = trim_dm.collapse(["file"], dv)
			m = cm["mean"].mean()
			se = cm['mean'].std() / np.sqrt(len(cm))
			ci = se * constants.critVal
			lMeans.append(m)
			errMeans.append(ci)
	
		# Plot landing positions of all 3 saccadesL
		xData = range(len(lMeans))
		yData = lMeans
		yErr = errMeans
		lineStyle = lineStyles.pop()
		col = colList.pop()
		markerCol = "white"
		plt.errorbar(xData, yData, yerr=yErr, fmt='o-',\
			marker = "o", color = col, linestyle = \
			lineStyle, markerfacecolor=markerCol, markeredgecolor=col,\
			markeredgewidth = 1)
		plt.ylim(yLim)	
	
		# Modify plot:
	plt.legend(lLegend, frameon = False, loc = 'best')
	xTicks = range(0,3)
	plt.xticks(xTicks, xLabels, rotation = .5)
	plt.xlabel(xTitle)
	plt.xlim(min(xTicks)-spacing, max(xTicks)+spacing)
	plt.ylabel(yTitle)
	
	plt.axhline(0, color = "black", linestyle = "--")
	plt.savefig(os.path.join(dst, "%s.svg" % figName))
	plt.savefig(os.path.join(dst, "%s.png" % figName))
	
	
if __name__ == "__main__":
	
	trim = True
	blinkRemov = False	
	fig1(trim,blinkRemov)