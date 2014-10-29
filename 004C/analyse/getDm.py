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

@cachedDataMatrix
def getDm(exp):
	
	"""
	"""
	
	dm = parse.parseAsc(exp = exp, cacheId = "%s_parsed" % exp)
	dm = addCommonFactors.addCommonFactors(dm, cacheId = "%s_common_factors" % exp)
	dm = addCoord.addCoord(dm, cacheId = "%s_coord" % exp)
	dm = addLat.addLat(dm, cacheId = "%s_lat" % exp)
	dm = selectDm.selectDm(dm, cacheId = "%s_select" % exp)
	
	return dm

