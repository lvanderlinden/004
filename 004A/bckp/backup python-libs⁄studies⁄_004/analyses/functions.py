def contrastBinAn(dm, nBin = 10, showFig = False, saveFig = True):
	
	"""
	Landing positions as a function of binned latency and contrast.
	
	TODO: Binned only on the basis of pp, not on contrast...
	TODO: How to test significantly?
	
	Arguments:
	dm		--- Data matrix.
	
	Keyword arguments:
	nBin 	--- Number of bins. Default = 10.
	show	Fig	--- Boolean indicating whether or not to show the plots. Default 
				= False.
	saveFig 	--- Boolean indicating whehter or not to save the plot. Default = 
				True.
	"""
	
	dm = latBins(dm, nBin = nBin)
	
	pm = PivotMatrix(dm, ['mask_side', 'saccLatBin'], ['file'], \
		dv='endX', colsWithin=True)
	pm._print()
	
	fig = plt.figure()
	name = "Landing pos as a function of binned Latency and Contrast nBin = %s"%nBin

	plt.suptitle(name)
	xLabels = range(1,nBin+1)
	xLabel = "binned latencies"
	lLabel = "contrast manipulation"
	lLabels = ["control", "more contrast right", "more contrast left"]
	#lLabels = None
	yLabel = "landing position \n negative = left, positive = right"
	pm.linePlot(xLabels = xLabels, xLabel = xLabel, yLabel = yLabel, \
		legendTitle = lLabel, lLabels = lLabels)
	plt.axhline(0, color = "grey", linestyle = "--")
	
	if showFig:
		plt.show()
		savFig = False
	if saveFig:
		plt.savefig(os.path.join(outputFolder,\
			"%s.jpg"%name))


	
def landOnHandlePerContrast(dm,dv, saveFig = True, showFig = False, \
		printStats = True,onlyControl = True, exSymm = True):
	
	"""
	Plots a given dv as a function of handle side, and contrast.
	
	Arguments:
	dm		--- Data matrix.\
	dv		--- {'endX', 'endXCorr'}, depedent value.
	
	Keyword arguments:
	show	Fig	--- Boolean indicating whether or not to show the plots. Default 
				= False.
	saveFig 	--- Boolean indicating whehter or not to save the plot. Default = 
				True.
	printStats	--- Boolean indicating whether or not to print stats.
	exSymm		--- Boolean indicating whether or not to exclude symmetrical 
					(filler) objects. Default = True.
	onlyControl	--- Boolean indicating whether or not to only include trials on which
					contrast was manipulated. Default = True.
	trim
	"""
	
	# Only include asymmetrical objects:
	if exSymm:
		dm = dm.select('symm == "asymm"')
		
	if onlyControl:
		dm = dm.select("mask_side != 'control'")
	

	# Get pivot table:
	pm = PivotMatrix(dm, ['handle_side', 'mask_side'], ['file'], \
		dv=dv, colsWithin=True)
	pm._print()

	am = AnovaMatrix(dm, factors = ["mask_side", "handle_side"], dv = dv, \
		subject = "file")._print(maxLen=10,ret=True)

	fig = plt.figure()
	name = "%s as a function of Contrast and Handle exSymm = %s"\
		%(dv,exSymm)
		
	plt.suptitle(name)
	plt.subplot(121)
	
	legendTitle = "contrast"
	
	if onlyControl:
		xLabels =["more contrast right", "more contrast left"] 
	else:
		xLabels = ["control", "more contrast right", "more contrast left"]
	yLabel = "Landing position: \n negative = left, positive = right"

	legendTitle = "handle side"
	lLabels = ["handle left", "handle right"]
	lLabels = None
	pm.linePlot(fig = fig, xLabels = xLabels, lLabels = lLabels, yLabel = yLabel)
	plt.axhline(0, linestyle = "--", color = "grey")

	# Print the stats:
	statSubplot(am)
	
	if showFig:
		plt.show()
		saveFig = False
	
	if saveFig:
		plt.savefig(os.path.join(outputFolder,"%s.jpg"%name))

def landOnHandlePerContrastSplitBy(dm,dv, factor,saveFig = True, showFig = False, \
		printStats = True,onlyControl = True, exclCorrTooLarge = False):
			

	"""
	Plots a given dv as a function of handle side, and contrast.
	
	Arguments:
	dm		--- Data matrix.
	dv		--- {'endX', 'endXCorr'}, depedent value.
	factor	--- {'symm', 'corrDirection'}, factor to split handle-contrast
				analysis by.
	
	Keyword arguments:
	show	Fig	--- Boolean indicating whether or not to show the plots. Default 
				= False.
	saveFig 	--- Boolean indicating whehter or not to save the plot. Default = 
				True.
	printStats	--- TODO Boolean indicating whether or not to print stats.
	onlyControl	--- Boolean indicating whether or not to only include trials on which
					contrast was manipulated. Default = True.
	exclCorrTooLarge	---- Boolean indicating whether or not to exclude objects
						for which the CoG correction was too large.
	"""

	# Apply some selection criteria if desired:
	if onlyControl:
		dm = dm.select("mask_side != 'control'")
	if exclCorrTooLarge:
		
		if factor == "corrDirection":
			msg.userMsg.userMsg(\
				"Splitting by AND selecting only one level of %s makes no sense."%factor,\
				__file__)
			return
		dm = dm.select("corrDirection == 'correction smaller than %s'"% \
			constants.CoGCorrTooLarge)
		
	
	# Create the figure:
	fig = plt.figure(figsize = (20,10))
	name = "%s as a function of Contrast, Handle and %s - exclCorrTooLarge = %s"\
		%(dv,factor, exclCorrTooLarge)
	plt.suptitle(name)

	if factor == "corrDirection":
		nrCols = 2
		nrRows = 3
	else:
		nrCols = nrRows = 2

	i = 1
	
	for lvl in np.unique(dm[factor]):
		
		lvl_dm = dm.select("%s == '%s'"%(factor,lvl))
		
		# Get pivot table:
		pm = PivotMatrix(lvl_dm, ['handle_side', 'mask_side'], ['file'], \
			dv=dv, colsWithin=True)
		pm._print()

		am = AnovaMatrix(lvl_dm, factors = ["mask_side", "handle_side"], dv = dv, \
			subject = "file")._print(maxLen=10,ret=True)

		plt.subplot(nrRows,nrCols,i)
		i +=1
		plt.title(lvl)
		legendTitle = "contrast"
	
		if onlyControl:
			xLabels =["more contrast right", "more contrast left"] 
		else:
			xLabels = ["control", "more contrast right", "more contrast left"]
		yLabel = "Landing position: \n negative = left, positive = right"

		legendTitle = "handle side"
		lLabels = ["handle left", "handle right"]
		lLabels = None
		pm.linePlot(fig = fig, xLabels = xLabels, lLabels = lLabels, yLabel = yLabel)
		plt.axhline(0, linestyle = "--", color = "grey")

		# Print the stats:
		statSubplot(am, nrRows,nrCols,i, flip=False)
		i +=1
		
	if showFig:
		plt.show()
		saveFig = False
	
	if saveFig:
		plt.savefig(os.path.join(outputFolder,"%s.jpg"%name))

	
	



	




