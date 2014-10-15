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
import studies._004.getDM
import studies._004.analyses.distributions
import studies._004.analyses.anovas
import studies._004.analyses.binAnalyses
import studies._004.analyses.regressionAnalyses

# Define constants:
dvList = ["rtFromStim", "saccLat", "endXCorr", "accuracy"]


if __name__ == "__main__":
	
	# Get the data matrix:
	dmDriftCorr  = studies._004.getDM.getDM(driftCorr = True)
	dmRaw = studies._004.getDM.getDM(driftCorr = False)
	
	# Look at the distribution of starting positions and landing positions before
	# drift correction is applied:
	#studies._004.analyses.distributions.distHistTwoVars(dmRaw, ['startXDegr', 'endXDegr'],showFig = False,\
	#	zTransform = False, figName = "distHists startX and endX before drift corr.png")
	
	#studies._004.analyses.distributions.distHistTwoVars(dmDriftCorr, ['startXDegr', 'endXDegr'],showFig = False,\
	#	zTransform = False,figName = "distHists startX and endX after drift corr.png")

	# ANOVAs to show that landing positions are explained by CoG and a tendency
	# to land towards the middle of the object:
	
	# Landing as a function of handle side and contrast:
	#studies._004.analyses.anovas.twoFactor(dmRaw, dv = "endXDegr", factors = ["mask_side", "handle_side"], exControlMask = False,
	#exFiller = True, showFig = True)
	
	#studies._004.analyses.anovas.twoFactor(dmRaw, dv = "endXCorrDegr", factors = ["mask_side", "handle_side"], exControlMask = False,
	#exFiller = True, showFig = True)

	#studies._004.analyses.anovas.twoFactor(dmRaw, dv = "endXCorrMaskDegr", factors = ["mask_side", "handle_side"], exControlMask = False,
	#exFiller = True, showFig = True)

	#studies._004.analyses.anovas.twoFactor(dmDriftCorr, dv = "endXDegr", factors = ["mask_side", "handle_side"], exControlMask = False,
	#exFiller = True, showFig = False, yLim = [-0.6, 0.6])
	
	#studies._004.analyses.anovas.twoFactor(dmDriftCorr, dv = "endXCorrDegr", factors = ["mask_side", "handle_side"], exControlMask = False,
	#exFiller = True, showFig = False,yLim = [-0.6, 0.6])

	#studies._004.analyses.anovas.twoFactor(dmDriftCorr, dv = "endXCorrMaskDegr", factors = ["mask_side", "handle_side"], exControlMask = False,
	#exFiller = True, showFig = False,yLim = [-0.6, 0.6])

		### Time course of affordance effect on endX:
	studies._004.analyses.binAnalyses.binAnalysesSepLines(dmDriftCorr, dv = "degrTowardsHandleCorr",\
		varToBin = "saccLat", factor = "corrDirection", showFig = False, nBin = 15)
	studies._004.analyses.binAnalyses.binAnalysesSepLines(dmDriftCorr, dv = "degrTowardsHandle",\
		varToBin = "saccLat", factor = "corrDirection", showFig = False, nBin = 15)
	studies._004.analyses.binAnalyses.binAnalysesSepLines(dmDriftCorr, dv = "degrTowardsHandleCorrMask",\
		varToBin = "saccLat", factor = "corrDirection", showFig = False, nBin = 15)
	sys.exit()

