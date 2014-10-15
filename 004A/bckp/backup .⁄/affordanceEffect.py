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
	
	# Is there an affordance effect  on accuracy?
	dmAll = studies._004.getDM.getDM(dm)
	
	#studies._004.analyses.anovas.\
	#	twoFactor(dmAll, 'accuracy', ["handle_side", "response_hand"],showFig = True)

	# Is there an affordance effect on (different types of) RT?
	dmCorrect = studies._004.getDM.getDM(dm,excludeErrors = True)
	
	for rtVar in ('rtFromStim', 'rtFromLanding', 'rtFromSuccess'):
		
		
		# Those cutoffs are determined by looking at disthists, but I don't 
		# think we should use them, because according to the delta plots,
		# affordances appear to progressively build up over time:
		if rtVar == 'rtFromStim':
			cutoff = 1200
		if rtVar == 'rtFromLanding':
			cutoff = 950
		if rtVar == 'rtFromSuccess':
			cutoff = 800
		
		# Exclude too late saccades, if wanted:
		#_dm = dm.select('%s < %s'%(rtVar,cutoff))
		_dm = dmCorrect
		
		# Affordance effect on RT:
		studies._004.analyses.anovas.\
			twoFactor(_dm, rtVar, ["handle_side", "response_hand"],showFig = True)
	
		# Affordance effect as a function of repetition:
		#studies._004.analyses.anovas.twoFactor(_dm, dv = rtVar, \
			#factors = ["comp", "rep"],showFig = True)
			
		# Affordance effect as a function of binned RT:
		#studies._004.analyses.binAnalyses.\
		#	binAnalyses(_dm, rtVar, rtVar, "comp",showFig = True)
	

	
	sys.exit()

