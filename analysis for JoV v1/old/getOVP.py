#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: landOnHandle.py

"""
Landing positions as a function of object orientation (across and
per 'object group').

ANOVA's
Bin analyses
"""

# Import Python modules:
import numpy as np
import os
import sys
from matplotlib import pyplot as plt
import scipy.stats

# Import own modules:
from exparser.DataMatrix import DataMatrix
from exparser.PivotMatrix import PivotMatrix
from exparser.AnovaMatrix import AnovaMatrix
import getDM
import onObject
import constants

dst = "/home/lotje/Documents/PhD Marseille/Studies/004 - Single-object experiment - Handle-orientation effect/manuscript/sources"

def ovp(dm, dv, binVar = "endX1Norm", ws = True,nBin = 5):
	
	"""
	Plots a given dv as a function of binned landing pos.
	
	Arguments:
	dm --- 
	dv --- y axis
	
	ws --- within-subjects binnig
	binVar --- to-be-binned dv, for x-axis
	"""
	
	# Determine whether or not to first split data per participant
	# (i.e. to make within-subjects bins):
	if ws:
		keys = ['file']
	else:
		keys = None
		
	binnedVar = "binned_%s"%binVar
	dm = dm.addField(binnedVar)
	dm = dm.calcPerc(binVar, binnedVar,keys = keys, nBin = nBin)
	
