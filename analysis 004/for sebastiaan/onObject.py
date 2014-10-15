#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: onOjbect.py

"""
DESCRIPTION:
Excludes off-object fixations (determined on only the x-axis,
or both axes, and returns the fitlered DM.

TODO: normalised (x,y) for experiment 2 and 3??????
"""

# Import own modules:
from exparser.DataMatrix import DataMatrix
import getDM

# Import own modules:

def onObject(dm, sacc, exclY = False, verbose = True):
	
	"""
	Excludes off-object fixations and returns filtered dm.
	
	Arguments:
	dm		--- data matrix
	sacc	--- {"1", "2", "3"}, sacc count.
	
	Keyword arguments:
	exclY	--- Boolean indicating whether or not to exclude on the
				y-axis as well. Default = False. 
	verbose --- Default = True
	"""
	
	# X-axis:

	# Exclude trials on which xNorm doesn't exist:
	dm = dm.select("endX%sNorm != ''" % sacc, verbose = verbose)
	# Exclude off-object x coordinates:
	#dm = dm.select("endX%sNorm > -.8" % sacc, verbose = verbose)
	#dm = dm.select("endX%sNorm < .8" % sacc, verbose = verbose)
	
	# Y-axis (optional):
	if exclY:
		# Exclude trials on which yNorm doesn't exist:
		dm = dm.select("endY%sNorm != ''" % sacc, verbose = verbose)
		# Exclude off-object coordinates
		dm = dm.select("endY%sNorm > -.5" % sacc, verbose = verbose)
		dm = dm.select("endY%sNorm < .5" % sacc, verbose = verbose)
		
	return dm

if __name__ == "__main__":
	
	for exp in ["004A", "004B"]:
		
		dm = getDM.getDM(exp)
		
		for sacc in ["1", "2", "3"]:
			_dm = onObject(dm, sacc)
			
			

		