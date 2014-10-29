#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: affordances.py

"""
Affordance effects in RTs:

# TODO:
time course??
"""

# Import Python modules:
import numpy as np
import os
import sys
from matplotlib import pyplot as plt

# Import own modules:
from exparser.DataMatrix import DataMatrix
from exparser.PivotMatrix import PivotMatrix
from exparser.AnovaMatrix import AnovaMatrix
import getDM
import onObject

def affPerSacc(trim = True, exclY = False, dv = "RT", \
	colList = ["#73d216", "#f57900"]):
	
	"""
	Affordance effect as t-test between levels of the factor 
	compatibility, per saccade.
	
	Keyword arguments:
	"""

	fig = plt.figure()
	title = "Affordance effect per sacc - dv = %s - exclY = %s" % (dv, exclY)
	plt.suptitle(title)
	plotNr = 1
	
	for exp in ["004A", "004B"]:
		copyColList = colList[:]
		plt.subplot(1,2,plotNr)
		plt.title("Exp = %s" % exp)
		
		dm = getDM.getDM(exp)
	
		for sacc in ["1", "2"]:
			
			# Only on-object saccades:
			_dm = onObject.onObject(dm, sacc, exclY = exclY, verbose = False)
			# Trim:
			if trim:
				trimmed_dm = _dm.selectByStdDev(keys =["comp", "file"], dv = dv)
			else:
				trimmed_dm = _dm
		
			pm = PivotMatrix(trimmed_dm, ["comp"], ["file"], dv = dv, colsWithin = True)
			
			am = AnovaMatrix(trimmed_dm, ["comp"], dv = dv, \
				subject = "file")._print(ret=True)
			print am
			
			col = copyColList.pop()
			pm.plot(nLvl1=1, fig = fig, colors = [col])
		plt.legend(["data sacc 1", "data sacc 2"])
		plotNr +=1
			
	plt.savefig("%s.png"%title)
	plt.savefig("%s.svg"%title)
	
def affCross(trim = True, exclY = False, dv = "RT"):
	
	"""
	Affordance effect as cross-over interaction between handle
	and response hand ACROSS saccades
	
	NOTE: on-object is difficult here, because we're not
	looking across saccades.
	"""

	fig = plt.figure()
	title = "Affordance effect per Exp - exclY = %s" % exclY
	plt.suptitle(title)
	plotNr = 1
	
	for exp in ["004A", "004B"]:
		
		if exp != "004B":
			continue
		
		
		plt.subplot(1,2,plotNr)
		plt.title("Exp = %s" % exp)
		
		dm = getDM.getDM(exp)
		
		dm = onObject.onObject(dm, "1", exclY = exclY)

		if trim:
			trimmed_dm = dm.selectByStdDev(keys = \
				["handle_side", "response_hand", "file"], dv = dv)
		else:
			trimmed_dm = dm

		am = AnovaMatrix(trimmed_dm, ["handle_side", "response_hand"], dv = dv, \
			subject = "file")._print(ret=True)
		print am
#		raw_input()
		
		# Get descriptive statistics:
		pm = PivotMatrix(trimmed_dm, ["comp"], ["file"], colsWithin = False, \
			dv = dv, err = 'se')
		print pm
		
		
		raw_input()
		pm = PivotMatrix(trimmed_dm, ["handle_side", "response_hand"], \
			["file"], dv = dv, colsWithin = True)
		pm.linePlot(fig = fig)
		
		plotNr +=1
		
	plt.savefig("%s.png"%title)
	
def deltaPlot(trim = True, exclY = False, \
		cousineau = True, nBin = 5, factor = "comp",\
		levelList = ["compatible", "incompatible"],\
		colList = ["#73d216", "#f57900"]):
	
	"""
	Effect size (comp-incomp) over time.
	
	Keyword arguments:
	trim
	exclY
	dv
	cousineau		--- Boolean indicating whether or not 
						to withinize data.
	"""
	
	fig = plt.figure()
	title = "Affordance effect over time - exclY = %s cousineau = %s" % \
		(exclY, cousineau)
	plt.suptitle(title)
	
	for exp in ["004A", "004B"]:
		
		dv = "RT"

		dm = getDM.getDM(exp)
		dm = onObject.onObject(dm, "1", exclY = exclY)

		if trim:
			trimmed_dm = dm.selectByStdDev(keys =[factor, "file"], dv = dv)
		else:
			trimmed_dm = dm
		
		# If wanted, normalize according to Cousineau:
		if cousineau:	
			new_dm = trimmed_dm.addField("cousineau_%s"%dv, dtype = None)
			new_dm = new_dm.withinize(dv, "cousineau_%s"%dv, "file", \
				whiten=False)
			dv = "cousineau_%s"%dv
		
		else:
			new_dm = trimmed_dm
		
		# Make bins
		varToBin = dv
		binID = '%sBin'%varToBin
		binKeys = ["file", factor] # Bin by subject and condition
			
		new_dm = new_dm.addField(binID)
		new_dm = new_dm.calcPerc(varToBin, binID, keys=binKeys, nBin=nBin)
		
		# Empty lists to collect bin means:
		lY = []
		lX = []
		
		# Walk through all bins
		for _bin in new_dm.unique(binID):  
			# Filter out all but one bin
			_dm = new_dm.select('%s == %f' % (binID, _bin))
			
			m1 = _dm.select('%s == "%s"'%(factor, levelList[0]),\
				verbose=False)[dv].mean()
			m2 = _dm.select('%s == "%s"'%(factor, levelList[1]),\
				verbose=False)[dv].mean()
			
			y = m2-m1
			x = _dm[varToBin].mean()
			
			lY.append(y)
			lX.append(x)
		col = colList.pop()
		plt.plot(lX, lY, color = col, linewidth = 2, marker = 'o')
	
	plt.legend(["Exp1", "Exp2"])
	plt.xlabel(varToBin)
	plt.ylabel("effect size")
	plt.axhline(0, color = "#888a85", linestyle = "--", linewidth = 2)
	plt.savefig("%s.png"%title)

if __name__ == "__main__":
	
	#deltaPlot(nBin = 10)
	#affPerSacc()
	affCross()
	plt.show()