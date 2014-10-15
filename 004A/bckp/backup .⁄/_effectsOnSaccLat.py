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
import studies._004B.analyses.distributions
import studies._004B.analyses.anovas
import studies._004B.analyses.binAnalyses
import studies._004B.analyses.regressionAnalyses

# Define constants:
dvList = ["rtFromStim", "saccLat", "endXCorr", "accuracy"]


if __name__ == "__main__":
	
	# Get the data matrix:
	dmDriftCorr  = studies._004.getDM.getDM(driftCorr = True)
	dmRaw = studies._004.getDM.getDM(driftCorr = False)
	
	dmCorrect = studies._004.getDM.getDM(driftCorr = True, excludeErrors = True)

	# GAP EFFECT:

	## Distributions:
	#studies._004B.analyses.distributions.distHistSplit(dmCorrect, "saccLat", \
		#'gap' ,showFig = False, zTransform = False, nBin = 100)

	#studies._004B.analyses.distributions.distHistSplit(dmCorrect, "saccLat", \
		#'gap' ,showFig = False, zTransform = True, nBin = 100)
	
	## One-way anova:
	#studies._004B.analyses.anovas.oneFactor(dmCorrect, "saccLat", ["gap"], showFig = False, yLim = 120)

	# CONTRAST EFFECT:
	
	# One-way anova:
	#studies._004B.analyses.anovas.oneFactor(dmCorrect, "saccLat", ["mask_side"], showFig = False, yLim = 160)

