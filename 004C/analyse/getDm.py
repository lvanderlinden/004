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
import addCoord2
import addLat
import selectDm
import addCommonFactors

@cachedDataMatrix
def getDm(exp):
	
	"""
	"""
	
	dm = parse.parseAsc(exp = exp, cacheId = "%s_parsed" % exp)
	dm = addCommonFactors.addCommonFactors(dm, cacheId = "%s_common_factors" % exp)
	dm = addCoord.addCoord(dm, cacheId = "%s_coord" % exp)
	if exp == "004A":
		dm = addCoord2.addCoord2(dm, cacheId = "%s_coord_rel_to_abs" % exp)
	
	dm = addLat.addLat(dm, cacheId = "%s_lat" % exp)
	dm = selectDm.selectDm(dm, cacheId = "%s_select" % exp)
	
	return dm

