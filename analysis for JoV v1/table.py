#!/usr/bin/env python
#-*- coding:utf-8 -*-

""" 
DESCRIPTION:
Plots landing position as a function of sacc latency (and other predictors, if
wanted), using LMM.
"""


from exparser.CsvReader import CsvReader
from exparser.RBridge import RBridge
from exparser.TangoPalette import *
from matplotlib import pyplot as plt
import getDM
import numpy as np
import sys
import os
import onObject

# Set font:
plt.rc("font", family="arial")
plt.rc("font", size=7)

# Constant variables:
dst = "/home/lotje/Documents/PhD Marseille/Studies/004 - Single-object experiment - Handle-orientation effect/manuscript/Versions/5th draft/Figures JoV/Timecourses"

def lmeRegr(exp, R, dm, sacc, direction, corr=False, color=blue[1], bins=8, \
	fixedRange=False, trim=True, steps=2, nsim=10000, stats=True):

	"""
	Creates a regression plot  with saccade latency on the X axis and
	horizontal gaze bias on the Y axis.

	Arguments:
	R		--	An RBridge object.
	dm		--	A DataMatrix.
	sacc	
	direction


	Generates LME tables (with t-values and SE, instead of p-values and CIs)
	"""

	
	# Determine the names of the dependent variables in the datamatrix
	if corr:
		dv = 'endX%dCorrNorm%s' % (sacc, direction)
	else:
		dv = 'endX%dNorm%s' % (sacc, direction)
	slDv = 'saccLat%d' % sacc

	# Pre-process the datamatrix
	dm = dm.addField('shiftedSaccLat', dtype=float)
	dm = dm.select('saccLat%d != ""' % sacc, verbose=False)
	if trim:
		dm = dm.selectByStdDev(["file"], slDv, verbose=True)
		dm = dm.removeField("__dummyCond__")
		dm = dm.removeField("__stdOutlier__")
		dm = dm.selectByStdDev(["file"], dv, verbose=True)
		print "Trim Exp %s DV %s" % (exp, dv)

		raw_input()

	# Determine avg landing position:
	cm = dm.collapse(["file"], dv)
	m = cm["mean"].mean()
	se = cm['mean'].std() / np.sqrt(len(cm))
	print "Exp = ", exp
	print "DV = ", dv
	print "M = ", m
	print "SE = ", se

	
	R.load(dm)

	# Run a full LME
	if direction == "ToHandle":
		lmerDm = R.lmer(\
			'%s ~ %s + response_hand + y_stim + (1|file) + (1|object)'\
			% (dv, slDv))#, nsim=nsim, printLmer=True)
	elif direction == "ToContrast":
			#lmerDm = R.lmer(\
				#'%s ~ %s + contrast_side + response_hand + handle_side + y_stim + (1|file) + (1|object)'\
				#% (dv, slDv), nsim=nsim, printLmer=True)

		lmerDm = R.lmer(\
			'%s ~ %s + response_hand + handle_side + y_stim + (1|file) + (1|object)'\
			% (dv, slDv))#, nsim=nsim, printLmer=True)


		
	lmerDm._print(sign=5)
	tableDst = "/home/lotje/Studies/004 - Single-object experiment - Handle-orientation effect/manuscript/Versions/6th draft"
	lmerDm.save(os.path.join(tableDst,'lme_%s_%s_sacc_%s_corr_%s.csv' % (exp, direction, sacc, corr)))
	#print
	#raw_input()
	#return lmerDm, x0pos, x0neg
	
def printStats(exp, direction):
	
	"""
	Plots data for one experiment.
	
	Arguments:
	exp		--- {"004A", "004B"}
	"""
	
	if direction == "ToHandle":
		src = 'selected_dm_%s_WITH_drift_corr_onlyControl_True.csv' % exp
	elif direction == "ToContrast":
		src = 'selected_dm_%s_WITH_drift_corr_onlyControl_False.csv' % exp

	if direction == "ToHandle":
		yLim = [-.30,.15]
	elif direction == "ToContrast":
		yLim = [-.15,.1]

	dm = CsvReader(src).dataMatrix()
	if direction == "ToContrast":
		dm = dm.select("contrast_side != 'control'")
	
	R = RBridge()

	lmeRegr(exp, R, dm, sacc=1, direction=direction, corr=False, color=blue[1])
	if exp == "004A":
		lmeRegr(exp, R, dm, sacc=1, direction=direction, corr=True, color=orange[1])
	lmeRegr(exp, R, dm, sacc=2, direction=direction, corr=False, color=blue[1])
	if exp == "004A":	
		lmeRegr(exp, R, dm, direction=direction, sacc=2, corr=True, color=orange[1])
	

if __name__ == "__main__":
	
	for exp in ["004A", "004B"]:
		for direction in ["ToHandle", "ToContrast"]:
			#if exp == "004A" and direction == "ToHandle":
			#	continue
			printStats(exp, direction)
