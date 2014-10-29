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
from exparser.CsvReader import CsvReader
import getDM
import onObject

# Set font.
# For guidelines, see:
# http://www.journalofvision.org/site/misc/peer_review.xhtml#style
plt.rc("font", family="arial")
plt.rc("font", size=7)

# Some constant vars:
dst = "/home/lotje/Studies/004 - Single-object experiment - Handle-orientation effect/manuscript/Versions/5th draft/Figures JoV"

src_sal = 'selected_dm_004C_WITH_drift_corr.csv'
dm_sal = CsvReader(src_sal).dataMatrix()
sal_peak= dm_sal["endX1NormToHandle"].mean()




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



def distr(dm, dv, saccVar, trim=True, withinize=True, binSize = 50, \
	col = blue[1], perBin=True, perPp = False):
	
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
	
	if perBin == True and perPp == True:
		print "Per bin AND per pp is not possible"
		return
	
	if "1" in saccVar:
		sacc = "1"
	elif "2" in saccVar:
		sacc = "2"
	
	# landing position should not be "":
	dm = onObject.onObject(dm, sacc)	

	# Exclude outliers sacc lat:
	dm = dm.selectByStdDev(keys=["file"], dv = saccVar)

	# Remove outliers landing position:
	dm= dm.removeField("__dummyCond__")
	dm= dm.removeField("__stdOutlier__")
	dm = dm.selectByStdDev(keys=["file"], dv =dv)

	# Divide sacc latency into equal bins:
	dm = dm.addField("binnedSaccLat")
	dm= dm.calcPerc(saccVar, "binnedSaccLat",keys = ["file"],\
		nBin = 3)
		
	colList = yellow + red + blue
	colList = [orange[1], green[1], blue[1]]
	#fig= plt.figure()
	
	if perBin:
		nBins = 15

		for _bin in dm.unique("binnedSaccLat"):
	
			_dm = dm.select("binnedSaccLat == %s" % _bin)
	
			# Normalize landing positions:
			_dm= _dm.addField("newLanding", dtype = float)
			_dm= _dm.withinize(dv, "newLanding", \
					["handle_side"], whiten=False)
	
			#samp = _dm["endX1NormToHandle"]
			samp = _dm["newLanding"]
	
			y, edges = np.histogram(samp, bins = nBins)
			y = normY(y)
					
			x = .5*edges[1:] + .5*edges[:-1]
			col = colList.pop()
			plt.plot(x, y, 'o-', color = col, markeredgecolor = col,\
				markerfacecolor = "white", markeredgewidth = 1)
			#plt.show()

	if perPp:

		nBins = 9
		fig = plt.figure()
		plt.subplots_adjust(hspace=.6)
		nRows = 5
		nCols = 4
		nPlot = 0
		
		for pp in dm.unique("file"):
			nPlot +=1
			plt.subplot(nRows, nCols, nPlot)
	
			_dm = dm.select("file == '%s'" % pp)
			plt.title("M lat = %s" % int(_dm[saccVar].mean()))
	
			samp = _dm[dv]
	
			y, edges = np.histogram(samp, bins = nBins)
			y = normY(y)
					
			x = .5*edges[1:] + .5*edges[:-1]

			plt.plot(x, y, 'o-', color = col, markeredgecolor = col,\
				markerfacecolor = "white", markeredgewidth = 1)

			plt.ylim([0,1.1])
			plt.xlim([-.7, .7])
		#plt.show()
		

	if not perPp and not perBin:
		
		nBins=45
		samp = dm[dv]

		y, edges = np.histogram(samp, bins = nBins)
		y = normY(y)
				
		x = .5*edges[1:] + .5*edges[:-1]
		col = colList.pop()
		plt.plot(x, y, 'o-', color = col, markeredgecolor = col,\
			markerfacecolor = "white", markeredgewidth = 1)

		
	plt.ylim([0,1.1])
	plt.xlim([-.7, .7])
	
if __name__ == "__main__":

	perBin = False
	perPp = True

	for exp in ["004A", "004B"]: #, "004B"]:
		legend = True
		# Data processing:
		src = 'selected_dm_%s_WITH_drift_corr.csv' % exp
		main_dm = CsvReader(src).dataMatrix()

		nCols = 2
		if exp == "004B":
			nRows = 1
			fig = plt.figure(figsize = (8, 3))
			plt.subplots_adjust(wspace=0, hspace = 0.2, left = .2, bottom = .15)
			plt.suptitle("Experiment 2")
		if exp == "004A":
			nRows = 2
			fig = plt.figure(figsize = (8,6))
			plt.subplots_adjust(wspace=0, hspace = 0.2,\
				left = .2, bottom = .15)
			plt.suptitle("Experiment 1")

		nPlot = 0
		
		if exp == "004A":
			varList = ["absolute center", "CoG"]
		elif exp == "004B":
			varList = ["absolute center"]
		
		for dvType in varList:

			for sacc in ["1", "2"]:
			
				#colList = [orange[1], green[1], blue[1]]

				if dvType == "absolute center":
					dv = "endX%sNormToHandle" % sacc
				elif dvType == "CoG":
					dv = "endX%sCorrNormToHandle" % sacc
				
				if not perPp:
					continue
				else:
					distr(main_dm, dv, "saccLat%s" % sacc, \
						perPp=perPp, perBin=perBin)

					plt.savefig(os.path.join(dst,"Distr_PP_%s_%s.png" % \
						(exp, dv)))
				
				
				# Plot distr per saccade bin:
				nPlot +=1
				ax = plt.subplot(nRows, nCols, nPlot)
				plt.title("Landing position %s: relative to %s" % \
					(sacc, dvType))
				distr(main_dm, dv, "saccLat%s" % sacc, \
					perBin=perBin)
				
				if legend:
					plt.legend(["Fast", "Medium", "Slow"],loc='best')
					legend=False

				if sacc == "2":
					ax.yaxis.set_ticklabels([])
				elif sacc == "1":
					plt.ylabel("Normalized frequency")
				if exp == "004A":
					if dvType == "absolute center":
						ax.xaxis.set_ticklabels([])
					elif dvType == "CoG":
						plt.xlabel("Normalized gaze bias")
				if exp == "004B":
					plt.xlabel("Normalized gaze bias")
				
					
				plt.axvline(0, linestyle = "--", color = gray[3])
		
		if not perPp:
			plt.savefig(os.path.join(dst,"Distr_%s_perBin_%s.png" % \
				(exp, perBin)))