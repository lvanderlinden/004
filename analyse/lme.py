"""
DESCRIPTION:
Analyses for 004C
"""

import parse
from exparser.Cache import cachedDataMatrix, cachedArray
from exparser.PivotMatrix import PivotMatrix
from exparser.RBridge import R
from matplotlib import pyplot as plt
from exparser.TangoPalette import *
import numpy as np
import sys
import constants
import getDm
import getSaccDm

def lmePerSacc(dm, sacc, fullModel = False):
	
	"""
	"""
	
	R().load(dm)
	
	exp = dm["expId"][0]
	
	# See Barr 2012
	# Note: if I use (1+saccLat%s+stim_type|stim_name) as random effect, nothing
	# is significant
	
	if dm.count('stim_type') == 1:
		
		if fullModel:
			f = "xNorm%s ~ saccLat%s*response_hand*y_stim + (1+saccLat%s|file) + (1+saccLat%s|stim_name)" % \
				(sacc, sacc, sacc, sacc)
		else:
			f = "xNorm%s ~ saccLat%s + (1+saccLat%s|file) + (1+saccLat%s|stim_name)" % \
				(sacc, sacc, sacc, sacc)
			
	else:
		
		if fullModel:
			f = "xNorm%s ~ saccLat%s*stim_type+correct_response+ecc+visual_field+devAngle + (1+saccLat%s+stim_type|stim_name)" % (sacc, sacc, sacc)
		else:
			f = "xNorm%s ~ saccLat%s*stim_type + (1+saccLat%s+stim_type|stim_name)" % \
				(sacc, sacc, sacc)
			
	lm = R().lmer(f)
	if fullModel:
		lm.save("Stats_full_model_exp%s_sacc%s.csv" % (exp, sacc))
	else:
		lm.save("Stats_simple_model_exp%s_sacc%s.csv" % (exp, sacc))
		
	return lm


if __name__ == "__main__":
	
	norm = True
	removeOutliers = True

	for exp in ["004A", "004C"]:
		
		if exp == "004A":
			continue
		
		dvId = "xNorm"
		dm = getDm.getDm(exp = exp, cacheId = "%s_final" % exp)
		lme(dm, dvId, fullModel = False)

	