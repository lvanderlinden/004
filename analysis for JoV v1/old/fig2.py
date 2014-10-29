#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: fig2.py
"""
Created on Wed Jan 22 11:54:37 2014

@author: lotje

Fig 2:
	- Landing positions exp 2
	- Landig positions saliency simulation

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

def fig2(trim, blinkRemov):
	
	"""
	Plots average observed and simulated landing position per sacc, for Exp 2.
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

	figName= "fig2_trim=%s_blinkRemov=%s" % (trim, blinkRemov)
	
	lLegend = ["Relative to center", "Relative to CoG"]
	lineStyles = ["-", "-"]
	colList = ["#73d216", "#3465a4"]

	
	for exp in ["004B", "004C"]:
		dm = getDM.getDM(exp)
	
		lMeans = []
		errMeans = []
		
		for sacc in ["1", "2", "3"]:
			
			dv = "endX%sNormToHandle" % sacc
		
			# dv must not contain ''s:
			on_dm = onObject.onObject(dm, sacc)
			
			# Remove blinks:
			if blinkRemov:
				if exp == "004B":
					on_dm = on_dm.select("n_blink == 0")		

			if trim:
				trim_dm = on_dm.selectByStdDev(keys = ["file"], dv = dv)
			else:
				trim_dm = on_dm
			
			# Determine avg landing position:
			# M and error bars:
			cm = trim_dm.collapse(["file"], dv)
			m = cm["mean"].mean()
			se = cm['mean'].std() / np.sqrt(len(cm))
			ci = se * constants.critVal
			lMeans.append(m)
			errMeans.append(ci)
		
		# Plot:
		xData = range(len(lMeans))
		yData = lMeans
		yErr = errMeans
		lineStyle = lineStyles.pop()
		#markerCol = colList.pop()
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
	fig2(trim,blinkRemov)