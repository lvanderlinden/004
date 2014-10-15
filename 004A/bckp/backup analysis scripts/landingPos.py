#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: landingPos.py

"""
TODO:
- Average per stimulus?
- All EM per stimulus? -> both x and y normalised, stimulus on background
- Have a closed look at y coordinates -> overshoot instead of undershoot 
	is weird....
- Plot normalised CoG -> 
- Check yCOG
- Over VF, indicate mask condition with different colors!
- Adapt y coordinates according to laucnh site (upper or lower, to
	make undershoot effect less visible)

CHANGELOG:
02-07-2013:
	Normalised saccade landing positions per stimulus (i.e., objects
	with a given orientation and mask), per visual field.
	
	landPosPerStim():
		The best function to use is , which plots all
		stimuli, and indicates visual field by different colors.
	landPosPerStimPerVF(): 
		Separate subplots for UVF and LVF. As a consequence,
		mask condition (left, right, control) couldn't be
		included IN the plots, therefore saved in separate
		plots (name indicates mask condition).
		
	landPosAcrossVF():
		Separate subplots for orientation. Different mask 
		conditions are indicated by color.
		Not split by visual field.
		TODO: correct for launch site (see P&N?)

22-07-2013:
	
	xCoG normalised is obtained by dividing xCoG by the 
	width of the ORIGINAL bitmap, not of the chopped bitmap!!
"""

# Import Python modules:
import numpy as np
import os
import sys
from matplotlib import pyplot as plt
from matplotlib import image as mpimg
from matplotlib.backends.backend_pdf import PdfPages

# Import own modules:
import getDM
from exparser.DataMatrix import DataMatrix
import studies._004.constants

plt.rc("font", family="ubuntu")
plt.rc("font", size=11)
		

# Folder containing chopped bitmaps (used for drawing the imaginary box around the
# objects:
src = "/home/lotje/Documents/PhD Marseille/Studies/004 - One-object experiment - Orienation effect/Analysis/plots/chopped bitmaps"


def distPerObject(dm, dv, nBin = 20, handlesOnly = True, inPDF = True, \
		dst = "./plots/landing positions/binned", onlyControl = True, \
			cousineau = True, trim = True, verbose = True):

	"""
	Plots distribution of normalised landing positions under stimulus.
	
	NOTE the problem with this funciton: The CoG as calculated for the 
	unchopped bitmaps (as used for the data analysis and input for 
	Exp2) does not correspond (exactly) to the CoG as plotted on the
	chopped bitmaps here...
	
	NOTE also that this is no problem for normalising the raw landing
	positions. It probably has something to do with the fact that
	(1) the object was not perfectly centered in the original bitmap,
	or (2) that the chopping is not caried out perfectly.
	
	Arguments:
	dm		--- data matrix
	dv		--- dependent variable (e.g. 'endX1Norm')
	
	Keyword arguments:
	nBin	--- number of bins (default = 20)
	handlesOnly		--- Inlcude only handled objects, not the filler objects 
						(e.g. carrot). Default = True.
	inPDF
	onlyControl		---Include only trials where no mask was applied. 
						Default = True.
	"""
	
	# Walk through all possible picture by handle side combinations:
	
	if "Corr" in dv:
		corr = True
	else:
		corr = False
	
	# Exclude non-handled objects:
	if handlesOnly:
		dm = dm.select("symm == 'asymm'")
	
	# Exclude empty cells:
	dm = dm.select("%s != ''" % dv)
	
	exp = dm["exp"][0]
	
	if inPDF:
		pp = PdfPages('%s: Binned landing positions %s.pdf' % (exp, dv))
		
	
	expFolder = os.path.join(dst, exp)
	
	if not os.path.exists(expFolder):
		os.makedirs(expFolder)
	
	varFolder = os.path.join(expFolder, dv)
	
	if not os.path.exists(varFolder):
		os.makedirs(varFolder)
	
	# Exclude initial eye-movements that were outside the object:
	# Note that this means subsequent OFF object eye movements are still
	# included.
	dm = dm.select('endX1Norm < .5', verbose = False)
	dm = dm.select('endX1Norm > -.5', verbose = False)
	
	
	if onlyControl:
		dm = dm.select("mask_side == 'control'", verbose = False)
	
	if trim:
		trimmed_dm = dm.selectByStdDev(keys = ["handle_side", "file"], dv = dv)
	else:
		trimmed_dm = dm
		
	if cousineau:
		
		new_dv = "cousineau_%s" % dv
		
		ws_dm = trimmed_dm.addField(new_dv, dtype = None)
		ws_dm = ws_dm.withinize(dv, new_dv, "file", verbose = True, whiten=False)
	else:
		ws_dm = trimmed_dm
		new_dv = dv

	
	for pict in np.unique(ws_dm["picture_name"]):
		pict_dm = ws_dm.select("picture_name == '%s'"%pict, verbose = True)
		
		
		fig = plt.figure()
		figName = "%s: binned %s on %s nBin = %s trim = %s cousineau = %s" % (exp, dv, str(pict), nBin, trim, cousineau)
		plt.suptitle(figName)

		nCols = 2
		nRows = 2
		nPlots = 0

		for handle_side in ["left", "right"]:

			handle_dm = pict_dm.select("handle_side == '%s'"%handle_side, verbose = True)
			
			print 'CHECK CHECK'
			print dm.unique('contrast_side')
			print
			
			
			data = handle_dm[dv]

			
			nPlots += 1
			plt.subplot(nRows,nCols,nPlots)
			plt.title("nr of trials = %s handle = %s"% (len(data),handle_side))
			plt.hist(data, bins = nBin, color = "#729fcf", alpha = .5)
			if exp == "004A":
				plt.xlim(-.5, .5)
			else:
				plt.xlim(-.8, .8)
			line1 = plt.axvline(0, color = "#fce94f", linewidth = 2)
			
			w = studies._004.constants.wBitmap
			xCoG = handle_dm['xCoG'][0]/w
			
			if exp != "004B":
				line2 = plt.axvline(xCoG, linestyle = "--", color = "#f57900", linewidth = 2)
			plt.subplots_adjust(hspace = 0)
			if corr == True:
				if handle_side == "right":
					plt.legend([line1, line2],["center", "CoG"], loc = 'best')
			
			nPlots += 2
			plt.subplot(nRows, nCols, nPlots)
			fName = "handle_%s_%s.jpg" % (handle_side, pict)
			fSrc = os.path.join(src, fName)
			img=mpimg.imread(fSrc)
			plt.xticks([])
			plt.yticks([])
			
			nPlots -= 2
			
			plt.imshow(img, aspect = None)#, anchor = (0,0))
		pp.savefig(fig)
		plt.savefig(os.path.join(varFolder, "%s.png"%figName))
		plt.savefig(os.path.join(varFolder, "%s.svg"%figName))
		#plt.show()
	pp.close()
	
def landPosPerStimPerVF(exp, saccNr = "1", corrCoG = False):
	"""
	Plots all normalised sacc coordinates per stimulus.
	
	Keyword arguments:
	corrCoG		--- False = raw coordinates, True = coordinates
						minues CoG
	"""
	
	# Get the dm:
	dm = getDM.getDM(exp, driftCorr = True)
	

	# Only objects without mask:
	
	## Only select ON OJBECT eye movements:
	dm = dm.select("endX1Norm > -.5")
	dm = dm.select("endX1Norm < .5")
	dm = dm.select("endY1Norm < 5")
	dm = dm.select("endY1Norm > -5")
	
	# One such a selection should be sufficient:
	dm = dm.select("endX%sNorm != ''" % saccNr)
	
	for mask_side in ["control", "left", "right"]:
	
		mask_dm = dm.select("mask_side == '%s'" % mask_side)
				
		
		for pict in np.unique(dm["object"]):
			
			pict_dm = mask_dm.select("object == '%s'"% pict)
			
			
			w = studies._004.constants.wBitmap
			h = studies._004.constants.hBitmap

			ratio = dm['boxWidth'][0]/dm['boxHeight'][0]
			
			
			figH = 10
			figW = figH/ratio
		
			figName = "%s: all eye movements (counter = %s) per VF on %s mask = %s N = %s corr = %s" % (exp, saccNr, pict, mask_side, len(pict_dm), corrCoG)
			#fig = plt.figure(figsize = (figH, figW))
			fig = plt.figure()
			plt.suptitle(figName)
			
			nRows = 2
			nCols = 2
			nPlots = 0

			for vf in ["upper", "lower"]:
				vf_dm = pict_dm.select("visual_field == '%s'" % vf)
					
				for handle in ["left", "right"]:	
					
					handle_dm = vf_dm.select("handle_side == '%s'" % handle)
					
					xCoG = handle_dm['xCoG'][0]/w
					yCoG = handle_dm['yCoGZero'][0]/h
					
					if not corrCoG:
						y = handle_dm['endY%sNorm' % saccNr]
						x = handle_dm['endX%sNorm'% saccNr]
					else:
						y = handle_dm['endY%sCorrNorm'% saccNr]
						x = handle_dm['endX%sCorrNorm'% saccNr]
							
					
					nPlots += 1
					plt.subplot(nRows, nCols, nPlots)
					plt.title('handle = %s VF = %s n = %s' % \
						(handle, vf, len(handle_dm)))
					plt.xlim(-.5, .5)
					plt.axhline(0, color = 'gray', linewidth = 2)
					plt.axvline(0, color = 'gray', linewidth = 2)
					if exp == "004A":
						plt.axvline(xCoG, linestyle = '--', color = 'orange', linewidth = 2)
						plt.axhline(yCoG, linestyle = '--', color = 'orange', linewidth = 2)
					plt.axhspan(-.5, .5, color = 'lightblue', alpha = .5)
					
					plt.scatter(x,y)
					#print handle_dm['xCoG']
					#print handle_dm['yCoGZero']
					plt.gca().invert_yaxis()
					
					#plt.show()
			
			#plt.show()
			plt.savefig("%s.png" % figName)

def landPosPerStim(exp, saccNr = "1", corrCoG = False, handlesOnly = True, inPDF = True):
	"""
	Plots all normalised sacc coordinates per stimulus.
	
	Keyword arguments:
	corrCoG		--- False = raw coordinates, True = coordinates
						minues CoG
	handlesOnly --- Default = True
	"""
	
	w = studies._004.constants.wBitmap
	h = studies._004.constants.hBitmap
	
	
	# Get the dm:
	dm = getDM.getDM(exp, driftCorr = True)
	
	# Exclude non-handled objects:
	if handlesOnly:
		dm = dm.select("symm == 'asymm'")
		
	
	# Only objects without mask:
	
	## Only select ON OJBECT eye movements:
	dm = dm.select("endX1Norm > -.5")
	dm = dm.select("endX1Norm < .5")
	dm = dm.select("endY1Norm < 5")
	dm = dm.select("endY1Norm > -5")
	
	# One such a selection should be sufficient:
	dm = dm.select("endX%sNorm != ''" % saccNr)
	
	if inPDF:
		pp = PdfPages('%s: Raw landing positions - sacc count = %s.pdf' % (exp, saccNr))
					
	
	for pict in np.unique(dm["object"]):
		
		pict_dm = dm.select("object == '%s'"% pict)
		
		
		figName = "%s: all eye movements (sacc count = %s) on %s N = %s corr = %s" % \
			(exp, saccNr, pict, len(pict_dm), corrCoG)
		fig = plt.figure(figsize = (8,10))
		plt.suptitle(figName)
		plt.subplots_adjust(hspace = .4)
		
		nRows = 3
		nCols = 2
		nPlots = 0

		for contrast_side in ["_left", "control", "right"]:
			
			mask_dm = pict_dm.select("contrast_side == '%s'" % contrast_side)
					
			for handle in ["left", "right"]:	
			
				handle_dm = mask_dm.select("handle_side == '%s'" % handle)
			
				xCoG = handle_dm['xCoG'][0]/w
				yCoG = handle_dm['yCoGZero'][0]/h

				vf_upper = handle_dm.select("visual_field == 'upper'")
				vf_lower = handle_dm.select("visual_field == 'lower'")
					
				
				if not corrCoG:
					yUp = vf_upper['endY%sNorm' % saccNr]
					xUp = vf_upper['endX%sNorm'% saccNr]
					yLow = vf_lower['endY%sNorm'% saccNr]
					xLow = vf_lower['endX%sNorm'% saccNr]

				else:
					yUp = vf_upper['endY%sCorrNorm'% saccNr]
					xUp = vf_upper['endX%sCorrNorm'% saccNr]
					yLow = vf_lower['endY%sCorrNorm'% saccNr]
					xLow = vf_lower['endX%sCorrNorm'% saccNr]
				
				if contrast_side == 'control':
					titleCol = "#73d216"
				else:
					titleCol = "#2e3436"
					
				
				nPlots += 1
				plt.subplot(nRows, nCols, nPlots)
				plt.title('handle = %s most contrast = %s \nn = %s' % \
					(handle, contrast_side, len(handle_dm)), color = titleCol)
				if exp == "004A":
					plt.xlim(-.5, .5)
				else:
					plt.xlim(-.8, .8)
				
				plt.axhline(0, color = '#888a85', linewidth = 2)
				plt.axvline(0, color = '#888a85', linewidth = 2)
				if exp == "004A":
					plt.axvline(xCoG,linestyle = '--', color = '#ef2929', linewidth = 2)
					plt.axhline(yCoG, linestyle = '--', color = '#ef2929', linewidth = 2)
				plt.axhspan(-.5, .5, color = '#fce94f', alpha = .3)
				
				# Upper VF = orange, lower VF  = blue!!
				l1 = plt.scatter(xUp,yUp, color = "#f57900")
				l2 = plt.scatter(xLow, yLow, color = "#3465a4")
				
				#if nPlots == nRows * nCols:
				#	plt.legend((l1,l2),["upper VF", "lower VF"], loc = 'best')
				plt.gca().invert_yaxis()
				
		plt.savefig("%s.png" % figName)
		pp.savefig(fig)
	pp.close()
def landPosAcrossVF(exp, saccNr = "1", corrCoG = False):
	
	"""
	Plots all normalised sacc coordinates per stimulus.
	
	Keyword arguments:
	corrCoG		--- False = raw coordinates, True = coordinates
						minues CoG
	"""
	
	# Get the dm:
	dm = getDM.getDM(exp, driftCorr = True)
	
	# Only objects without mask:
	
	## Only select ON OJBECT eye movements:
	dm = dm.select("endX1Norm > -.5")
	dm = dm.select("endX1Norm < .5")
	dm = dm.select("endY1Norm < 5")
	dm = dm.select("endY1Norm > -5")
	
	# One such a selection should be sufficient:
	dm = dm.select("endX%sNorm != ''" % saccNr)
	
	for pict in np.unique(dm["object"]):
		
		pict_dm = dm.select("object == '%s'"% pict)
		
		w = studies._004.constants.wBitmap
		h = studies._004.constants.hBitmap
		
		
		figName = "%s: all eye movements (counter = %s) across VF on %s N = %s corr = %s" % \
			(exp, saccNr, pict, len(pict_dm), corrCoG)
		#fig = plt.figure(figsize = (8,10))
		fig = plt.figure()
		plt.suptitle(figName)
		plt.subplots_adjust(hspace = .4)
		
		nRows = 1
		nCols = 2
		nPlots = 0

				
		for handle in ["left", "right"]:	
		
			handle_dm = pict_dm.select("handle_side == '%s'" % handle)
		
			xCoG = handle_dm['xCoG'][0]/w
			yCoG = handle_dm['yCoGZero'][0]/h

			mask_control = handle_dm.select("mask_side == 'control'")
			mask_left = handle_dm.select("mask_side == 'left'")
			mask_right = handle_dm.select("mask_side == 'right'")
				

			if not corrCoG:
				yControl = mask_control['endY%sNorm' % saccNr]
				xControl = mask_control['endX%sNorm'% saccNr]
				yL = mask_left['endY%sNorm'% saccNr]
				xL = mask_left['endX%sNorm'% saccNr]
				yR = mask_right['endY%sNorm'% saccNr]
				xR = mask_right['endX%sNorm'% saccNr]
				
			else:
				yControl = mask_control['end%sCorrNorm'% saccNr]
				xControl = mask_control['endY%sCorrNorm'% saccNr]
				yL = mask_left['endY%sCorrNorm'% saccNr]
				xL = mask_left['endY%sCorrNorm'% saccNr]
				yR = mask_right['endY%sCorrNorm'% saccNr]
				xR = mask_right['endY%sCorrNorm'% saccNr]
				
			nPlots += 1
			plt.subplot(nRows, nCols, nPlots)
			plt.title('handle = %s n = %s' % \
				(handle, len(handle_dm)))
			plt.xlim(-.5, .5)
			plt.axhline(0, color = '#888a85', linewidth = 2)
			plt.axvline(0, color = '#888a85', linewidth = 2)
			if exp == "004A":
				plt.axvline(xCoG, linestyle = '--', color = '#ef2929', linewidth = 2)
				plt.axhline(yCoG, linestyle = '--', color = '#ef2929', linewidth = 2)
			plt.axhspan(-.5, .5, color = '#fce94f', alpha = .3)
			
			# Upper VF = orange, lower VF  = blue!!
			l1 = plt.scatter(xControl,yControl, color = "#73d216")
			l2 = plt.scatter(xL, yL, color = "#3465a4")
			l3 = plt.scatter(xR, yR, color = "#f57900")
			
			if nPlots == nRows * nCols:
				plt.legend((l1,l2, l3),["control", "mask left", "mask right"], loc = 'best')
			plt.gca().invert_yaxis()
			
		plt.savefig("%s.png" % figName)


if __name__ == "__main__":
	
	def dummy():
		
		pass
	
	for saccNr in ["1", "2", "3"]:
		if saccNr != "1":
			continue
		for exp in ["004A", "004B"]:
			
			dm = getDM.getDM(exp, driftCorr = True)
			distPerObject(dm, "endX%sNorm" % saccNr)
			if exp == "004A":
				distPerObject(dm, "endX%sCorrNorm" % saccNr)
			#landPosAcrossVF(exp, corrCoG = corr)
	#		landPosPerStim(exp, corrCoG = corr,saccNr = saccNr)
			#landPosPerStimPerVF(exp, corrCoG = corr)
		
		
		
