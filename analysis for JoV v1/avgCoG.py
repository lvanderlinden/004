# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 12:30:26 2013

@author: lotje
"""

import numpy as np
import os
import sys

# Import own modules:
from exparser.DataMatrix import DataMatrix
from exparser.PivotMatrix import PivotMatrix
from exparser.CsvReader import CsvReader
import ascParser
import constants
import getDM
import onObject

w = constants.wBitmap
h = constants.hBitmap
print w
print h


# Determine average cog of objects used for analysis of initial saccade in
# Experiment 2:
dm = getDM.getDM("004B", onlyControl = False)

handle_dm = dm.select("handle_side == 'right'")

for mask in ["left", "right", "control"]:
	mask_dm = handle_dm.select("mask_side == '%s'" % mask)
	l = []
	for stim in mask_dm.unique("object"):
		stim_dm = mask_dm.select("object == '%s'" % stim, verbose = False)		
	
		for cog in stim_dm.unique('xCoGMask'):
			norm_cog = cog
			print stim, norm_cog
			l.append(norm_cog)
	print "average cog all objects weighted equally:"
	a = np.asarray(l)
	avg_cog_overall = a.mean()/w
	print avg_cog_overall*100
