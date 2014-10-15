	#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: runAnalyses.py

"""
DESCRIPTION:
Create data matrix.
TODO: splits per correctie naar links of naar rechts
kijk op trial niveau
kijk naar symmetrische objecten
kijken hoeveel variantie gravity verklaard door binanalyses
apart te doen per luminantiemanipulatie

TODO: bin analyses hoeven geen aparte modules te zijn!


NOTE NOTE NOTE NOTE:
corrDirection is changed!
"""

# Import Python libraries:
import math
import numpy as np
import scipy
from matplotlib import cm
from matplotlib import pyplot as plt
import sys
import os

# Import own modules:
from exparser.EyelinkAscFolderReader import EyelinkAscFolderReader
from exparser.DataMatrix import DataMatrix
from exparser.PivotMatrix import PivotMatrix
import studies._004B.getDM
import studies._004B.analyses.distributions
import studies._004B.analyses.anovas
import studies._004B.analyses.binAnalyses
import studies._004B.analyses.regressionAnalyses

# Define constants:
dvList = ["rtFromStim", "saccLat", "endXCorr", "accuracy"]


if __name__ == "__main__":
	
	# Get the data matrix, WITH and WITHOUT drift correction:
	dmDriftCorr  = studies._004B.getDM.getDM(driftCorr = True)
	#dmRaw = studies._004B.getDM.getDM(driftCorr = False)

	dmCorrect = studies._004B.getDM.getDM(driftCorr = True, excludeErrors = True)
	dmCorrect = dmCorrect.select("file != '00416.asc'")

	# Look at the distribution of starting positions and landing positions before
	# drift correction is applied:
	#studies._004B.analyses.distributions.distHistTwoVars(dmRaw, \
		#['startXDegr', 'endXDegr'],showFig = False,\
		#zTransform = False, xLabel = "visual degrees", xLim = [-2,2], nBin = 100)
	
	#studies._004B.analyses.distributions.distHistTwoVars(dmDriftCorr, \
		#['startXDegr', 'endXDegr'],showFig = False,\
		#zTransform = False, xLabel = "visual degrees", xLim = [-2,2], nBin = 100)
	#sys.exit()

	# ANOVAs to show that landing positions are explained by CoG and a tendency
	# to land towards the middle of the object:
	
	# Landing as a function of handle side and contrast:
	
	# Before drift correction:
	#studies._004B.analyses.anovas.twoFactor(dmRaw, dv = "endXDegr", factors = ["mask_side", "handle_side"], exControlMask = False,
	#exFiller = True, showFig = False)
	
	#studies._004B.analyses.anovas.twoFactor(dmRaw, dv = "endXCorrDegr", factors = ["mask_side", "handle_side"], exControlMask = False,
	#exFiller = True, showFig = False)

	#studies._004B.analyses.anovas.twoFactor(dmRaw, dv = "endXCorrMaskDegr", factors = ["mask_side", "handle_side"], exControlMask = False,
	#exFiller = True, showFig = False)

	# After drift correction:
	figName = "Graphe 2"
	legendTitle = "contraste"
	lLabels = ["controle", "contraste a droite", "contraste a gauche"]
	xLabel = "orientation de la poignee"
	xLabels = ["gauche", "droite"]
	yLabel = "position d'atterrissage de l'oeil"

	studies._004B.analyses.anovas.twoFactor(dmDriftCorr, dv = "endXDegr", \
		factors = ["mask_side", "handle_side"], exControlMask = False,
		exFiller = True, showFig = False, yLim = [-0.6, 0.6], figName = figName,\
			legendTitle = legendTitle, lLabels = lLabels, xLabel = xLabel,\
				xLabels = xLabels, yLabel = yLabel, saveExt = '.svg')
	

	studies._004B.analyses.anovas.twoFactor(dmDriftCorr, dv = "endXDegr", \
		factors = ["mask_side", "handle_side"], exControlMask = False,
		exFiller = True, showFig = True, yLim = [-0.6, 0.6])
	
	
	## Split per 'heavy side':
	#studies._004B.analyses.anovas.threeFactor(dmDriftCorr, dv = "endXDegr", \
		#factors = ["heavy_side", "mask_side", "handle_side"], \
		#exControlMask = False, exFiller = True, showFig = False, \
			#yLim = [-0.6, 0.6])


	#studies._004B.analyses.anovas.twoFactor(dmDriftCorr, dv = "endXCorrDegr", factors = ["mask_side", "handle_side"], exControlMask = False,
	#exFiller = True, showFig = False, yLim = [-0.6, 0.6])

	#studies._004B.analyses.anovas.twoFactor(dmDriftCorr, dv = "endXCorrMaskDegr", factors = ["mask_side", "handle_side"], exControlMask = False,
	#exFiller = True, showFig = False, yLim = [-0.6, 0.6])
	

	### Time course of affordance effect on endX:
	#studies._004B.analyses.binAnalyses.binAnalysesSepLines(dmDriftCorr, dv = "degrTowardsHandleCorr",\
	#	varToBin = "saccLat", factor = "corrDirection", showFig = False, nBin = 15)
	#studies._004B.analyses.binAnalyses.binAnalysesSepLines(dmDriftCorr, dv = "degrTowardsHandle",\
		#varToBin = "saccLat", factor = "corrDirection", showFig = False, nBin = 15)
	#studies._004B.analyses.binAnalyses.binAnalysesSepLines(dmDriftCorr, dv = "degrTowardsHandleCorrMask",\
		#varToBin = "saccLat", factor = "corrDirection", showFig = False, nBin = 15)
	#sys.exit()
	
	
	# Check the 'heavy_side' variable: 
	#dm = dmDriftCorr.select("handle_side == 'right'")
	#dmHeavyRight = dm.select("heavy_side == 'right'")
	#dmHeavyNeutral = dm.select("heavy_side == 'neutral'")
	#dmHeavyLeft = dm.select("heavy_side == 'left'")

	#print "RIGHT:", np.unique(dmHeavyRight["object"])
	#print "NEUTRAL:", np.unique(dmHeavyNeutral["object"])
	#print "LEFT:", np.unique(dmHeavyLeft["object"])
