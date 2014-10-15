# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 16:11:45 2014

@author: lotje
"""
import onObject
import numpy as np
from matplotlib import pyplot as plt
from exparser.CsvReader import CsvReader
from exparser.PivotMatrix import PivotMatrix

exp = "004B"
src = 'selected_dm_%s_WITH_drift_corr_onlyControl_False.csv' % exp
main_dm = CsvReader(src).dataMatrix()
main_dm = main_dm.select("contrast_side != 'control'")


dv = "endX1NormToContrast"
dm = main_dm.select("%s != ''" % dv)
dm = dm.selectByStdDev(["file"], dv)
dm = dm.removeField("__dummyCond__")
dm = dm.removeField("__stdOutlier__")
dm = dm.selectByStdDev(["file"], "saccLat1")

fig = plt.figure()
pm = PivotMatrix(dm, cols = ["visual_field"], \
	rows = ["file"], dv = dv, colsWithin=True)
pm.barPlot(fig = fig)

for vf in ["upper", "lower"]:
	
	_dm = dm.select("visual_field == '%s'" % vf)
	cm = _dm.collapse(["file"], dv)
	m = cm["mean"].mean()
	se = cm['mean'].std() / np.sqrt(len(cm))
	print "VISUAL FIELD = ", vf
	print "DV = ", dv
	print "M = ", m
	print "SE = ", se

plt.savefig("VF_effect.png")


dv = "endX2NormToContrast"
dm = main_dm.select("%s != ''" % dv)
dm = dm.selectByStdDev(["file"], dv)
dm = dm.removeField("__dummyCond__")
dm = dm.removeField("__stdOutlier__")
dm = dm.selectByStdDev(["file"], "saccLat1")

fig = plt.figure()
pm = PivotMatrix(dm, cols = ["response_hand"], \
	rows = ["file"], dv = dv, colsWithin=True)
pm.barPlot(fig = fig)

for rh in ["left", "right"]:
	
	_dm = dm.select("response_hand == '%s'" % rh)
	cm = _dm.collapse(["file"], dv)
	m = cm["mean"].mean()
	se = cm['mean'].std() / np.sqrt(len(cm))
	print "RESPONSE HAND = ", rh
	print "DV = ", dv
	print "M = ", m
	print "SE = ", se


plt.savefig("ResponseHand_effect.png")