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

def lmePerSacc(dm, sacc, dvId, fullModel = False, center = False):
	
	"""
	"""
	
	dm.save('test_dm.csv')
	exp = dm["expId"][0]
	
	# See Barr 2012
	# Note: if I use (1+saccLat%s+stim_type|stim_name) as random effect, nothing
	# is significant
	
	dm = dm.addField("saccLatCen")
	dm["saccLatCen"] = dm["saccLat%s" % sacc] - dm["saccLat%s" % sacc].mean()
	
	print "Sacc = ", sacc
	print "ref = ", dm["saccLat%s" % sacc].mean()
	
	R().load(dm)
	
	dv = "%s%s" % (dvId, sacc)
	saccVar = "saccLat%s" % sacc
	if center:
		saccVar = "saccLatCen"
	
	if dm.count('stim_type') == 1:
		
		if fullModel:
			f = "%s ~ %s*response_hand*y_stim + (1+%s|file) + (1+%s|stim_name)" % \
				(dv, saccVar, saccVar,saccVar)
		else:
			f = "%s ~ %s + (1+%s|file) + (1+%s|stim_name)" % \
				(dv, saccVar, saccVar, saccVar)
			
	else:
		
		if fullModel:
			f = "%s ~ %s*stim_type+correct_response+ecc+visual_field+devAngle + (1+%s+stim_type|stim_name)" % (dv, saccVar, saccVar)
		else:
			f = "%s ~ %s*stim_type + (1+%s+stim_type|stim_name)" % \
				(dv, saccVar, saccVar)
	
			
	lm = R().lmer(f)
	if center:
		if fullModel:
			lm.save("Stats_full_model_exp%s_%s.csv" % (exp, dv))
		else:
			lm.save("Stats_simple_model_exp%s_%s.csv" % (exp, dv))
		
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

	