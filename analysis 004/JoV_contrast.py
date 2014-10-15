"""
DESCRIPTION:
Plots contrast effect and tests for significance using LME.
"""

# Import Python modules:
import numpy as np
import os
import sys
from matplotlib import pyplot as plt
import scipy
import re
# Import own modules:
from exparser.RBridge import RBridge
from exparser.AnovaMatrix import AnovaMatrix
from exparser.CsvReader import CsvReader
import onObject

# Set font:
plt.rc("font", family="arial")
plt.rc("font", size=7)

# Constant variables:
dst = "/home/lotje/Studies/004 - Single-object experiment - Handle-orientation effect/manuscript/Versions/5th draft/Figures JoV"
critVal = 2.44
yTitle = "Normalised landing position"

def lmeContrast(R, dm, dv, saccVar = None, exp="exp?",nsim=10000):

	"""
	Creates a regression plot  with saccade latency on the X axis and
	horizontal gaze bias on the Y axis.

	Arguments:
	R		--	An RBridge object.
	dm


	Keyword arguments:
	nsim			--	The number of MCMC simulations passed onto pvals.fnc().
					Decrease to increase speed. (default=10000)

	Returns:
	"""
	
	
	R.load(dm)
	if saccVar == None:	
		lmerDm = R.lmer(\
			'%s ~ contrast_side + handle_side + y_stim + response_hand + (1|file) + (1|object)' % (dv),\
			nsim=nsim, printLmer=True)
	else:
		lmerDm = R.lmer(\
			'%s ~ %s + contrast_side + handle_side + y_stim + response_hand + (1|file) + (1|object)' % (dv, saccVar),\
			nsim=nsim, printLmer=True)
			
	lmerDm._print(sign=5)
	
	#lmerDm.save('lme_contrast_%s_%s.csv' % (exp, dv))
	print 'Done!'		

def plotContrast(exp = "004B", trim=True, inclSim=True,stats=True,norm=False):
	
	
	"""
	Plots landing positions as a function of contrats manipulation per saccade,
	for Exp 1 and Exp 2, relative to CoG.
	
	Keyword arguments:
	trim		--- (default=True)
	"""
	

	# Get dm:
	src = 'selected_dm_%s_WITH_drift_corr_onlyControl_False.csv' % exp
	dm = CsvReader(src).dataMatrix()

	colList = ["#f57900", "#3465a4"]
	lLegend = ["Saccade 1", "Saccade 2"]

	fig = plt.figure(figsize = (3,4))
	plt.subplots_adjust(left=.2, bottom=.15)
	yLim = [-.07, .12]
	

	for sacc in ["1", "2"]:
		dv = "endX%sNorm" % sacc
		saccVar = "saccLat%s" % sacc

		# Get dm:	
		# Only on-object:
		dm = onObject.onObject(dm, sacc,verbose=False)
		
		if trim:
			dm = dm.removeField("__dummyCond__")
			dm = dm.removeField("__stdOutlier__")
			dm = dm.selectByStdDev(keys = ["file"], \
			dv = dv,verbose=False)
			dm = dm.removeField("__dummyCond__")
			dm = dm.removeField("__stdOutlier__")
			dm = dm.selectByStdDev(keys = ["file"], dv = saccVar,\
				verbose=False)

		
		# Collect mean and error bar per saccade:
		lM = []
		lErr = []
		
		if norm:
			# Normalize across handle side:
			dm = dm.removeField("normDV")
			dm= dm.addField("normDV", dtype = float)
			dm= dm.withinize(dv, "normDV", \
					["handle_side"], whiten=False)
			dv = "normDV"

	
		for contrast in dm.unique("contrast_side"):
			contrast_dm = dm.select("contrast_side == '%s'" % contrast,\
				verbose = False)
			
			cm = contrast_dm.collapse(["file"], dv)

			M = cm["mean"].mean()
			SE = cm['mean'].std() / np.sqrt(len(cm))
			CI = SE * critVal
			lM.append(M)
			lErr.append(CI)
		if stats:
			# Run a full LME
			print "Exp = ", exp
			print "DV = ", dv
			print "trim = ", trim
			print "norm = ", norm
			print "saccVar = ", saccVar
			lmeContrast(R, dm, dv, saccVar, exp=exp)
			#raw_input()
				
			xData = range(len(lM))
			yData = lM
			yErr = lErr

		col = colList.pop()
		plt.errorbar(xData, yData, yerr=yErr, fmt='o-', marker = "o", \
			color = col, markerfacecolor='white', markeredgecolor=col, \
			markeredgewidth=1)
	plt.axhline(0, linestyle = "--")
	plt.ylim(yLim)
	plt.ylabel(yTitle)
	#ax.yaxis.set_ticklabels([])
	plt.legend(lLegend, frameon = False)
	plt.axhline(0, color = "black", linestyle = "--")
	plt.xlabel("High-contrast side")
	spacing = 0.5
	xTicks = range(0,3)
	xLabels = ["Left", "Control", "Right"]
	plt.xticks(xTicks, xLabels, rotation = .5)
	plt.xlim(min(xTicks)-spacing, max(xTicks)+spacing)
	plt.savefig(os.path.join(dst,"Contrast_Effect_%s_trim_%s_norm_%s.png") \
		% (exp, trim, norm))
	plt.show()



if __name__ == "__main__":
	

	R = RBridge()
	plotContrast(norm=True)
	plotContrast(nor=False)