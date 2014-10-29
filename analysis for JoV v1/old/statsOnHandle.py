#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: landOnHandle.py

"""
Landing positions as a function of object orientation (across and
per 'object group').

ANOVA's
Bin analyses
"""

# Import Python modules:
import numpy as np
import os
import sys
from matplotlib import pyplot as plt
import scipy.stats

# Import own modules:
from exparser.DataMatrix import DataMatrix
from exparser.PivotMatrix import PivotMatrix
from exparser.AnovaMatrix import AnovaMatrix
import getDM
import onObject
import constants

dst = "/home/lotje/Documents/PhD Marseille/Studies/004 - Single-object experiment - Handle-orientation effect/manuscript/sources"

def landOnHandle(trim = True, spacing = .5, exclOverlap = False, \
	exclY = False, colList = ["#ef2929", "#3465a4", "#f57900", "#73d216"],\
		lLegend = ["Exp1: relative to center", "Exp1: relative to CoG", \
		"Exp2: relative to CoG", "Exp3: relative to CoG"], yLim = [-.3, .3],\
		xLabels = ["1", "2", "3"], xTitle = "saccade", \
		yTitle = "normalised landings towards handle"):
	
	"""
	Landing position as a funciton of orientation, across or per object group.
	
	Arguments:
	
	Keyword arguments:
	trim			--- 
	exclOverlap		--- indicates whether or not to exclude gap-overlap trials
						in the simulation.
	"""
	
	fig = plt.figure(figsize = (5,10))
	title = "Average towards-handle landings - exclOverlap = %s - exclY = %s" \
		% (exclOverlap, exclY)
	plt.suptitle(title)
	copyColList = colList[:]
	
	dm_sim = getDM.getDM("004C")
	
##	for handle in ["right", "left"]:
##		handle_dm = dm_sim.select("handle_side == '%s'" % handle)
##		print handle_dm["endX1NormToHandle"].mean()
#
#	cm = dm_sim.collapse(['object'], 'endX1NormToHandle')
#	cm._print(sign=5)
#
#	dm_sim = dm_sim.select('object == "fork"')
#	for _dm in dm_sim:
#		print '%d: %.4f' % (_dm['count_trial_sequence'], \
#			_dm['endX1NormToHandle'])
#	cm = dm_sim.collapse(['gap', 'handle_side'], 'endX1NormToHandle')
#	cm._print(sign=5)
#	sys.exit()

	for exp in ["004A", "004B", "004C"]:
		
		if exp != "004B":
			continue
		
#		l = []
#		if exp != "004A":
#			continue
		
		dm = getDM.getDM(exp)
		for vf in dm.unique("visual_field"):
			_dm = dm.select("visual_field == '%s'" % vf)
			plt.hist(_dm["y_stim"], bins = 50)
			plt.show()
		
		sys.exit()
		
		if exp == "004A":
			dvList = ["abs", "corr"]
		else:
			dvList = ["abs"]
		
		for dvType in dvList:
			lMeans = []
			
			for sacc in ["1", "2", "3"]:

				sim_avg = float(dm_sim["endX%sNormToHandle" % sacc].mean())
				print sim_avg
				#raw_input()
				
				if dvType == "corr":
					dv = "endX%sCorrNormToHandle" % sacc
				else:
					dv = "endX%sNormToHandle" % sacc
			
				# dv must not contain ''s:
				on_dm = onObject.onObject(dm, sacc)
			
				if trim:
					trim_dm = on_dm.selectByStdDev(keys = ["file"], dv = dv)
				else:
					trim_dm = on_dm
					
				
				pm = PivotMatrix(trim_dm, ["catch_trial"], ["file"], dv, \
					colsWithin = False, err = 'se')
				a = pm.asArray()
#				print pm				
				M = float(a[-2][2])
				SE = float(a[-1][2])
#				print M
#				print SE
				#sys.exit()
				#M = cdm["mean"].mean()
				#SE = cdm["se"].mean()								
				#print M
				#print SE
				
				
				print "exp ", exp
				print "sacc = ", sacc
				print "dv = ", dv
				am = AnovaMatrix(trim_dm, ["handle_side"], "endX%sNorm" % \
					sacc, "file")#._print(ret=True)
#				print am
				p =  am.asArray()[2][3]
				p_corr = float(p) * 6
#				print p_corr
				
				print 'T test scipy'
				
				cm = trim_dm.collapse(["file"], dv)
				M = cm["mean"].mean()
				SE = cm['mean'].std() / np.sqrt(len(cm))
				ref = 0
				
				t, p = scipy.stats.ttest_1samp(cm['mean'], ref)				
				p_corr = min(1, float(p * 6.))
#				print p_corr
				print "M = %.3f, SE = %.3f, t(17) = %.2f, p = %6.4f" % \
					(M, SE, t, p_corr)
				raw_input()
				
	

	
def perFactor(factor, trim = True, exclY = False, \
	colList = ["#ef2929", "#3465a4","#73d216", "#f57900"], \
	yLim = [-.5, .5], lLegend = \
	["exp1: relative to center", "exp1: relative to CoG",\
	"exp2: relative to CoG", "exp3: relative to CoG"], \
	yTitle = "normalised landing position"):
	
	"""
	Per factor seperately (as for ECEM plots).
	
	NOTE: splitting per factor can't be done for the third saccade
	
	Arguments:
	factor
	"""
	
	l = []
	
	fig = plt.figure()
	title = "Per %s - exclY = %s" % (factor, exclY)
	
	for sacc in ["1", "2"]:
		
		plt.subplot(1,2,int(sacc))
		plt.title('sacc = %s' % sacc)
		copyColList = colList[:]
		
		for exp in ["004A", "004B", "004C"]:
			
			if exp != "004B":
				continue
			dm = getDM.getDM(exp = exp)
			
			# Only include on-object saccades:
			on_dm = onObject.onObject(dm, sacc, exclY = exclY)
			
			if exp == "004A":
				dvList = ["endX%sNormToHandle" % sacc, "endX%sCorrNormToHandle" % sacc]
			else:
				dvList = ["endX%sNormToHandle" % sacc]
				
			for dv in dvList:

				if trim:
					trimmed_dm = on_dm.selectByStdDev(keys = [factor, "file"], dv = dv)
				else:
					trimmed_dm = on_dm
				
				
				
				if exp != "004C":
					am = AnovaMatrix(trimmed_dm, [factor], dv = dv, \
						subject = "file")._print(ret=True)
					print "Exp = ", exp
					print "DV = ", dv
					print "SACC = ", sacc
					print am
					raw_input()

if __name__ == "__main__":
	
	landOnHandle()
	#for f in ["handle_side", "response_hand"]:
	#	perFactor(f)
	