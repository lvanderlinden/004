# Import Python modules:
import numpy as np
import os
import sys
from matplotlib import pyplot as plt

# Import own modules:
from exparser.DataMatrix import DataMatrix
from exparser.PivotMatrix import PivotMatrix
from exparser.AnovaMatrix import AnovaMatrix
import getDM

def landHandle(dm, nRows = 5, nCols = 2, dvLand = 'endX1Norm', addStats = True):
	
	"""
	"""
	
	# Define keys:
	factors = ["handle_side", "contrast_side"]
	pp = ["file"]
	dv = dvLand
	
	exp = dm["exp"][0]
	
	# Exclude trials on which the dv does not exist:
	dm = dm.select("%s != ''"%dvLand)
	
	# TODO: This doesn't work for experiment 2!!
	# Only on-object eye movements:
	dm = dm.select('endX1Norm < .5')
	dm = dm.select('endX1Norm > -.5')
	
	# Apply selections:
	dm = dm.selectByStdDev(keys = factors + pp, dv = dv)
	
	# Create figure:
	fig = plt.figure()
	figName = "%s: Landing position (%s) as a function of Handle and Mask" % (exp, dvLand)
	plt.suptitle(figName)
	nPlots = 0
	
	contrastList = ["_left", "control", "right"]
	for contrast in contrastList:
		
		colList = ['#f57900', '#3465a4']
		
		vf_dm = dm.select("contrast_side == '%s'" % contrast)
		
		#plt.subplot(nRows, nCols, nPlots)
		plt.subplot2grid((nRows,nCols), (nPlots, 0))
		

		handleList = ["left", "right"]
		for handle in handleList:
			
			plt.subplots_adjust(hspace = 0)
			#plt.title("most contrast = %s" % contrast)
			col = colList.pop()
			gap_dm = vf_dm.select("handle_side == '%s'" % handle)
			plt.hist(gap_dm[dv], bins = 30, color = col, alpha = .3)
			plt.xlim(-.5, .5)
			plt.axvline(0, color = "#555753", linewidth = 2, linestyle = '--')
			plt.ylabel(contrast)
			
		if contrast == contrastList[-1]:
			plt.xlabel('initial-saccade landing position')
		else:
			plt.xticks([])
		nPlots +=1
	plt.subplots_adjust(hspace = .6, wspace = .4)
	plt.subplot2grid((nRows,nCols), (0, 1), rowspan=3)
	pm = PivotMatrix(dm, factors, pp, dv, colsWithin = True)
	pm.linePlot(fig = fig, legendTitle = "handle side")
	plt.axhline(0, color = "#555753", linestyle = "--", linewidth = 1.5)
	plt.ylabel("Intial-saccade landing position")
	plt.ylim(-.5,.5)
	am = AnovaMatrix(dm, factors = factors, dv = dv, \
		subject = pp[0])._print(maxLen=10, ret=True)
	plt.subplot2grid((nRows,nCols), (3, 0), colspan=2, rowspan = 2)
	plt.text(0.1,0.05,am, family='monospace')
	plt.savefig("%s.png"%figName)
	#plt.show()

def landWithoutContrast(factor = ["handle_side"], nRows = 3, nCols = 4, saccNr = "1", \
	yLim = [-.05, .05], pp = ["file"], addStats = True, figTitle = True):
	
	"""
	Plots effect of handle side on landing-position variable. Only trials without
	contrast manipulation are included.
	
	Arguments:
	dm
	
	Keyword arguments:
	saccNr		--- nth saccade of interest (default = first, "1")
	addStats	--- if False, only 3 plots
	figTitle	--- if False, ugly but informative title is not added
	"""

	if not addStats:
		nCols = 1
		fig = plt.figure(figsize = (3,7))
		plt.subplots_adjust(hspace = .25)
		
	else:
		fig = plt.figure()
		plt.subplots_adjust(hspace = .5)
		
	# Create figure:
	figName = "Landing position as a function of %s - saccNr = %s"%(factor[0],saccNr)
	if figTitle:
		plt.suptitle(figName)
	plotCount = 0
	
	# Experiment 004A:
	exp = "004A"
	dm1 = getDM.getDM(exp = exp, driftCorr = True)
	
	# Only use objects without contrast manipulation
	dm1 = dm1.select("mask_side == 'control'", verbose = False)
	
	dm_temp = dm1
	

		
	for dv in ["endX%sNorm" % saccNr, "endX%sCorrNorm" % saccNr]:
		
		if "Corr" in dv:
			subTitle = "Landing pos Exp 1 corrected"
		else:
			subTitle = "Landing pos Exp 1 uncorrected"
		
		_dm = dm1

		# Only trials where variable has a value:
		_dm = _dm.select("%s != ''"%dv)
		
		# Only on-object eye movements:
		_dm = _dm.select('endX%sNorm < .5' % saccNr)
		_dm = _dm.select('endX%sNorm > -.5' % saccNr)
	
		# Trim:
		_dm = _dm.selectByStdDev(keys = factor + pp, dv = dv)
		
		
		plt.subplot2grid((nRows,nCols), (plotCount, 0))
		plt.title(subTitle)
		pm = PivotMatrix(_dm, factor, pp, dv, colsWithin = True)
		plt.axhline(0, linestyle = "--", color = "#555753")
		plt.ylim(yLim)
		pm.barPlot(fig=fig)
		
		if addStats:
			am = AnovaMatrix(_dm, factors = factor, dv = dv, \
				subject = pp[0])._print(maxLen=7, ret=True)
			plt.subplot2grid((nRows,nCols), (plotCount, 1), colspan=3)
			plt.title("Exp = %s DV = %s" % (exp, dv))
			plt.text(0.05,0.1,am, family='monospace')
			plt.xticks([])
			plt.yticks([])
		plotCount +=1
	
	# For experiment 004B we plot only the normalised landing position.
	# Correcting for CoG doesn't make sense here!
	exp = "004B"
	
	# Get dm:
	dm2 = getDM.getDM(exp = exp, driftCorr = True)
	
	# Only trials without contrast manipulation:
	dm2 = dm2.select("mask_side == 'control'")
	
	# Only trials where variable has a value:
	dm2 = dm2.select("%s != ''"%dv)
	
	# Only on-object eye movements:
	dm2 = dm2.select('endX%sNorm < .5' % saccNr)
	dm2= dm2.select('endX%sNorm > -.5' % saccNr)
	
				 
	# Trim:
	dm2 = dm2.selectByStdDev(keys = factor + pp, dv = dv)
	
	# Pivot matrix and stats:
	dv = "endX%sNorm" % saccNr
	pm = PivotMatrix(dm2, factor, pp, dv = dv, colsWithin = True)
	plt.subplot2grid((nRows,nCols), (plotCount, 0))
	plt.title("Landing pos Exp 2")
			
	
	pm.barPlot(fig = fig)
	plt.axhline(0, linestyle = "--", color = "#555753")
	plt.ylim(yLim)
	plt.xlabel("Handle side")
	if addStats:
		am = AnovaMatrix(dm2, factors = factor, dv = dv, \
			subject = pp[0])._print(maxLen=7, ret=True)
		plt.subplot2grid((nRows,nCols), (plotCount, 1), colspan=3)
		plt.title("Exp = %s DV = %s" % (exp, dv))
		plt.text(0.05,0.1,am, family='monospace')
		plt.xticks([])
		plt.yticks([])
		  
	plt.savefig("%s.png"%figName)



if __name__ == "__main__":
	

	for saccNr in ("1", "2", "3"):
		
		#if saccNr != "3":
		#	continue
		
		yLim = [-.5, .5]
		
		#landWithoutContrast(factor = ["heavySide"], saccNr = saccNr, yLim = yLim)
		landWithoutContrast(factor = ["handle_side"], saccNr = saccNr, yLim = yLim, addStats = False, figTitle = False)
	
	sys.exit()
	
	
	for exp in ["004A", "004B"]:
		
		# Get dm:
		dm = getDM.getDM(exp = exp, driftCorr = True)

		# Only use handled objects:
		dm = dm.select("symm == 'asymm'")

		landHandle(dm, dvLand = 'endX2Norm')
		landHandle(dm, dvLand = 'endX1Norm')
		if exp == "004A":
			landHandle(dm, dvLand = 'endX1CorrNorm')
			landHandle(dm, dvLand = 'endX2CorrNorm')
			
	
		#landHandle(dm, dvLand = 'endX3Norm')
		#landHandle(dm, dvLand = 'endX3CorrNorm')
	

		#sys.exit()
	
	
	