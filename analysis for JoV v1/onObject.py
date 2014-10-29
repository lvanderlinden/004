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
from matplotlib import pyplot as plt
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
	
	from matplotlib import pyplot as plt
	
	

	#for exp in ["004A", "004B"]:
	dv = "endX1NormToHandle"

	for exp in ["004B"]:	
		main_dm = getDM.getDM(exp, onlyControl=True)
		
		for handle in ["left", "right"]:
			plt.title(handle)
			
			dm = main_dm.select("handle_side == '%s'" % handle)
		
			dm = onObject(dm,"1")
			dm = dm.selectByStdDev(["file"], dv, verbose=True)
			dm = dm.addField("newDV")
			
#			dm = dm.withinize(dv, "newDV", \
#				["object", "file", "gap", "visual_field", \
#				"response_hand"])

			dm = dm.withinize(dv, "newDV", \
				["object"])
			
			plt.subplot(211)
			plt.hist(dm[dv],bins=50)
			plt.subplot(212)
			plt.hist(dm["newDV"], bins = 50)
			plt.show()
		
#
#		print dm["startX1"].mean()
#	
#		
#		plt.hist(dm["startX1"], bins=20)
#		plt.axvline(0)
#		plt.show()
#		
#		#for sacc in ["1", "2", "3"]:
#		#	_dm = onObject(dm, sacc)
#			
			

		