# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 16:11:45 2014

@author: lotje
"""

src = 'selected_dm_%s_WITH_drift_corr_onlyControl_False.csv' % exp
dm = CsvReader(src).dataMatrix()

for sacc in ["1", "2"]:
	dv = "endX%sCorrNormToHandle" % sacc
	else:
		dv = "endX%sNormToHandle" % sacc

	# dv must not contain ''s:
	on_dm = onObject.onObject(dm, sacc)
	trim_dm = on_dm.selectByStdDev(keys = ["file"], dv = dv)
	
	# Determine avg landing position:
	cm = trim_dm.collapse(["file"], dv)
	print len(cm)
	m = cm["mean"].mean()
	se = cm['mean'].std() / np.sqrt(len(cm))
	ci = se * constants.critVal
	lMeans.append(m)
	errMeans.append(ci)
