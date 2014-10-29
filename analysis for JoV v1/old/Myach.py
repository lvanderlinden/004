#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: Myach.py

"""
DESCRIPTION:
Discrepancy between Myachykov et al. (2013) and our results.

One important difference is the dependent variable:
Landing positions versus proportional dwell times.

Although using their exact methods is not a good idea, because
- subjective: what is handle
- not possible for some of our objects to determine the border
between handle and 'body'

we try to investigate whether IF the eyes land on the handle,
they stay there longer.

Still, note that their interpretation: handles automatically
attract visual attention, is not replicated by us anyway.

TODO: 
some refixations DO have a value for landing pos, but not
for duration -> see in ascParser where this goes wrong...
Perhaps because the duration of the last fixation in the trial
is caclulated differently (e.g RT - latency)??
slope = -86.14, intercept = 270.22, R = -0.10, p = 0.000, SE = 14.09

TODO:
Try to fit other than linear functions??
Maybe in SPSS?

TODO: trim two dv's
"""

# Own modules:
import getDM
import onObject
from exparser.DataMatrix import DataMatrix
import regrAn
import mergeDM

# Python modules:
import numpy as np
from matplotlib import pyplot as plt
import sys

def Myach():
	
	"""
	"""
	
	for exp in ["004A", "004B"]:
		
		big_dm = mergeDM.mergeDM(exp)
		
		if exp == "004A":
			dvList = ["xToHandle", "xToHandleCorr"]
		else:
			dvList = ["xToHandle"]
		
		for dv in dvList:
			
			#trimmed_dm = big_dm.selectByStdDev(keys = ["file"], dv = dv)
			#_trimmed_dm = trimmed_dm.selectByStdDev(keys = ["file"], dv = "fixDur")
			
			trimmed_dm = big_dm.selectByStdDev(keys = ["file"], dv = "fixDur")
			figName = "Exp %s: correlation between %s and fix dur" % (exp, dv)
			regrAn.regrAn(trimmed_dm, [dv, "fixDur"], figName = figName)
	
if __name__ == "__main__":

	Myach()