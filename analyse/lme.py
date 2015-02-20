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

def lmePerSacc(dm, sacc, dvId, fullModel = False, center = False, changeRef = False):
	
	"""
	"""
	

	changeRef = False

	dm.save('test_dm.csv')
	exp = dm["expId"][0]
	
	# See Barr 2012
	# Note: if I use (1+saccLat%s+stim_type|stim_name) as random effect, nothing
	# is significant
	
	dm = dm.addField("saccLatCen%s" % sacc)
	dm["saccLatCen%s" % sacc] = dm["saccLat%s" % sacc] - dm["saccLat%s" % sacc].mean()
	
	if center:
		print "Sacc = ", sacc
		print "ref = ", dm["saccLat%s" % sacc].mean()
		#raw_input()
	
	dm = dm.addField("stim_type2", dtype =str)
	dm["stim_type2"] = dm["stim_type"]
	dm["stim_type2"][dm.where("stim_type == 'object'")] = "A_object"
	
	if changeRef == False:
		iv = "stim_type"
	else:
		iv = "stim_type2"

	
	dm = dm.addField("visual_field2", dtype = str, default = "vf1")
	dm["visual_field2"][dm.where("visual_field == 'lower'")] = "vf2"
	
	dm = dm.addField("response_hand", dtype = str, default = "right")
	dm["response_hand"][dm.where("correct_response == 1")] = "left"
	
	dm.save("Voor_Bas_Sacc%s.csv" % sacc)
	
	R().load(dm)
	
	dv = "%s%s" % (dvId, sacc)
	
	if not center:
		saccVar = "saccLat%s" % sacc
	elif center:
		saccVar = "saccLatCen%s" % sacc
	else:
		raise Exception("Check Boolean center")
	if dm.count('stim_type') == 1:
		
		if fullModel:
			lm = f = None
			f = "%s ~ %s*response_hand*y_stim + (1+%s|file) + (1+%s|stim_name)" % \
				(dv, saccVar, saccVar,saccVar)
			lm = R().lmer(f)
			lm.save("%s.csv" % f)
			lm.save("%s_fullModel_%s_center_%s_Sacc%s.csv" % (exp, fullModel, center, sacc))
		else:
			lm = f = None
			f = "%s ~ %s + (1+%s|file) + (1+%s|stim_name)" % \
				(dv, saccVar, saccVar, saccVar)
			lm = R().lmer(f)
			lm.save("%s_fullModel_%s_center_%s_Sacc%s.csv" % (exp, fullModel, center, sacc))
			
			
	else:
		
		if fullModel:
			if not changeRef:
				#lm = f = None
				#f = "%s ~ %s*stim_type+response_hand+ecc+visual_field2+devAngle + (1+%s+stim_type|file) + (1+%s+stim_type|stim_name)" % (dv, saccVar, saccVar, saccVar)
				#lm = R().lmer(f)
				#lm.save("%s_fullModel_%s_center_%s_Sacc%s.csv" % (exp, fullModel, center, sacc))

				##lm = f = None
				##f = "%s ~ %s*stim_type+visual_field2+devAngle + (1+%s+stim_type|file) + (1+%s+stim_type|stim_name)" % (dv, saccVar, saccVar, saccVar)
				##lm = R().lmer(f)
				##lm.save("%s_fullModel_%s_center_%s_Sacc%s.csv" % (exp, fullModel, center, sacc))


				lm = f = None
				f = "%s ~ %s*stim_type+devAngle + (1+%s+stim_type|file) + (1+%s+stim_type|stim_name)" % (dv, saccVar, saccVar, saccVar)
				lm = R().lmer(f)
				lm.save("%s_fullModel_%s_center_%s_Sacc%s.csv" % (exp, fullModel, center, sacc))




			else:
				#lm = f = None
				#f = "%s ~ %s*stim_type2+response_hand+ecc+visual_field2+devAngle + (1+%s+stim_type2|file) + (1+%s+stim_type2|stim_name)" % (dv, saccVar, saccVar, saccVar)
				#lm = R().lmer(f)
				#lm.save("%s_fullModel_%s_center_%s_Sacc%s.csv" % (exp, fullModel, center, sacc))

				lm = f = None
				f = "%s ~ %s*stim_type2+visual_field2+devAngle + (1+%s+stim_type2|file) + (1+%s+stim_type2|stim_name)" % (dv, saccVar, saccVar, saccVar)
				lm = R().lmer(f)
				lm.save("%s_fullModel_%s_center_%s_Sacc%s.csv" % (exp, fullModel, center, sacc))




		else:
			lm = f = None
			f = "%s ~ %s*stim_type + (1+%s+stim_type|file) + (1+%s+stim_type|stim_name)" % \
				(dv, saccVar, saccVar, saccVar)
			lm = R().lmer(f)
			lm.save("%s_fullModel_%s_center_%s_Sacc%s.csv" % (exp, fullModel, center, sacc))
	
	#if fullModel:

		#lm.save("Stats_full_model_exp%s_%s_centered_%s.csv" % (exp, dv, center))
	#else:

		#print "centered = ", center
		#print "DV = ", dv
		#print "Sacc var = ", saccVar
		#raw_input()

		#lm.save("Stats_simple_model_exp%s_%s_centered_%s.csv" % (exp, dv, center))
		
	return lm



if __name__ == "__main__":
	
	
	norm = True
	removeOutliers = True

	for exp in ["004A", "004C"]:
		
		if exp == "004A":
			continue
		
		dvId = "xNorm"
		dm = getDm.getDm(exp = exp, cacheId = "%s_final" % exp)
		
		
		#print dm.unique("devAngle")
		#sys.exit()
		lme(dm, dvId, fullModel = False)

	