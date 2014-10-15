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
"""

# Import Python modules:
import numpy as np
import os
import sys
from matplotlib import pyplot as plt
from matplotlib import image as mpimg

# Import own modules:
import getDM
from exparser.DataMatrix import DataMatrix
import studies._004.constants

plt.rc("font", family="ubuntu")
plt.rc("font", size=11)
		

# Folder containing chopped bitmaps (used for drawing the imaginary box around the
# objects:
src = "/home/lotje/Documents/PhD Marseille/Studies/004 - One-object experiment - Orienation effect/Analysis/plots/chopped bitmaps"


def distPerObject(dm, dv, nBin = 20):

	"""
	Plots distribution of normalised landing positions under stimulus.
	
	Arguments:
	dm		--- data matrix
	dv		--- dependent variable (e.g. 'endX1Norm')
	
	Keyword arguments:
	nBin	--- number of bins (default = 20)
	"""
	
	# Walk through all possible picture by handle side combinations:
	
	# Exclude empty cells:
	dm = dm.select("%s != ''" % dv)
	
	exp = dm["exp"][0]
	
	# Exclude eye-movements that were outside the object:
	
	if "Norm" in dv:
		dm = dm.select('%s < .5'%dv)
		dm = dm.select('%s > -.5'%dv)
	
	for pict in np.unique(dm["picture_name"]):
		
		
		fig = plt.figure()
		figName = "%s: binned %s on %s nBin = %s" % (exp, dv, str(pict), nBin)
		plt.suptitle(figName)
		plt.subplots_adjust(hspace = 0)
		nCols = 2
		nRows = 2
		nPlots = 0

		for handle_side in ["left", "right"]:

			_dm = dm.select("picture_name == '%s'"%pict)
			_dm = _dm.select("handle_side == '%s'"%handle_side)
			
			data = _dm[dv]

			plt.subplots_adjust(hspace = 0, wspace = 0)
			
			nPlots += 1
			plt.subplot(nRows,nCols,nPlots)
			plt.title("nr of trials = %s"% len(data))
			plt.hist(data, bins = nBin, color = "#f57900", alpha = .5)
			plt.xlim(-.5, .5)
			plt.axvline(0)
			plt.subplots_adjust(hspace = 0)
			#plt.xlabel(dv)
			plt.xticks([])
			plt.yticks([])
			
			nPlots += 2
			plt.subplot(nRows, nCols, nPlots)
			fName = "handle_%s_%s.jpg" % (handle_side, pict)
			fSrc = os.path.join(src, fName)
			img=mpimg.imread(fSrc)
			plt.xticks([])
			plt.yticks([])
			
			nPlots -= 2
			
			plt.imshow(img, aspect = None)#, anchor = (0,0))
			
		plt.savefig("%s.png"%figName)
		#plt.show()

	
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
			
			print len(dm)
			
		
			w = dm['boxWidth'][0]
			h = dm['boxHeight'][0]
			
			ratio = w/h
			
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

def landPosPerStim(exp, saccNr = "1", corrCoG = False):
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
		
		w = dm['boxWidth'][0]
		h = dm['boxHeight'][0]
		
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
				plt.xlim(-.5, .5)
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
		
		w = dm['boxWidth'][0]
		h = dm['boxHeight'][0]
		
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
	
	
	for saccNr in ["1", "2", "3"]:
		for exp in ["004A", "004B"]:
	
			dm = getDM.getDM(exp, driftCorr = True)
		
			#distPerObject(dm, "endX%sNorm" % saccNr)
			
			corr = False
		
			#landPosAcrossVF(exp, corrCoG = corr)
			landPosPerStim(exp, corrCoG = corr,saccNr = saccNr)
			#landPosPerStimPerVF(exp, corrCoG = corr)
		
		
		