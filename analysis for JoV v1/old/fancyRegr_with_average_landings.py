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
import constants

# Set font:
plt.rc("font", family="arial")
plt.rc("font", size=7)

# Constant variables:
dst = "/home/lotje/Studies/004 - Single-object experiment - Handle-orientation effect/manuscript/Versions/5th draft/Figures JoV"
yLim = [-.30,.1]

def salMeans():
	
	"""
	"""
	
	src = 'selected_dm_004C_WITH_drift_corr_onlyControl_True.csv'
	dm = CsvReader(src).dataMatrix()
	
	l = []
	for sacc in ["1", "2"]:
		_dm = onObject.onObject(dm, sacc)
		l.append(_dm["endX%sNormToHandle" % sacc].mean())
	
	return l


def plotMeans(dm, exp, trim=True):
	
	"""
	Plots overall landing position per saccade per reference point.
	
	Arguments:
	exp
	
	Keyword arguments:
	trim
	"""
	
	if exp == "004A":
		lLabels = ["Relative to absolute center", "Relative to CoG"]
		lLabels.reverse()
	if exp == "004B":
		lLabels = ["Relative to CoG", "saliency simulation"]
		lLabels.reverse()
	
	if exp == "004A":	
		dvList = ["abs", "corr"]
	else:
		dvList = ["abs"]

	colList = [orange[1], blue[1]]

	for dvType in dvList:
		
		col = colList.pop()
	
		lMeans = []
		errMeans = []
	
		for sacc in ["1", "2"]:

			if dvType == "corr":
				dv = "endX%sCorrNormToHandle" % sacc
			else:
				dv = "endX%sNormToHandle" % sacc
		
			# Process the dm:
			dm = onObject.onObject(dm, sacc)
			
			if trim:
				
				dm = dm.removeField("__dummyCond__")
				dm = dm.removeField("__stdOutlier__")

				dm = dm.selectByStdDev(["file"], "saccLat%s" % sacc, \
					verbose=False)
				dm = dm.removeField("__dummyCond__")
				dm = dm.removeField("__stdOutlier__")
				dm = dm.selectByStdDev(["file"], dv, verbose=False)


			# Determine avg landing position:
			cm = dm.collapse(["file"], dv)
			m = cm["mean"].mean()
			se = cm['mean'].std() / np.sqrt(len(cm))
			ci = se * 1.95
			lMeans.append(m)
			errMeans.append(ci)
	
		# Plot landing positions of 2
		xData = range(len(lMeans))
		yData = lMeans
		yErr = errMeans
		
		plt.errorbar(xData, yData, label = lLabels.pop(), \
			yerr=yErr, fmt='o-',\
			marker = "o", color = col, \
			markerfacecolor='white', markeredgecolor=col, \
			markeredgewidth=1)
		
		if exp == "004B":
			lSal = salMeans()
			print lSal
			plt.plot(lSal, marker = "o", color = red[1], \
				markerfacecolor='white', markeredgecolor=red[1], \
				markeredgewidth=1, label = lLabels.pop())
	
	plt.legend(loc='best', frameon=False)

	

def lmeRegr(R, dm, sacc, corr=False, color=blue[1], bins=8, \
	fixedRange=False, trim=True, steps=5, nsim=10, stats=True):

	"""
	Creates a regression plot  with saccade latency on the X axis and
	horizontal gaze bias on the Y axis.

	Arguments:
	R		--	An RBridge object.
	dm		--	A DataMatrix.


	Keyword arguments:
	sacc			--	The saccade number. (default=1).
	corr			--	Indicates whether the CoG-corrected gaze bias should be used
					or the uncorrect. (default=False)
	color		--	The color for the plot. (default=blue[1])
	bins			--	The number of bins for the datapoints. (default=8)
	fixedRange	--	Indicates whether a fixed range should be used for the fit
					or whether we should use -1 to +2 SD. (default=False)
	trim			--	Trim data by SD. (default=True)
	steps		--	The number of steps for the regression analysis. Decrease
					to increase speed. (default=10)
	nsim			--	The number of MCMC simulations passed onto pvals.fnc().
					Decrease to increase speed. (default=10000)
	saveStats	-- Indicates whether statistical tests should be performed and
					saved.

	Returns:
	An (lmerDm, x0pos, x0neg) tuple. The lmerDm is the results of LME analysis.
	The x0pos and x0neg indicates the saccade latency at which the
	upper and lower bounds respectively cross the zero line on the Y axis. 
	This means that before and after this point there is a significant gaze 
	bias.
	"""

	# Determine the names of the dependent variables in the datamatrix
	if corr:
		dv = 'endX%dCorrNormToHandle' % sacc
	else:
		dv = 'endX%dNormToHandle' % sacc
	slDv = 'saccLat%d' % sacc

	# Pre-process the datamatrix
	dm = dm.addField('shiftedSaccLat', dtype=float)
	dm = dm.select('saccLat%d != ""' % sacc, verbose=False)
	if trim:
		dm = dm.selectByStdDev(["file"], slDv, verbose=False)
		dm = dm.removeField("__dummyCond__")
		dm = dm.removeField("__stdOutlier__")
		dm = dm.selectByStdDev(["file"], dv, verbose=False)

	# Determine the range of saccade-latency shifts.
	if fixedRange:
		if sacc == 1:
			shiftRange = (75, 250)
		elif sacc == 2:
			shiftRange = (250, 600)
	else:
		shiftRange = np.linspace(dm[slDv].mean() - 1.5*dm[slDv].std(), \
			dm[slDv].mean() + 2.5*dm[slDv].std(), steps)

	# First draw the regression line, including 95% CI
	xData = []
	yData = []
	eLo = []
	eUp = []
	for shift in shiftRange:
		#print shift
		dm['shiftedSaccLat'] = dm[slDv] - shift
		R.load(dm)
		#lmerDm = R.lmer('%s ~ shiftedSaccLat + (1|file) + (1|object)' \
		#	% dv, nsim=100)

		lmerDm = R.lmer('%s ~ shiftedSaccLat + (1|file) + (1|object)' \
			% dv, nsim=nsim)
		#print lmerDm
		intercept = lmerDm['est'][0]
		p = lmerDm['p'][0]
		ci95lo = lmerDm['ci95lo'][0]
		ci95up = lmerDm['ci95up'][0]
		#print intercept, p
		xData.append(shift)
		yData.append(intercept)
		eLo.append(ci95lo)
		eUp.append(ci95up)
	
	plt.plot(xData, yData, '--', color=color)
	plt.fill_between(xData, eLo, eUp, alpha=.3, color=color)

	# Now draw the actual data in binned form
	dm = dm.addField('saccLat_perc', dtype=float)
	dm = dm.calcPerc(slDv, 'saccLat_perc', nBin=bins)
	cmX = dm.collapse(['saccLat_perc'], slDv)
	cmY = dm.collapse(['saccLat_perc'], dv)
	
	plt.plot(cmX['mean'], cmY['mean'], marker = 'o', color=color, \
		markerfacecolor='white', markeredgecolor=color, markeredgewidth=1)
		
	if stats:	
		# Determine the first point at which the intercept is significantly negative
		# or positive.
		R.load(dm)
		lmerDm = R.lmer('%s ~ %s + (1|file) + (1|object)' % (dv, slDv), \
			nsim=nsim, printLmer=False)
		up = lmerDm['ci95up'][0]
		lo = lmerDm['ci95lo'][0]
		s = lmerDm['est'][1]
		x0pos = -up/s
		x0neg = -lo/s
		print 'sacc = %s, corr = %s' % (sacc, corr)
		print 'x0pos = %.2f' % x0pos
		print 'x0neg = %.2f' % x0neg
		print 'shiftRange = %s' % shiftRange
		print lmerDm
		print
	
		# Run a full LME
		lmerDm = R.lmer(\
			'%s ~ %s + response_hand + y_stim + gap + (1|file) + (1|object)'\
			% (dv, slDv), nsim=nsim)
		lmerDm._print(sign=5)
		lmerDm.save('lme.%s.%s.%s.csv' % (exp,sacc, corr))
		print

		return lmerDm, x0pos, x0neg
	
def plotRegr(exp):
	
	"""
	Plots data for one experiment.
	
	Arguments:
	exp		--- {"004A", "004B"}
	"""
	
	src = 'selected_dm_%s_WITH_drift_corr_onlyControl_True.csv' % exp
	dm = CsvReader(src).dataMatrix()
	
	R = RBridge()

	fig = plt.figure(figsize = (8,3))
	plt.subplots_adjust(left=.2, bottom=.15)
	
	# Plot hline:
	plt.axhline(0, color = "black", linestyle = "--")
	
	lmeRegr(R, dm, sacc=1, corr=False, color=blue[1])
	if exp == "004A":
		lmeRegr(R, dm, sacc=1, corr=True, color=orange[1])
	lmeRegr(R, dm, sacc=2, corr=False, color=blue[1])
	if exp == "004A":	
		lmeRegr(R, dm, sacc=2, corr=True, color=orange[1])

	if exp == "004B":
		lSal = salMeans()
		plt.axhline(lSal[0], color = red[1])
		plt.axhline(lSal[1], color = red[1])

	# Fake legend:
	if exp == "004A":
		lLabels = ["Relative to center", "Relative to CoG"]
		col2 = orange[1]
	if exp == "004B":
		lLabels = ["Relative to CoG", "Simulated landing positions"]
		col2 = red[1]

	line1= plt.Line2D((0,1),(0,0), marker = "o", color = blue[1], \
		markerfacecolor = "white", markeredgecolor = blue[1], \
		markeredgewidth = 1)

	line1= plt.Line2D((0,1),(0,0), marker = "o", color = col2, \
		markerfacecolor = "white", markeredgecolor = col2, \
		markeredgewidth = 1)

	plt.legend([line1, line2], lLabels,\
		frameon = False, loc='best')
			
	plt.xlabel("Saccade latency since stimulus onset")
	plt.xlim([80,660])
	plt.ylim(yLim)	
	plt.ylabel("Normalised landing position")

	plt.savefig(os.path.join(dst,"Data_analysis_%s.png" % exp))


if __name__ == "__main__":

	for exp in ["004A", "004B"]:
		plotRegr(exp)
		#plotRegr(exp)
