#!/usr/bin/env python
#-*- coding:utf-8 -*-

""" 
DESCRIPTION:
Plots affordance effect and tests for significance using LME.

NOTE: I used rtFromStim for the final analysis!
"""


from exparser.CsvReader import CsvReader
from exparser.PivotMatrix import PivotMatrix
from exparser.RBridge import RBridge
from exparser.TangoPalette import *
from matplotlib import pyplot as plt
import getDM
import numpy as np
import sys
import os

# Set font:
plt.rc("font", family="arial")
plt.rc("font", size=7)

# Constant variables:
dst = "/home/lotje/Studies/004 - Single-object experiment - Handle-orientation effect/manuscript/Versions/5th draft/Figures JoV"


def lmeAff(R, dm, rtVar, nsim=10000, exp="exp?"):

	"""
	Creates a regression plot  with saccade latency on the X axis and
	horizontal gaze bias on the Y axis.

	Arguments:
	R		--	An RBridge object.
	dm		
	rtVar		-- {"RT", "rtFromlanding", "rtFromStim"}

	Keyword arguments:
	nsim			--	The number of MCMC simulations passed onto pvals.fnc().
					Decrease to increase speed. (default=10000)
	"""

	R.load(dm)

	# Run a full LME
	lmerDm = R.lmer(\
		'%s ~ response_hand * handle_side + (1|file) + (1|object)' % rtVar, \
		nsim=nsim, printLmer=True)
	lmerDm._print(sign=5)
	lmerDm.save('lme_affordance_%s.csv' % exp)
	print 'Done!'		

def plotAff(rtVar, trim=True,errBar = False,stats=True):


	"""
	"""
	
	fig = plt.figure(figsize = (5, 2.5))
	plt.subplots_adjust(left=.2, bottom=.15, wspace=.4)

	nRows = 1
	nCols = 2
	nPlot = 0
	
	lTitles = ["b) Experiment 2", "a) Experiment 1"]	
	
	for exp in ["004A", "004B"]:
		nPlot +=1 

		ax = plt.subplot(nRows, nCols, nPlot)
		plt.title(lTitles.pop())

		# Get dm:
		src = 'selected_dm_%s_WITH_drift_corr_onlyControl_True.csv' % exp
		dm = CsvReader(src).dataMatrix()
	
		# Determine the names of the dependent variables in the datamatrix
		if trim:
			dm = dm.selectByStdDev(["file"], \
				rtVar, verbose=False)
	
		colList = [orange[1], blue[1]]
		
		for hand in dm.unique("response_hand"):
			_dm = dm.select("response_hand == '%s'" % hand)
			
			lM = []		
			lErr = []
			
			for handle in dm.unique("handle_side"):
				__dm = _dm.select("handle_side == '%s'" % handle)
	
				cm = __dm.collapse(["file"], rtVar)
	
				M = cm["mean"].mean()
				SE = cm['mean'].std() / np.sqrt(len(cm))
				lM.append(M)
				lErr.append(SE)
	
			col = colList.pop()
	
			xData = range(len(lM))
			yData = lM

			if errBar:
				plt.errorbar(xData, yData, yerr=lErr, fmt='o-', marker = "o", \
					color = col, markerfacecolor='white', markeredgecolor=col, \
					markeredgewidth=1)
			else:
				plt.plot(yData, marker = "o", \
					color = col, markerfacecolor='white', markeredgecolor=col, \
					markeredgewidth=1)
			if exp == "004A":
				plt.legend(dm.unique("handle_side"), loc = 'best', frameon=False, \
					title="Handle Orientation")
			
			if exp == "004A":
				plt.ylim([700, 750])
			if exp == "004B":
				plt.ylim([600,650])

			plt.xlabel("Response Hand")
			spacing = 0.5
			xTicks = range(0,2)
			xLabels = dm.unique("response_hand")
			plt.xticks(xTicks, xLabels, rotation = .5)
			plt.xlim(min(xTicks)-spacing, max(xTicks)+spacing)
			plt.ylabel("Response time")

		if stats:
			print "Exp = ", exp
			print "rtVar = ", rtVar
			lmeAff(R, dm, rtVar,exp=exp)
		
		raw_input()



	plt.savefig(os.path.join(dst,"Affordances_both_exp.png"))
			
		

if __name__ == "__main__":

	R = RBridge()

	plotAff("rtFromStim")
	#for rtVar in ["RT", "rtFromStim"]:#for exp in ["004A", "004B"]:
	#	for exp in ["004A","004B"]:	
	#		lmeAff(R, exp, rtVar)
