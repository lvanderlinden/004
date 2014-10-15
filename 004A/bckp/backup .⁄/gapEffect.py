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
import parseAsc
import studies._004.getDM
import studies._004.analyses.distributions
import studies._004.analyses.anovas
import studies._004.analyses.binAnalyses
import studies._004.analyses.regressionAnalyses

# Define constants:
dvList = ["rtFromStim", "saccLat", "endXCorr", "accuracy"]


if __name__ == "__main__":
	
	# Get the data matrix:
	dm = parseAsc.parseAsc()
	
	dmAll = studies._004.getDM.getDM(dm)
	#dmCorrect = studies._004.getDM.getDM(dm,excludeErrors = True)
	
	# Distributions split per gap:
	studies._004.analyses.distributions.distHistSplit(dm, "saccLat", "gap", \
		showFig = True, nBin = 100)
	

	# Replication of Goldring & Fischer:
	# The direction of the two-way interactio changed after I changed some
	# exclusion criteria in getDM(). Now, the gap effect is more pronounced
	# in upwards saccades (in contrast to what I found before and in contrast
	# to Goldring & Fischer).
	#studies._004.analyses.anovas.twoFactor(dmAll, dv = "saccLat", \
	#	factors = ["visual_field","gap"],showFig = True)
	
	# Does strength of the gap effect depend on repetition?
	studies._004.analyses.anovas.twoFactor(dmAll, dv = "saccLat", \
		factors = ["gap", "rep"],showFig = True)

	# Does strength of the gap effect depend on binned sacclat?
	studies._004.analyses.binAnalyses.binAnalyses(dmAll, dv = "saccLat", \
		varToBin = "saccLat", factor = "gap",showFig = True)
		

	## ANOVAs to show that luminance effect is explained by CoG:
	#studies._004.analyses.anovas.oneFactor(dmAll, dv = "endXDegr", \
		#factor = ["mask_side"], exControlMask = False, \
			#exFiller = False, showFig = False, printStats = True, yLim = (-.5,.1))

	#studies._004.analyses.anovas.oneFactor(dmAll, dv = "endXCorrDegr", \
		#factor = ["mask_side"], exControlMask = False, \
			#exFiller = False, showFig = False, printStats = True, yLim = (-.5,.1))

	#studies._004.analyses.anovas.oneFactor(dmAll, dv = "endXCorrMaskDegr", \
		#factor = ["mask_side"], exControlMask = False, \
			#exFiller = False, showFig = False, printStats = True, yLim = (-.5,.1))
	#sys.exit()

	## INTERACTIONS between low-level factors?
	#studies._004.analyses.anovas.oneFactor(dmAll, dv = "saccLat", \
		#exControlMask = True, factor = ["mask_side"], yLim = 150, showFig = True)	
	#studies._004.analyses.anovas.oneFactor(dmAll, dv = "saccLat", \
		#exControlMask = True,factor = ["gap"], yLim = 150, showFig = True)
	#studies._004.analyses.anovas.twoFactor(dmAll, dv = "saccLat",\
		#exControlMask = True, factors = ["mask_side", "gap"], showFig = True)
	#sys.exit()
	
	# Landing positions as a function of binned latency and mask:
	#studies._004.analyses.binAnalyses.binAnalysesSepLines(dmAll, dv = "endXDegr",\
		#varToBin = "saccLat", factor = "mask_side", showFig = False)
	#studies._004.analyses.binAnalyses.binAnalysesSepLines(dmAll, dv = "endXCorrDegr",\
		#varToBin = "saccLat", factor = "mask_side", showFig = False)
	#studies._004.analyses.binAnalyses.binAnalysesSepLines(dmAll, dv = "endXCorrMaskDegr",\
		#varToBin = "saccLat", factor = "mask_side", showFig = False)

	##Distributions per dv per iv:
	#for dv in ["endXDegr", "endXCorrDegr", "rtFromStim", "rtFromObject"]:
		#for z in [True, False]:
			#for factor in ["file", "gap", "handle_side", "mask_side"]:
				#studies._004.analyses.distributions.distHistSplit(dmAll, dv = dv, \
					#factor = factor, showFig = False, zTransform = z)
	
	# Bin analyses:
	
	# Time course of affordance effect on RT:
	#studies._004.analyses.binAnalyses.binAnalyses(dmAll, dv = "rtFromStim",\
		#varToBin = "saccLat", factor = "comp", showFig = False)
	#studies._004.analyses.binAnalyses.binAnalyses(dmCorrect, dv = "rtFromStim",\
		#varToBin = "rtFromStim", factor = "comp", showFig = False)

	#studies._004.analyses.binAnalyses.binAnalyses(dmCorrect, dv = "rtFromLanding",\
		#varToBin = "rtFromLanding", factor = "comp", showFig = False)

	
	### Time course of affordance effect on endX:
	#studies._004.analyses.binAnalyses.binAnalysesSepLines(dmAll, dv = "degrTowardsHandleCorr",\
		#varToBin = "saccLat", factor = "corrDirection", showFig = False, nBin = 15)
	#studies._004.analyses.binAnalyses.binAnalysesSepLines(dmAll, dv = "degrTowardsHandle",\
		#varToBin = "saccLat", factor = "corrDirection", showFig = False, nBin = 15)
	#studies._004.analyses.binAnalyses.binAnalysesSepLines(dmAll, dv = "degrTowardsHandleCorrMask",\
		#varToBin = "saccLat", factor = "corrDirection", showFig = False, nBin = 15)
	#sys.exit()
	
	#studies._004.analyses.binAnalyses.binAnalyses(dmAll, dv = "pxTowardsHandleCorr",\
		#varToBin = "rtFromStim", factor = "comp", showFig = False)
	#studies._004.analyses.binAnalyses.binAnalyses(dmAll, dv = "pxTowardsHandle",\
		#varToBin = "rtFromStim", factor = "comp", showFig = False)
	
	#studies._004.analyses.regressionAnalyses.regrAn(dmCorrect, \
		#["saccLat","pxTowardsHandleCorr"], showFig = True)
	#studies._004.analyses.regressionAnalyses.regrAn(dmCorrect, \
		#["saccLat","pxTowardsHandleCorr"], showFig = True)
	#sys.exit()


	## Regression:
	#studies._004.analyses.regressionAnalyses.regrAn(dmAll, ["jitter_dur", "rtFromStim"])
	#studies._004.analyses.regressionAnalyses.regrAn(dmAll, ["saccLat", "rtFromStim"])
	#studies._004.analyses.regressionAnalyses.regrAn(dmAll, ["jitter_dur", "saccLat"])

	# Anovas:

	# One-factorial
#	studies._004.analyses.anovas.oneFactor(dmCorrect, dv = "rtFromStim", \
#		factor = ["comp"], yLim = [650,700])

	# AFFORDANCE:
	studies._004.analyses.anovas.twoFactor(dmCorrect, dv = "rtFromStim", \
		factors = ["handle_side", "response_hand"], exControlMask = False, \
			exFiller = True, showFig = False, printStats = True, exMask = False)

	studies._004.analyses.anovas.twoFactor(dmCorrect, dv = "rtFromLanding", \
		factors = ["handle_side", "response_hand"], exControlMask = False, \
			exFiller = True, showFig = False, printStats = True, exMask = False)
	
	# SIMON:
	studies._004.analyses.anovas.twoFactor(dmCorrect, dv = "rtFromStim", \
		factors = ["response_hand", "mask_side"], exControlMask = True, \
			exFiller = True, showFig = False, printStats = True)

	studies._004.analyses.anovas.twoFactor(dmCorrect, dv = "rtFromLanding", \
		factors = ["response_hand", "mask_side"], exControlMask = True, \
			exFiller = True, showFig = False, printStats = True)


	sys.exit()


	# Two-factorial:
	for dv in ["endX", "endXCorr"]:
		
		studies._004.analyses.anovas.twoFactor(dmCorrect, dv = "endXCorr", \
			factors = ["handle_side", "mask_side"], exControlMask = True, exFiller = True)
		studies._004.analyses.anovas.twoFactor(dmCorrect, dv = "endX", \
			factors = ["handle_side", "mask_side"], exControlMask = True, exFiller = True)
	
	sys.exit()
	
	for dv in ["rtFromStim", "accuracy"]:
		
		if dv == "accuracy":
			_dm = dmAll
		else:
			_dm = dmCorrect
			
		studies._004.analyses.anovas.twoFactor(_dm, dv = dv, \
			factors = ["response_hand", "mask_side"])
		studies._004.analyses.anovas.twoFactor(_dm, dv = dv, \
			factors = ["response_hand", "handle_side"])
		studies._004.analyses.anovas.twoFactor(_dm, dv = dv, \
			factors = ["comp", "visual_field"])
	
	
	
	# Three-factorial"
	dv = "endXCorr"
	studies._004.analyses.anovas.threeFactor(dmCorrect, dv, \
		["visual_field", "response_hand", "handle_side"])

	# Distribution histograms:
	studies._004.analyses.distributions.overallDistr(dm, "jitter_dur")

	for dv in ["rtFromStim", "saccLat"]:
		studies._004.analyses.distributions.overallDistr(dm, dv = dv)
		studies._004.analyses.distributions.splitDistr(dm, dv = dv, factor = "gap")
		studies._004.analyses.distributions.splitDistr(dm, dv = dv, factor = "mask_side")
	
		
	## RT effects:
	dv = "rtFromStim"

	functions.affordanceVF(dmCorrect, dv = dv, showFig = False, exSymm = True, \
		printStats = True)
	#functions.gapEffect(dmCorrect, dv = dv, trim = True)
	
	## Accuracy effects:
	dv = "accuracy"
	functions.affordanceVF(dmAll, dv = dv, showFig = False, printStats = True, \
		trim = False)
	sys.exit()
	

