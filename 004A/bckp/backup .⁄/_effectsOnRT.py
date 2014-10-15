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
import studies._004B.analyses.anovas
import studies._004B.analyses.binAnalyses

# Define constants:
dvList = ["rtFromStim", "saccLat", "endXCorr", "accuracy"]


if __name__ == "__main__":
	
	# Get the data matrix:
	#dmDriftCorr  = studies._004B.getDM.getDM(driftCorr = True)
	dmCorrect = studies._004.getDM.getDM(driftCorr = True, excludeErrors = True)
	#dmRaw = studies._004B.getDM.getDM(driftCorr = False)
	
	# Effect of compatibility (regardless of hand) on RT:
	# ONLY INCLUDE CONTROL CONDITION
	#studies._004B.analyses.anovas.oneFactor(dmCorrect, \
	#	dv = "rtFromStim", factor = ["comp"], showFig = True, exMask = True, \
		#exFiller = True)
	
	# Affordance effect:
	# ONLY INCLUDE CONTROL CONDITION
	studies._004B.analyses.anovas.twoFactor(dmCorrect, \
		dv = "rtFromStim", factors = ["handle_side", "response_hand"], \
		showFig = False, exMask = True, exFiller = True)
	sys.exit()
	# Affordance effect split per mask condition:
	#studies._004B.analyses.anovas.threeFactor(dmCorrect, \
		#dv = "rtFromLanding", factors = ["mask_side", "response_hand",
		#"handle_side"], showFig = True, exFiller = True, yLim = [300, 800])


	# Simon effect in terms of luminance:
	# EXCLUDE CONTROL CONDITION WITHOUT MASK MANIPULATION:
	#dm = dmCorrect.select("heavy_side == 'neutral'")
	studies._004B.analyses.anovas.twoFactor(dmCorrect, \
		dv = "rtFromStim", factors = ["response_hand", "mask_side"], \
		showFig = True, exControlMask = True)

	# Simon effect in terms of heavy side:
	#studies._004B.analyses.anovas.twoFactor(dmCorrect, \
	#	dv = "rtFromStim", factors = ["response_hand", "heavy_side"], showFig = True, exControlMask = True)
	
	# Three-way interaction between hand, mask and heavy side:
	studies._004B.analyses.anovas.threeFactor(dmCorrect, \
		dv = "rtFromStim", factors = ["heavy_side", "mask_side", \
			"response_hand"], showFig = True, exControlMask = False, \
			yLim = [580, 720])
