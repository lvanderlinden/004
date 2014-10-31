"""
DESCRIPTION:
Makes sure dm's for all experiments contain the factors that we need for
calculating the dv.
"""


import sys
import os
import numpy as np
from exparser.Cache import cachedDataMatrix, cachedArray
from exparser.CsvReader import CsvReader
import parse
import addCoord
import addLat
import selectDm
import addCommonFactors
import analyse
from matplotlib import pyplot as plt
from exparser.TangoPalette import *

@cachedDataMatrix
def getDm(exp):
	
	"""
	"""
	
	if exp == "004C":
		offlineDriftCorr = False
	else:
		offlineDriftCorr = False
	
	dm = parse.parseAsc(exp = exp, cacheId = "%s_parsed_driftcorr_%s" % (exp, \
		offlineDriftCorr), offlineDriftCorr = offlineDriftCorr)
	
	plt.hist(dm["sacc1_ex"], bins = 100)
	plt.show()
	
	dm = addCommonFactors.addCommonFactors(dm, \
		cacheId = "%s_common_factors_driftcorr_%s" % (exp,offlineDriftCorr))
	dm = addCoord.addCoord(dm, cacheId = "%s_coord_driftcorr_%s" % (exp, offlineDriftCorr))
	dm = addLat.addLat(dm, cacheId = "%s_lat_driftcorr_%s" % (exp, offlineDriftCorr))
	dm = selectDm.selectDm(dm, cacheId = "%s_select_driftcorr_%s" % (exp, offlineDriftCorr))
	
	return dm

if __name__ == "__main__":

	for exp in ["004A", "004B", "004C"]:
		
		#if exp != "004C":
		#	continue
		
		dm = getDm(exp = exp, cacheId = "%s_final" % exp)
		print dm.unique("offlineDriftCorr")
		raw_input()
		
		#lCols = allColors
		
		#fig = plt.figure()
		#for pp in dm.unique("file"):
			#ppDm = dm.select("file == '%s'" % pp)
			#col = lCols.pop()
			#analyse.plotDist(ppDm, "saccLat1", col=col, label = pp)
		#plt.legend()
		#plt.show()
			


