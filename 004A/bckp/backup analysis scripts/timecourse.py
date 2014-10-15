#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: timecourse.py

"""
DESCRIPTION:
Does tendency to land towards CoG fade over time?

TODO:
Check verbose!
"""


# Import Python modules:
import numpy as np
import os
import sys
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import scipy

# Import own modules:
from exparser.DataMatrix import DataMatrix
from exparser.PivotMatrix import PivotMatrix
from exparser.AnovaMatrix import AnovaMatrix
import getDM
import saccLat
import twoWayAnova

dst = "/home/lotje/Documents/PhD Marseille/Studies/004 - One-object experiment - Orienation effect/Analysis/plots/analyses discussed with francoise 22-07-2013"

plt.rc("font", family="ubuntu")
plt.rc("font", size=10)

def onObject(dm, landVar, verbose = True):
	
	"""
	Selects only valid, on-object landing positions for a given variable (e.g. 'endX1NormToHandle')
	"""
	
	dm = dm.select("%s != ''" % landVar, verbose = verbose)
	dm = dm.select("%s >= -.5" % landVar, verbose = verbose)
	dm = dm.select("%s <= .5" % landVar, verbose = verbose)
	
	return dm

def twoWay(dm, factor1, factor2, figTitle = True, addStats = True):
	
	"""
	NOTE: sacc 3 is not possible
	"""
	
	if (factor2 == "contrast_side" or factor2 == "mask_side") or (factor1 == "contrast_side" or factor1 == "mask_side"):
		onlyControl = False
	else:
		onlyControl = True
	
	exp = dm['exp'][0]
	
	figList = []
	
	for saccCount in ["1", "2"]:
		
		print '\n\t\tsacc count = %s\n'% saccCount
		
		if exp == "004A":
			dvList = ["endX%sNorm" % saccCount, "endX%sCorrNorm" % saccCount]
		if exp == "004B":
			dvList = ["endX%sNorm" % saccCount]
		
		for landVar in dvList:
			
			print '\n\tdv = %s\n' % landVar
			
			dv_dm = onObject(dm, landVar)
	
			fig = twoWayAnova.twoWayAnova(dv_dm, landVar, factor1, factor2, onlyControl = onlyControl, \
				figTitle = figTitle, addStats = addStats)
			figList.append(fig)
			plt.savefig( os.path.join(dst, "Interaction %s and %s on %s exp %s.png" % \
				(factor1, factor2, landVar, exp)) )
			
	return figList

def saccLats(dm):
	
	"""
	"""
	
	# Absolute saccade latencies as a function of gap manipulation and
	# contrast manipulation
	
	figList = []
	
	for saccCount in ["1", "2"]:
		print "sacc count = ", saccCount
		
		fig = saccLat.contrastEffect(dm, saccCount)
		plt.savefig(os.path.join(dst,\
			"Dist hist sacc latencies sacc %s exp %s as a function of gap and contrast manipulation.png" % (saccCount, exp)))
		figList.append(fig)

	return figList

def distHistPos(dm):
	
	"""
	"""
	
	start_dm = dm.select("contrast_side == 'control'")
	
	exp = dm["exp"][0]
	
	fig = plt.figure()
	title = "Dist hist landing positions per handle side exp %s" % exp
	plt.suptitle(title)
	plt.subplots_adjust(hspace = .3, wspace = .3)
	handleList = ["left", "right"]
	
	colCount = 0
	for saccCount in ["1", "2", "3"]:
		
		print "\n\tsacc count = %s\n" % saccCount
		
		sacc_dm = onObject(start_dm, 'endX%sNorm' % saccCount)
		
		if exp == "004A":
			dvList = ["endX%sNorm" % saccCount, "endX%sCorrNorm" % saccCount]
		else:
			dvList = ["endX%sNorm" % saccCount]
		
		plotCount = 0
		
		for dv in dvList:
			
			print "\n\tDV = %s\n" % dv
			
			plt.subplot2grid((2,3), (plotCount, colCount))
			colList = ["#3465a4", "#f57900"]
			
			# Dist hist landing positions as a function of handle:
			for handle in handleList:
				
				print "handle = %s" % handle
				handle_dm = sacc_dm.select("handle_side == '%s'" % handle)
				plt.hist(handle_dm[dv], color = colList.pop(), bins = 50, alpha = .3)
				plt.xlim(-.5, .5)
			plotCount +=1
			plt.xlabel(dv)
		colCount +=1
			
	plt.legend(handleList, loc = 'best')
	plt.savefig(os.path.join(dst, '%s.png' %title))
	
	return fig

def distHistToHandle(dm, trim = True):
	
	"""
	"""
	
	start_dm = dm.select("contrast_side == 'control'")
	
	exp = dm['exp'][0]
	
	fig = plt.figure()
	plt.subplots_adjust(hspace = .3, wspace = .3)
	
	title = "Dist hist of landing position towards handle exp %s (positive = towards, negative = away)" % exp
	plt.suptitle(title)
	colCount = 0
	
	for saccCount in ["1", "2", "3"]:
		print "\n\tsacc count = %s\n" % saccCount
	
		plotCount = 0
		
		if exp == "004A":
			dvList = ["endX%sNormToHandle" % saccCount, "endX%sCorrNormToHandle" % saccCount]
		else:
			dvList = ["endX%sNormToHandle" % saccCount]
		
		for dv in dvList:
			
			print "DV = %s" % dv
			
			dm = onObject(start_dm, dv)
			
			plt.subplot2grid((2,3), (plotCount, colCount))
			
			plt.hist(dm[dv], color = "#3465a4", bins = 50, alpha = .3)
			plt.xlim(-.5, .5)
			plt.xlabel(dv)
			plt.axvline(0, linestyle = "--", color = "#555753", linewidth = 3)
			
			plotCount +=1
		colCount +=1
		
	plt.savefig(os.path.join(dst, '%s.png'%title))
	
	return fig

def regrAn(dm, trim = True):
	
	"""
	NOTE: across-subjects!
	"""
	
	start_dm = dm.select("contrast_side == 'control'")
	
	exp = dm['exp'][0]
	
	figList = []
	
	for saccCount in ["1", "2", "3"]:
		
		print "\n\tsacc count = %s\n" % saccCount
	
		title = "Landing positions as a function of latency of saccade %s exp %s" % (saccCount, exp)
		fig = plt.figure()
		plt.suptitle(title)
		plt.subplots_adjust(hspace = .4)

		
		plotCount = 1
		if exp == "004A":
			dvList = ["endX%sNormToHandle" % saccCount, "endX%sCorrNormToHandle" % saccCount]
		else:
			dvList = ["endX%sNormToHandle" % saccCount]
		
		for dv in dvList:
			
			print "\n\tDV = %s\n" % dv
			
			dv_dm = onObject(start_dm, dv)
			
			xLabel = 'saccLat%s' % saccCount
			yLabel = dv
			
			if trim:
				# Exclude extreme sacc lats: TODO: SHould I do this?
				trimmed_dm = dv_dm.selectByStdDev(keys = ["file"], dv = xLabel)
			else:
				trimmed_dm = dv_dm
				
			iv = trimmed_dm[xLabel]
			dv = trimmed_dm[dv]
			plt.subplot(2,1,plotCount)
			fit = scipy.polyfit(iv, dv,1)
			fit_fn = scipy.poly1d(fit)

			slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(iv,dv)
			stats = "slope = %.2f, intercept = %.2f, R = %.2f, p = %.3f, SE = %.2f" \
				% (slope, intercept, r_value, p_value, std_err)
			plt.title(stats)
			plt.plot(iv, dv, 'yo', iv, fit_fn(iv), '--k')
			plt.axhline(0, color = "#555753", linestyle = "--", linewidth = 2)
			plotCount +=1
			plt.ylabel(yLabel)
			plt.xlabel(xLabel)
		plt.savefig(os.path.join(dst, '%s.png'%title))
		
		figList.append(fig)
		
	return figList

def binLat(dm, cousineau = True,nBin = 8, direction = "ToHandle", trim = False, figTitle = True):
	
	"""

	Argument:
	dm		--- data matrix
	
	Keyword argument:
	cousineau		--- withinize or not. Default = True.
	direction		--- {"toHandle", "toContrast"
	"""
	
	print '\n\tdirection = %s \n' % direction
	
	if direction == "ToHandle":
		start_dm = dm.select("contrast_side == 'control'")
	if direction == "ToContrast":
		start_dm = dm.select("contrast_side != 'control'")
	
	exp = start_dm['exp'][0]
	
	figList = []

	if exp == "004A":
		corrList = ["uncorrected", "corrected"]
	if exp == "004B":
		corrList = ["uncorrected"]
	
	for corr in corrList:
		colList = ["#73d216","#3465a4","#f57900"]
		
		fig = plt.figure(figsize = (3,7))
		title = "Landing (%s) %s as a function of binned sacc lats exp %s cousineau = %s trim = %s" % (corr, direction, exp, cousineau, trim)
		
		if figTitle:
			plt.title(title)
		
		for saccCount in ["1", "2", "3"]:
			
			print '\n\tsacc count = %s\n' % saccCount
			
			if corr == "uncorrected":
				dv = "endX%sNorm%s"%(saccCount, direction)
			elif corr == "corrected":
				dv = "endX%sCorrNorm%s"%(saccCount, direction)
				
			print "\tDV = %s\n" % dv

			dv_dm = onObject(start_dm,dv)
			
			saccLat = "saccLat%s" % saccCount
			
			# Trim the data matrix such that the most extreme latencies are excluded:
			if trim:
				trimmed_dm = dv_dm.selectByStdDev(keys = ["file"], dv = saccLat)
			else:
				trimmed_dm = dv_dm
			
			# Withinize sacc latencies, if wanted:
			print "\n\tcousineau = %s\n" % cousineau
			if cousineau:
				
				_dm = trimmed_dm.addField("cousineau_%s"%saccLat, dtype = None)
				_dm = _dm.withinize(saccLat, "cousineau_%s"%saccLat, "file", verbose = True, whiten=False)
				saccLat = "cousineau_%s"%saccLat
			else:
				_dm = dv_dm
				
			col = colList.pop()
			
			# Make bins, only for the first dv (for the second dv, the binned variable is the same and
			# therefore already exists:
			varToBin = saccLat
			binnedVar = "binnend%s" % varToBin
			binned_dm = _dm.addField(binnedVar)
			binned_dm = binned_dm.calcPerc(varToBin, binnedVar ,keys = ["file"], nBin = nBin)
			
			lX = []
			lY = []
			
			for _bin in binned_dm.unique(binnedVar):  
			
			# Filter out all but one bin
				dm_one_bin = binned_dm.select('%s == %f' % (binnedVar, _bin))
		
				# Get the mean sacc lat and the mean landing position (for x and y axis, respectively):
				# NOTE: withinising doesn't make any real difference for the overall pattern. 
		
				yMean = dm_one_bin[dv].mean()
				xMean = dm_one_bin[varToBin].mean()
				
				lX.append(xMean)
				lY.append(yMean)
			
			
			plt.plot(lX, lY, color = col, marker = 'o')
			plt.xlabel("binned saccade latencies from stimulus onset")
			plt.ylabel("landing position (%s) %s" % (corr,direction))
			
			# Disadvantages of pm: 
				# - There SHOULD be enough observations per participant to be able to plot
				# - bin number (instead of bin mean) on x axis
			#pm = PivotMatrix(_dm, "binned%s" % varToBin, "file", dv, colsWithin = True)
			#pm.plot(nLvl1=1, fig = fig, colors = col, \
			#	xLabel = "binned sacc lat", yLabel = "Landing pos towards handle")
		plt.ylim(-.2, .2)
		plt.axhline(0, color = "#555753", linestyle = "--", linewidth = 2)
		plt.legend(["sacc 1", "sacc 2", "sacc 3"])
		plt.savefig(os.path.join(dst,'%s.png' % title))
		
		figList.append(fig)
		
	return figList


def allSaccLats(dm, direction, figTitle = True, trim = True, cousineau = True, nBin = 15, usePm = True, err = 'se'):
	
	"""
	Throw all saccades latencies (since stim onset) in for bin analysis, irrespective of saccade count
	
	Arguments:
	dm
	direction --- {"ToHandle", "ToContrast"}, variable on the y axis
	
	Keyword arguments:
	
	Returns fig list
	
	
	"""
	figList = []
	print '\n\tdirection = %s \n' % direction
	
	if direction == "ToHandle":
		start_dm = dm.select("contrast_side == 'control'")
	if direction == "ToContrast":
		start_dm = dm.select("contrast_side != 'control'")
	
	exp = start_dm['exp'][0]
	
	lDm = []
	
	if exp == "004A":
		# Max sacc count = 4
		lSacc = range(1,5)
	if exp == "004B":
		# Max sacc count = 3
		lSacc = range(1,4)
		
	for saccCount in lSacc:
		
		# Create dms containing all latencies (i.e., the to-be-binned variable) 
		# of a given saccade count, e.g.
		# almost all trials for the first saccade, and less and less for the
		# subsequent saccades.
		# Do the same for the landing positions (dv's on the y-axis):
		
		# Select one saccade:
		dm_sacc = dm.select("saccLat%s != ''" % str(saccCount))
		
		# Create new column containing sacc count:
		dm_sacc = dm_sacc.addField("saccNr", dtype = str)
		dm_sacc["saccNr"] = "sacc%s" % saccCount
		
		# Create new column containing IV and DV's, but without the
		# sacc count in the column header:
		dm_sacc = dm_sacc.addField("absSaccLat", dtype = float)
		dm_sacc["absSaccLat"] = dm_sacc["saccLat%s" % str(saccCount)]
		
		dm_sacc = dm_sacc.addField("abs%s" % direction, dtype = float)
		dm_sacc["abs%s" % direction] = dm_sacc["endX%sNorm%s"%(str(saccCount), direction)]
		
		dm_sacc = dm_sacc.addField("absCorr%s" % direction, dtype = float)
		dm_sacc["absCorr%s" % direction] = dm_sacc["endX%sCorrNorm%s"%(str(saccCount), direction)]
		
		# Add the dm to the list of dm's
		lDm.append(dm_sacc)

	# Combine all dm's into one big dm:
	merged_dm = lDm[0]
	
	for dm in lDm[1:]:
		merged_dm = merged_dm + dm
	
		corrList = ["corrected", "uncorrected"]
	
	for corr in corrList:
	
		fig = plt.figure(figsize = (3,7))
		title = "Landing (%s) %s as a function of ALL binned sacc lats exp %s cousineau = %s trim = %s usePm = %s" \
			% (corr, direction, exp, cousineau, trim, usePm)
			
		if figTitle:
			plt.title(title)
			
		if corr == "uncorrected":
			dv = "abs%s" % direction
		elif corr == "corrected":
			dv = "absCorr%s" % direction
			
		print "\tDV = %s\n" % dv
		
		# There should be no ''s in the dm anymore, but off-object saccades are still
		# possible, so this filtering remains necessary:
		dv_dm = onObject(merged_dm,dv)
			
		saccLat = "absSaccLat"

		# Trim the data matrix such that the most extreme latencies are excluded:
		print "\n\ttrim = %s\n" % trim
		if trim:
			trimmed_dm = dv_dm.selectByStdDev(keys = ["file"], dv = saccLat)
		else:
			trimmed_dm = dv_dm
		
		# Withinize sacc latencies, if wanted:
		print "\n\tcousineau = %s\n" % cousineau
		if cousineau:
			
			_dm = trimmed_dm.addField("cousineau_%s"%saccLat, dtype = None)
			_dm = _dm.withinize(saccLat, "cousineau_%s"%saccLat, "file", verbose = True, whiten=False)
			saccLat = "cousineau_%s"%saccLat
		else:
			_dm = dv_dm
				
		# Make bins, only for the first dv (for the second dv, the binned variable is the same and
		# therefore already exists:
		varToBin = saccLat
		binnedVar = "binnend%s" % varToBin
		binned_dm = _dm.addField(binnedVar)
		binned_dm = binned_dm.calcPerc(varToBin, binnedVar ,keys = ["file"], nBin = nBin)
		
		if not usePm:
			
			lX = []
			lY = []
			
			for _bin in binned_dm.unique(binnedVar):  
			
			# Filter out all but one bin
				dm_one_bin = binned_dm.select('%s == %f' % (binnedVar, _bin))
		
				# Get the mean sacc lat and the mean landing position (for x and y axis, respectively):
				# NOTE: withinising doesn't make any real difference for the overall pattern. 
		
				yMean = dm_one_bin[dv].mean()
				xMean = dm_one_bin[varToBin].mean()
				
				lX.append(xMean)
				lY.append(yMean)
			
			
			plt.plot(lX, lY, color = "#3465a4", marker = 'o')
			plt.xlabel("binned saccade latencies from stimulus onset")
			plt.ylabel("landing position (%s) %s" % (corr,direction))
			plt.ylim(-.2, .2)
			plt.axhline(0, color = "#555753", linestyle = "--", linewidth = 2)
			plt.savefig(os.path.join(dst,'%s.png' % title))
		
		if usePm:
			
			pm = PivotMatrix(binned_dm, binnedVar, "file", dv, colsWithin = True, err = 'se')
			#pm.plot(nLvl1=1, fig = fig, xLabel = "binned saccade latencies from stimulus onset", \
			#	yLabel = "landing position (%s) %s" % (corr,direction))
			
			pm.barPlot(fig = fig, xLabel = "binned saccade latencies from stimulus onset", \
				yLabel = "landing position (%s) %s" % (corr,direction))
			
			plt.ylim(-.2, .2)
			plt.axhline(0, color = "#555753", linestyle = "--", linewidth = 2)
			plt.savefig(os.path.join(dst,'%s.png' % title))
			
			plt.savefig(os.path.join(dst,'%s.png' % title))
			
		
		figList.append(fig)

	return figList


def runAnalyses():
	
	"""
	Just made this a function so that I can more easily go here via the 
	'Symbol List'
	"""
	
	pp = PdfPages('Time course landing positions.pdf')
			
	
	for exp in ["004A", "004B"]:
		
		print "EXPERIMENT = ", exp

		# Get original dm (copies are used for the subanalyses below):
		main_dm = getDM.getDM(exp = exp, driftCorr = True)
		
		# Step 7:
		# Throw all saccade latencies (from stim onset) in, irrespective of saccade count.
		print "\n\n\t\t\tSTEP 7\n\n"
		
		for direction in ["ToHandle", "ToContrast"]:
			figList = allSaccLats(main_dm, "ToHandle")
			for fig in figList:
				pp.savefig(fig)
		
		##STEP 1: 
		##Landing positions as a function of contrast and handle, and gap and handle:
		#print "\n\n\t\t\tSTEP 1\n\n"
		#for factor2 in ["contrast_side", "gap"]:
			#if factor2 == "contrast_side":
				#continue
			#figList = twoWay(main_dm, "contrast_side", factor2, figTitle = True, addStats = True)
			#for fig in figList:
				#pp.savefig(fig)

		##STEP 2: 
		##Dist hist of landing position separated by Handle Side:
		#print "\n\n\t\t\tSTEP 3\n\n"
		#fig = distHistPos(main_dm)
		#pp.savefig(fig)
		

		##STEP 3:
		##Dist hist sacc latecnies:
		#print "\n\n\t\t\tSTEP 2\n\n"
		#figList = saccLats(main_dm)
		#for fig in figList:
			#pp.savefig(fig)
			
		##STEP 4:
		##Plot variable indicating whether landing position is towards the handle or not.
		#print "\n\n\t\t\tSTEP 4\n\n"
		#fig = distHistToHandle(main_dm)
		#pp.savefig(fig)
		
		## STEP 5:
		##Regression analysis saccade latency and landing position. 
		#print "\n\n\t\t\tSTEP 5\n\n"
		#figList = regrAn(main_dm)
		#for fig in figList:
			#pp.savefig(fig)

		# STEP 6:
		#Bin latencies per participant and plot landing position as a function of bin
		#print "\n\n\t\t\tSTEP 6\n\n"
		#for direction in ["ToHandle", "ToContrast"]:
			#figList = binLat(main_dm, direction = direction, cousineau = True, figTitle = False)
			#for fig in figList:
				#pp.savefig(fig)

	pp.close()
	
if __name__ == "__main__":
	
	runAnalyses()