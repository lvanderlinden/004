#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: fig2.py
"""
Created on Wed Jan 22 13:16:37 2014

@author: lotje

DESCRIPTION
Distribution of landing positions
- per saccade
- per reference point
- per experiment

TODO: 
Normalise per factor that might influence distributions, that we're not
interested in:
- Object


"""

# Import Python modules:
import numpy as np
import os
import sys
from matplotlib import pyplot as plt

# Import own modules:
from exparser.TangoPalette import *
import getDM
import onObject

# Set font.
# For guidelines, see:
# http://www.journalofvision.org/site/misc/peer_review.xhtml#style
plt.rc("font", family="arial")
plt.rc("font", size=7)

# Some constant vars:
dst = "/home/lotje/Studies/004 - Single-object experiment - Handle-orientation effect/manuscript/Versions/5th draft/Figures JoV"


def distr(exp, handle_side = None, trim=True, blinkRemov=False, 
	withMarker=False, withinize=True):
	
	"""
	Plots distribution per saccade (seperate subplots) per reference point
	(seperate lines) per experiment (seperate main plots)
	
	Arguments:
	exp
	
	Keyword arguments:
	trim
	blinkRemov
	withMarker
	"""
	
	figName= \
		"Distribution_%s_trim=%s_blinkRemov=%s_handle=%s_Withinze=%s" % \
		(exp, trim, blinkRemov, handle_side, withinize)

	fig = plt.figure(figsize = (7,3))
	plt.subplots_adjust(wspace=0)#, left = .2, bottom = .15)

	nPlot = 0
	nCols = 2
	nRows = 1
	
	if exp == "004A":
		dvList = ["abs", "corr"]
	elif exp == "004B":
		dvList = ["abs"]
	colList = [orange[1], blue[1]]

	nBins= 100

	# Data processing:
	dm = getDM.getDM(exp, onlyControl=True)
	
	if handle_side != None:
		dm = dm.select("handle_side == '%s'" % handle_side)
	letList = ["b", "a"]
	
	

	for sacc in ["1", "2"]:
		legendData = []
		colList = [orange[1],blue[1]]
		nPlot +=1

		for dvType in dvList:
			color = colList.pop()
		
			if dvType == "corr":
				dv = "endX%sCorrNormToHandle" % sacc
			else:
				dv = "endX%sNormToHandle" % sacc
		
			# dv must not contain ''s:
			on_dm = onObject.onObject(dm, sacc)
			
			if blinkRemov:
				on_dm = on_dm.select("n_blink == 0")		



			# Normalize:
			if withinize:
				norm_dm = on_dm.addField("newDV", dtype=float)
				norm_dm = norm_dm.withinize(dv, "newDV", ["gap", "handle_side"], whiten=False)
				#dv = "newDV"
			else:
				norm_dm = on_dm

			if trim:
				trim_dm = norm_dm.selectByStdDev(keys=[], dv = dv, thr=2.5)
				#trim_dm = trim_dm.select('saccLat1 > 150')
				#minDv = norm_dm[dv].mean() - .05
				#maxDv = norm_dm[dv].mean() + .05
				#trim_dm = norm_dm.select('newDV < %f' % maxDv) \
				#	.select('newDV > %f' % minDv)
			else:
				trim_dm = norm_dm


			nBins = int(len(trim_dm)/50)
			#nBins = 10
	
			samp = trim_dm[dv]
	
			ax = plt.subplot(nRows, nCols, nPlot)
			
			if dvType == "abs":
				plt.axvline(0, linestyle = "--", color = gray[3])

			if exp == "004A" and dv == "endX%sNormToHandle" % sacc:
				plt.title('%s) Saccade %s' % (letList.pop(), sacc))
	
			a, edges = np.histogram(samp, bins = nBins)

			# Normalise:
#			a = abs(a)
#			
#			k = 3
#			maxVal = a.mean() + a.std() * k
#			i = np.where(a > maxVal)
#			a[i] = maxVal
#			
#			_min = float(np.min(a))
#			_max = float(np.max(a))
#			
#			y = (a-_min)/(_max-_min)
			
			y = a			
			
			x = .5*edges[1:] + .5*edges[:-1]
			
			if sacc == "1":
				plt.ylabel("Normalised frequency")
			else:
				ax.yaxis.set_ticklabels([])			
			if withMarker:
				data = plt.plot(x, y, color = color, marker = ".", \
					markeredgecolor = color, markeredgewidth=1,\
					markerfacecolor = "white", alpha = .5)
			else:
				data = plt.plot(x, y, color = color)
			legendData.append(data)
			#plt.xlim([-.7, .7])
			plt.xlabel("Normalised landing position")
			#plt.ylim([0,1.1])
	
	if exp == "004A":
		if sacc == "1":
			plt.legend(legendData, ["Absolute center", "CoG"], \
				frameon = False, loc='best')			
	plt.savefig(os.path.join(dst, "%s.png" % figName))
	plt.show()
if __name__ == "__main__":

	#for handle_side in ["left", "right", None]:
	for withinize in [True]:# , False]:	
		for exp in ["004B"]:
			distr(exp=exp, handle_side = None, withinize = withinize)
		