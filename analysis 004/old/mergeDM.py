#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: mergeDM.py

"""
DESCRIPTION:
Merge dm in order to obtain saccade variables, such as 
landing pos or duration, irrespective of saccade count.

TODO: make more flexible. the script is now specific to 
only 2 dv's. It would be best to automatically merge
ALL saccade properties, such that it takes no keyword
arguments.

"""

# Own modules:
import getDM
import onObject
from exparser.DataMatrix import DataMatrix
import regrAn

# Python modules:
import numpy as np
from matplotlib import pyplot as plt
import sys

def mergeDM(exp):
	
	"""
	exparser
	"""
	
	lDM = []
	dm = getDM.getDM(exp)
	
	for sacc in ["1", "2", "3"]:
		
		# Only on-object:
		on_dm = onObject.onObject(dm, sacc)
		
		# Determine to-be-combined variables:
		if exp == "004A":
			old_dvs = ["endX%sNormToHandle" % sacc, "endX%sCorrNormToHandle" % sacc, "durationFix%s" % sacc]
			new_dvs = ["xToHandle", "xToHandleCorr", "fixDur"]
		else:
			old_dvs = ["endX%sNormToHandle" % sacc, "durationFix%s" % sacc, "saccLat%s" % sacc]
			new_dvs = ["xToHandle", "fixDur", "saccLat"]
		
		for i in range(len(old_dvs)):
		
			old_dv = old_dvs[i]
			new_dv = new_dvs[i]
			
			# Exclude trials on which fix dur has no value
			# NOTE: this should not happen after applying 
			# onObject() filtering.
			on_dm = on_dm.select("%s != ''" % old_dv)
		
			# New cols:
			on_dm = on_dm.addField(new_dv)
			on_dm[new_dv] = on_dm[old_dv]

		lDM.append(on_dm)
		
	# Make one big dm:
	big_dm = lDM[0]
	
	for dm in lDM[1:]:
		big_dm = big_dm + dm
	
	return big_dm



if __name__ == "__main__":

	mergeDM("004A")