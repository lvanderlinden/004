"""
DESCRIPTION:
Prepare DVs for statistical analyses: LP relative to CoG, normalized for 
object size and orientation
"""


import sys
import os
import numpy as np
from exparser.Cache import cachedDataMatrix, cachedArray

@cachedDataMatrix
def addLat(dm):
	
	"""
	Add sacc latency relative to stimulus onset
	
	Arguments:
	dm		--- A datamatrix instance.
	"""
	count = 0
	
	# Add col headers:
	#for sacc in range(1, int(max(dm["saccCount"])) + 1):
	# HACK: only the first 5 saccades:
	for sacc in range(1, 6):
		dm = dm.addField("saccLat%s" % sacc)
	
	# Walk through trials:
	for i in dm.range():
		stimOnset = dm["stim_onset"][i]
		saccTot = int(dm["saccCount"][i])

		for sacc in range(1,saccTot +1):
			
			# HACK:
			if sacc > 5:
				continue
			
			sSacc= dm["sacc%s_sTime" % sacc][i]
			saccLat = sSacc - stimOnset
			dm["saccLat%s" % sacc][i] = saccLat
	
	return dm		

	