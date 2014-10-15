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
import timecourse

plt.rc("font", family="ubuntu")
plt.rc("font", size=12)
	

def splitHeavy(factor = ["corrDirection", "handle_side"], nRows = 3, nCols = 4, saccNr = "1", \
	yLim = [-.5, .5], pp = ["file"], stats = True, colsWithin = True, sepPlots = True, exclY = True):
	
		# Create figure:
	# Experiment 004A:
	exp = "004A"
	dm1 = getDM.getDM(exp = exp, driftCorr = True)
	
	dm1 = dm1.select("corrDirection != 'correction smaller than 8'")
	
	for corr in dm1.unique("corrDirection"):
		print corr
		tmp = dm1.select("corrDirection == '%s'" % corr)
		print "Corr direction = ", corr
		print tmp.unique("object")

	
	# Only use objects without contrast manipulation
	dm1 = dm1.select("mask_side == 'control'", verbose = False)
	figList = []
	
	if not sepPlots:
		
		fig = plt.figure(figsize = (10,2))
		nRows = 1
		nCols = 3
		plotNr = 0
	
	for dv in ["endX%sNorm" % saccNr, "endX%sCorrNorm" % saccNr]:
		
		if sepPlots:
			
			fig = plt.figure(figsize = (10,3))
			figName = "split by heavy side exp %s dv %s colsWithin = %s - exclY = %s" % (exp, dv, colsWithin, exclY)
		
		else:
			plotNr +=1
			plt.subplot(nRows,nCols,plotNr)
			
		_dm = dm1

		# Only trials where variable has a value:
		_dm = _dm.select("%s != ''"%dv)
		
		# Only on-object EM's
		_dm = _dm.select('endX%sNorm < .5' % saccNr)
		_dm = _dm.select('endX%sNorm > -.5' % saccNr)
		
		if exclY:
			_dm = _dm.select('endY%sNorm < .5' % saccNr)
			_dm = _dm.select('endY%sNorm > -.5' % saccNr)
	
	
		# Trim:
		_dm = _dm.selectByStdDev(keys = factor + pp, dv = dv)
		
		
		#plt.subplot2grid((nRows,nCols), (plotCount, 0))
		pm = PivotMatrix(_dm, factor, pp, dv, colsWithin=colsWithin, err='se')
		#plt.axhline(0, linestyle = "--", color = "#555753")
		#plt.ylim(yLim)
		#pm.barPlot(fig=fig)
		
		pm.barPlot(fig = fig, _dir='right', legendTitle = "handle side")
		plt.axvline(0, linestyle = "--", color = "#555753")
		plt.axhline(0.5, linestyle = "-", color = "#555753")
		plt.xlim(yLim)
		
		if sepPlots:
			if "Corr" in dv:
				plt.xlabel("corrected horizontal landing position")
			else:
				plt.xlabel("horizontal landing position")
		else:
			plt.xticks([])
		if stats:
			am = AnovaMatrix(_dm, factors = factor, dv = dv, \
				subject = pp[0])._print(maxLen=7, ret=True)
			print am
		#plt.subplot2grid((nRows,nCols), (plotCount, 1), colspan=3)
		#plt.title("Exp = %s DV = %s" % (exp, dv))
		#plt.text(0.05,0.1,am, family='monospace')
		#plt.xticks([])
		#plt.yticks([])
		#plotCount +=1
		
		if sepPlots:
			plt.savefig("%s.svg"%figName)
			plt.savefig("%s.png"%figName)
			#plt.show()
			figList.append(fig)
		
	# For experiment 004B we plot only the normalised landing position.
	# Correcting for CoG doesn't make sense here!
	
	exp = "004B"

	# Get dm:
	dm2 = getDM.getDM(exp = exp, driftCorr = True)
	
	# Only trials without contrast manipulation:
	dm2 = dm2.select("mask_side == 'control'")
	dm2 = dm2.select("corrDirection != 'correction smaller than 8'")
	
	# Only trials where variable has a value:
	dm2 = dm2.select("%s != ''"%dv)
	
	# Only on-object eye movements:
	dm2 = dm2.select('endX%sNorm < .5' % saccNr)
	dm2= dm2.select('endX%sNorm > -.5' % saccNr)
	
	if exclY:
		dm2 = dm2.select('endY%sNorm < .5' % saccNr)
		dm2= dm2.select('endY%sNorm > -.5' % saccNr)
			
	
	# Pivot matrix and stats:
	dv = "endX%sNorm" % saccNr
				 
	# Trim:
	dm2 = dm2.selectByStdDev(keys = factor + pp, dv = dv)
	
	if sepPlots:
		fig = plt.figure(figsize = (10,3))
		figName = "split by heavy side exp %s dv %s colsWithin = %s" % (exp, dv, colsWithin)
	
	else:
		plt.subplot(nRows,nCols,3)

	pm = PivotMatrix(dm2, factor, pp, dv = dv, colsWithin = colsWithin, err = 'se')
	#plt.subplot2grid((nRows,nCols), (plotCount, 0))
	
	pm.barPlot(fig = fig, _dir='right')
	plt.axvline(0, linestyle = "--", color = "#555753")
	plt.axhline(0.5, linestyle = "-", color = "#555753")
	plt.xlim(yLim)
	if sepPlots:
		plt.xlabel("horizontal landing position")
	
	else:
		plt.xticks([])
	if stats:
		am = AnovaMatrix(dm2, factors = factor, dv = dv, \
			subject = pp[0])._print(maxLen=7, ret=True)
		print am
	#plt.subplot2grid((nRows,nCols), (plotCount, 1), colspan=3)
	#plt.title("Exp = %s DV = %s" % (exp, dv))
	#plt.text(0.05,0.1,am, family='monospace')
	#plt.xticks([])
	#plt.yticks([])
	
	if sepPlots:
		plt.savefig("%s.png"%figName)
		plt.savefig("%s.svg"%figName)
		
		figList.append(fig)
		
		return figList
	else:
		plt.savefig('per corrDir.png')
		return fig


def landWithoutContrast(factor = ["handle_side"], nRows = 3, nCols = 4, saccNr = "1", \
	yLim = [-.1, .1], pp = ["file"], stats = True, colsWithin = True, sepPlots = True, exclY = True):
	
	"""
	Plots effect of handle side on landing-position variable. Only trials without
	contrast manipulation are included.
	
	Arguments:
	dm
	
	Keyword arguments:
	saccNr		--- nth saccade of interest (default = first, "1")
	sepPlots	--- save and return as separate plots or as subplots of one main figure
	"""

	# Create figure:
	# Experiment 004A:
	exp = "004A"
	dm1 = getDM.getDM(exp = exp, driftCorr = True)
	
	# Only use objects without contrast manipulation
	dm1 = dm1.select("mask_side == 'control'", verbose = False)
	figList = []
	
	if not sepPlots:
		
		fig = plt.figure(figsize = (10,2))
		nRows = 1
		nCols = 3
		plotNr = 0
	
	for dv in ["endX%sNorm" % saccNr, "endX%sCorrNorm" % saccNr]:
		
		if sepPlots:
			
			fig = plt.figure(figsize = (10,3))
			figName = "exp %s dv %s colsWithin = %s - exclY = %s" % (exp, dv, colsWithin, exclY)
		
		else:
			plotNr +=1
			plt.subplot(nRows,nCols,plotNr)
			
		_dm = dm1

		# Only trials where variable has a value:
		_dm = _dm.select("%s != ''"%dv)
		
		# Only on-object EM's:
		_dm = _dm.select('endX%sNorm < .5' % saccNr)
		_dm = _dm.select('endX%sNorm > -.5' % saccNr)

		if exclY:
			_dm = _dm.select('endY%sNorm < .5' % saccNr)
			_dm = _dm.select('endY%sNorm > -.5' % saccNr)
		
	
		# Trim:
		_dm = _dm.selectByStdDev(keys = factor + pp, dv = dv)
		
		
		#plt.subplot2grid((nRows,nCols), (plotCount, 0))
		pm = PivotMatrix(_dm, factor, pp, dv, colsWithin=colsWithin, err='se')
		#plt.axhline(0, linestyle = "--", color = "#555753")
		#plt.ylim(yLim)
		#pm.barPlot(fig=fig)
		
		pm.barPlot(fig = fig, _dir='right')
		plt.axvline(0, linestyle = "--", color = "#555753")
		plt.axhline(0.5, linestyle = "-", color = "#555753")
		plt.xlim(yLim)
		
		if sepPlots:
			if "Corr" in dv:
				plt.xlabel("corrected horizontal landing position")
			else:
				plt.xlabel("horizontal landing position")
		else:
			plt.xticks([])
		if stats:
			am = AnovaMatrix(_dm, factors = factor, dv = dv, \
				subject = pp[0])._print(maxLen=7, ret=True)
			print am
		#plt.subplot2grid((nRows,nCols), (plotCount, 1), colspan=3)
		#plt.title("Exp = %s DV = %s" % (exp, dv))
		#plt.text(0.05,0.1,am, family='monospace')
		#plt.xticks([])
		#plt.yticks([])
		#plotCount +=1
		
		if sepPlots:
			plt.savefig("%s.svg"%figName)
			plt.savefig("%s.png"%figName)
			#plt.show()
			figList.append(fig)
		
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
	
	if exclY:
		dm2 = dm2.select('endY%sNorm < .5' % saccNr)
		dm2= dm2.select('endY%sNorm > -.5' % saccNr)
			
				 
	# Pivot matrix and stats:
	dv = "endX%sNorm" % saccNr


	# Trim:
	dm2 = dm2.selectByStdDev(keys = factor + pp, dv = dv)
	
	if sepPlots:
		fig = plt.figure(figsize = (10,3))
		figName = "exp %s dv %s colsWithin = %s - exclY = %s" % (exp, dv, colsWithin, exclY)
	
	else:
		plt.subplot(nRows,nCols,3)

	pm = PivotMatrix(dm2, factor, pp, dv = dv, colsWithin = colsWithin, err = 'se')
	#plt.subplot2grid((nRows,nCols), (plotCount, 0))
	
	pm.barPlot(fig = fig, _dir='right')
	plt.axvline(0, linestyle = "--", color = "#555753")
	plt.axhline(0.5, linestyle = "-", color = "#555753")
	plt.xlim(yLim)
	if sepPlots:
		plt.xlabel("horizontal landing position")
	
	else:
		plt.xticks([])
	if stats:
		am = AnovaMatrix(dm2, factors = factor, dv = dv, \
			subject = pp[0])._print(maxLen=7, ret=True)
		print am
	#plt.subplot2grid((nRows,nCols), (plotCount, 1), colspan=3)
	#plt.title("Exp = %s DV = %s" % (exp, dv))
	#plt.text(0.05,0.1,am, family='monospace')
	#plt.xticks([])
	#plt.yticks([])
	
	if sepPlots:
		plt.savefig("%s.png"%figName)
		plt.savefig("%s.svg"%figName)
		
		figList.append(fig)
		
		return figList
	else:
		return fig

def landAllSaccs(yLim = [-.05, .05], pp = ["file"], colsWithin = True, figTitle = True, spacing = .5):
	
	"""
	Plots effect of handle side on landing-position variable. Only trials without
	contrast manipulation are included.
	
	Arguments:
	dm
	
	"""

	# Create figure:
	# Experiment 004A:
	exp = "004A"
	dm1 = getDM.getDM(exp = exp, driftCorr = True)
	
	# Only use objects without contrast manipulation
	dm1 = dm1.select("mask_side == 'control'", verbose = False)
	figList = []
	
	fig = plt.figure(figsize = (4,8))
	#fig = plt.figure()
	colList = ["#f57900", "#73d216", "#3465a4"]
	
	for saccNr in ["1", "2", "3"]:

		lMeans = []
		for dv in ["endX%sNormToHandle" % saccNr, "endX%sCorrNormToHandle" % saccNr]:
			
			_dm = dm1

			# Only trials where variable has a value:
			_dm = _dm.select("%s != ''"%dv)
			
			# Only on-object eye movements:
			_dm = _dm.select('endX%sNorm < .5' % saccNr)
			_dm = _dm.select('endX%sNorm > -.5' % saccNr)
		
			# Trim:
			_dm = _dm.selectByStdDev(keys = pp, dv = dv)
			
			m = np.mean(_dm[dv])
			print 'sacc = %s exp = %s dv = %s' % (saccNr, exp, dv)
			print 'MEAN = ', m
			lMeans.append(m)
		
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
		dm2 = dm2.selectByStdDev(keys = pp, dv = dv)
		
		# Pivot matrix and stats:
		dv = "endX%sNormToHandle" % saccNr
		
		m = np.mean(dm2[dv])
		print 'sacc = %s exp = %s dv = %s' % (saccNr, exp, dv)
		print 'MEAN = ', m
		lMeans.append(m)

		xLabels = ["Exp1 abs", "Exp1 corr", "Exp 2"]
		xTicks = range(0,3)
		plt.plot(lMeans, color = colList.pop(), linewidth = 2, marker = 'o')
		plt.ylim(-.2, .2)
		plt.xticks(xTicks, xLabels, rotation = .5)
		plt.xlim(min(xTicks)-spacing, max(xTicks)+spacing)
		   
	plt.legend(["initial saccade", "first refixation", "second refixation"])
	plt.axhline(0, linestyle = '--', linewidth = 2, color = "#555753")
	
	plt.savefig("all_saccades.png")
	plt.savefig("all_saccades.svg")

	
def binAllSaccs(direction = "ToHandle", figTitle = False, trim = True, cousineau = True, nBin = 15, usePm = True, err = 'se',\
		onlySacc1 = False, onlyExp2 = False):
	
	"""
	Throw all saccades latencies (since stim onset) in for bin analysis, irrespective of saccade count
	
	Arguments:
	dm
	direction --- {"ToHandle", "ToContrast"}, variable on the y axis
	
	Keyword arguments:
	onlyFirstSacc	--- True means only bin the FIRST sacc lateny
	
	Returns fig list
	
	
	"""
	lLabels = ["Exp1 absolute", "Exp1 corrected", "Exp2"]
			
	colList = [["#f57900"], ["#73d216"], ["#3465a4"]]
	fig = plt.figure(figsize = (3,7))
	title = "Landing %s as a function of ALL binned sacc lats cousineau = %s trim = %s usePm = %s onlyExp2 = %s onlySacc1 = %s" \
		% (direction, cousineau, trim, usePm, onlyExp2, onlySacc1)
	
	if figTitle:
		plt.title(title)
		
	
	for exp in ["004A", "004B"]:
		
		dm = getDM.getDM(exp = exp, driftCorr = True)
	
		if direction == "ToHandle":
			dm = dm.select("contrast_side == 'control'", verbose = False)
		if direction == "ToContrast":
			dm = dm.select("contrast_side != 'control'", verbose = False)
			
		lDm = []
		
		if exp == "004A":
			if onlyExp2:
				continue
			# Max sacc count = 4
			lSacc = range(1,5)
			
		if exp == "004B":
			# Max sacc count = 3
			lSacc = range(1,4)
			
		for saccCount in lSacc:
			
			if onlySacc1:
				if saccCount != 1:
					continue
			
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
		
		if exp == "004A":	
			corrList = ["uncorrected", "corrected"]
			continue
		if exp == "004B":
			corrList = ["uncorrected"]
		
		for corr in corrList:
		
			if corr == "uncorrected":
				dv = "abs%s" % direction
			elif corr == "corrected":
				dv = "absCorr%s" % direction
				
			print "\tDV = %s\n" % dv
			
			# There should be no ''s in the dm anymore, but off-object saccades are still
			# possible, so this filtering remains necessary:
			dv_dm = timecourse.onObject(merged_dm,dv, verbose = False)
				
			saccLat = "absSaccLat"

			# Trim the data matrix such that the most extreme latencies are excluded:
			print "\n\ttrim = %s\n" % trim
			if trim:
				trimmed_dm = dv_dm.selectByStdDev(keys = ["file"], dv = saccLat, verbose = False)
			else:
				trimmed_dm = dv_dm
			
			# Withinize sacc latencies, if wanted:
			print "\n\tcousineau = %s\n" % cousineau
			if cousineau:
				
				_dm = trimmed_dm.addField("cousineau_%s"%saccLat, dtype = None)
				_dm = _dm.withinize(saccLat, "cousineau_%s"%saccLat, "file", verbose = False, whiten=False)
				saccLat = "cousineau_%s"%saccLat
			else:
				_dm = dv_dm
					
			# Make bins, only for the first dv (for the second dv, the binned variable is the same and
			# therefore already exists:
			varToBin = saccLat
			binnedVar = "binnend%s" % varToBin
			binned_dm = _dm.addField(binnedVar)
			binned_dm = binned_dm.calcPerc(varToBin, binnedVar ,keys = ["file"], nBin = nBin)
			
			col = colList.pop()
			print
			print "EXP = ", exp
			print "DV = ", dv
			print
			if not usePm:
				
				lX = []
				lY = []
				binCount = 0
				for _bin in binned_dm.unique(binnedVar):  
				
				# Filter out all but one bin
					dm_one_bin = binned_dm.select('%s == %f' % (binnedVar, _bin))
			
					# Get the mean sacc lat and the mean landing position (for x and y axis, respectively):
					# NOTE: withinising doesn't make any real difference for the overall pattern. 
			
					yMean = dm_one_bin[dv].mean()
					xMean = dm_one_bin[varToBin].mean()
					binCount +=1 
					print binCount,xMean
					
					lX.append(xMean)
					lY.append(yMean)
				
				i = 0
				for x in lX:
					i +=1
					print "Bin %s: " % i, x
					
				plt.plot(lX, lY, color = col[0], marker = 'o')
			
			if usePm:
				
				pm = PivotMatrix(binned_dm, binnedVar, "file", dv, colsWithin = True, err = err)
				pm.plot(nLvl1=1, fig = fig, colors = col)
				
				#pm.barPlot(fig = fig, xLabel = "binned saccade latencies from stimulus onset", \
					#yLabel = "landing position (%s) %s" % (corr,direction))
	plt.xlabel("Binned stimulus-saccade interval")
	plt.ylabel("Landing positiontowards handle")
	plt.legend(lLabels)
	plt.ylim(-.2, .2)
	plt.axhline(0, color = "#555753", linestyle = "--", linewidth = 2)
	
	plt.savefig("%s.png"%title)
	plt.savefig("%s.svg"%title)
	
	return fig
	
def binPerSacc(direction = "ToHandle", cousineau = True,nBin = 8,trim = False, \
		figTitle = True, usePm = True, yLim = [-.25,.25], onlyExp2 = False):
	
	"""

	Argument:
	dm		--- data matrix
	
	Keyword argument:
	cousineau		--- withinize or not. Default = True.

	direction		--- {"toHandle", "toContrast"
	"""

	titleList = ["Exp1 absolute", "Exp1 corrected", "Exp2"]

	
	if not onlyExp2:
		fig = plt.figure(figsize = (9,7))
		title = "Landing %s as a function of bin PER SACC cousineau = %s trim = %s onlyExp2 = %s" % \
			(direction, cousineau,trim, onlyExp2)
		if figTitle:
			plt.title(title)
			
	nRows = 1
	nCols = 3
	plotNr = 0
	
	for exp in ["004A", "004B"]:
		
		if onlyExp2:
			if exp != "004B":
				continue
		
		start_dm = getDM.getDM(exp = exp, driftCorr = True)

		if direction == "ToHandle":
			start_dm = start_dm.select("contrast_side == 'control'", verbose = False)
		if direction == "ToContrast":
			start_dm = start_dm.select("contrast_side != 'control'", verbose = False)

		if exp == "004A":
			corrList = ["uncorrected", "corrected"]
			if onlyExp2:
				nCols = 1
				continue
		if exp == "004B":
			corrList = ["uncorrected"]
		
		for corr in corrList:
			subTitle = titleList[plotNr]
			
			plotNr +=1
			
			colList = [["#f57900"], ["#73d216"], ["#3465a4"]]
										 
			
			if onlyExp2:
				fig = plt.figure(figsize = (3,7))
				title = "Landing %s as a function of bin PER SACC ONLY EXP2 cousineau = %s trim = %s onlyExp2 = %s" % \
					(direction, cousineau,trim, onlyExp2)
				
			
			for saccCount in ["1", "2", "3"]:
				
				if saccCount == "1":
					nBin = 10
				if saccCount == "2":
					nBin = 10
				if saccCount == "3":
					nBin = 3
				
				print '\n\tsacc count = %s\n' % saccCount
				
				if corr == "uncorrected":
					dv = "endX%sNorm%s"%(saccCount, direction)
				elif corr == "corrected":
					dv = "endX%sCorrNorm%s"%(saccCount, direction)
					
				print "\tDV = %s\n" % dv

				dv_dm = timecourse.onObject(start_dm,dv, verbose = False)
				
				saccLat = "saccLat%s" % saccCount
				
				# Trim the data matrix such that the most extreme latencies are excluded:
				if trim:
					trimmed_dm = dv_dm.selectByStdDev(keys = ["file"], dv = saccLat, verbose = False)
				else:
					trimmed_dm = dv_dm
				
				# Withinize sacc latencies, if wanted:
				print "\n\tcousineau = %s\n" % cousineau
				if cousineau:
					
					_dm = trimmed_dm.addField("cousineau_%s"%saccLat, dtype = None)
					_dm = _dm.withinize(saccLat, "cousineau_%s"%saccLat, "file", verbose = False, whiten=False)
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
				
				# Determine x and y means per bin by hand:
				if not usePm:
					
					lX = []
					lY = []
					binCount = 0
					for _bin in binned_dm.unique(binnedVar):  
					
					# Filter out all but one bin
						dm_one_bin = binned_dm.select('%s == %f' % (binnedVar, _bin))
				
						# Get the mean sacc lat and the mean landing position (for x and y axis, respectively):
						# NOTE: withinising doesn't make any real difference for the overall pattern. 
				
						yMean = dm_one_bin[dv].mean()
						xMean = dm_one_bin[varToBin].mean()
						binCount +=1
						print binCount, xMean
						lX.append(xMean)
						lY.append(yMean)
					
					if exp == "004B":
						print 'XXXXXXXXX'
						print saccCount
						i = 0
						for x in lX:
							i +=1
							print "Bin %s: " % i, x
						print 
						print 'xxxxxxxxxxx'
					if not onlyExp2:
						plt.subplot(nRows,nCols,plotNr)
						plt.title(subTitle)
					plt.plot(lX, lY, color = col[0], marker = 'o')
					plt.xlabel("binned saccade latencies from stimulus onset")
					plt.ylabel("landing position (%s) %s" % (corr,direction))
					
				# Disadvantages of pm: 
					# - There SHOULD be enough observations per participant to be able to plot
					# - bin number (instead of bin mean) on x axis
				if usePm:
					if not onlyExp2:
						plt.subplot(nRows,nCols,plotNr)
						plt.title(subTitle)
					
					pm = PivotMatrix(binned_dm, binnedVar, "file", dv, colsWithin = True, err = 'se')
					pm.plot(nLvl1=1, fig = fig, colors = col)
			
			if plotNr != "1":
				plt.yticks([])
			plt.xticks([])
			plt.ylim(yLim)
			plt.legend(["initial saccade", "refixation 1", "refixation 2"])
			plt.axhline(0, color = "#555753", linestyle = "--", linewidth = 2)
	plt.savefig(os.path.join('%s.png' % title))
	plt.savefig(os.path.join('%s.svg' % title))
	
if __name__ == "__main__":
	
	def start():
		
		pass
	
	# Split by heavy side to show that towards handle is NOT plausible.
	#binPerSacc(usePm = False)
	#sys.exit()
	#binAllSaccs(usePm = False)
	#sys.exit()
	#landWithoutContrast()
	#sys.exit()
	for excl in [True, False]:
		landWithoutContrast(exclY = excl)
	sys.exit()
	
	# All possible plots for bin analyses:
	direction = "ToContrast"
	binAllSaccs(onlyExp2 = True, direction = direction)
	binAllSaccs(onlyExp2 = True, onlySacc1 = True, nBin = 10, direction = direction)
	binAllSaccs(direction = direction)
	binAllSaccs(onlySacc1 = True, nBin = 10, direction = direction)
	binPerSacc(direction = direction)
	binPerSacc(onlyExp2 = True, direction = direction)
	sys.exit()
	
	plt.show()
	binAllSaccs(onlyFirstSacc = True, nBin = 10)
	
	#binAllSaccs(usePm = False)
	sys.exit()
	
	# Plot for slide about landing positions of refixations:
	landAllSaccs()
	
	dm = getDM.getDM(exp = "004A", driftCorr = True)
	
	
	sys.exit()
	for saccNr in ("1"):#, "2", "3", "4"):
		
		#if saccNr != "3":
		#	continue
		
		yLim = [-.3, .3]
		
		#landWithoutContrast(factor = ["heavySide"], saccNr = saccNr, yLim = yLim)
		
		fig = landWithoutContrast(factor = ["handle_side"], saccNr = saccNr, yLim = yLim, sepPlots = False)
		plt.show()
		
		#plt.show()
	#landHeavySide(dm)
	sys.exit()
	
	
	colsWithin = True
	for exp in ["004A", "004B"]:
		
		# Get dm:
		dm = getDM.getDM(exp = exp, driftCorr = True)

		# Only use handled objects:
		dm = dm.select("symm == 'asymm'")

		landHandle(dm, dvLand = 'endX2Norm', colsWithin = colsWithin)
		landHandle(dm, dvLand = 'endX1Norm', colsWithin = colsWithin)
		if exp == "004A":
			landHandle(dm, dvLand = 'endX1CorrNorm', colsWithin = colsWithin)
			landHandle(dm, dvLand = 'endX2CorrNorm',colsWithin = colsWithin)
			
	
		#landHandle(dm, dvLand = 'endX3Norm')
		#landHandle(dm, dvLand = 'endX3CorrNorm')
	

		#sys.exit()
	
	
	