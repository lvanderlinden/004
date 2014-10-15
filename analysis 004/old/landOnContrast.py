#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: landOnContrast.py

"""
Landing positions as a function of object orientation (across and
per 'object group').

NOTE: be careful with using --shortcut, because
for the contrast analyses the contrast manipulations
should not be excluded.

TODO: make a ToContrast variable, such that we have more observations
per cell and can do the on-object filter on the y axis as well?
The disadvantage is that we can't use the no-contrast-trials in this case
#(because 'ToContrast' should be a difference score between two bins).

For now, landing positions are split per contrast condition. As a consequence,
Positive values indicate landing position to the right,
negative values indicate landing pos to the left
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
from exparser import Constants
import getDM
import onObject

def contrastSide(trim = True):
	
	"""
	Landing position as a function of contrast.
	
	Keyword arguments:
	
	"""
	
	colList = ["#ef2929","#73d216","#f57900","#3465a4"]
	
	lLegend = ["Exp. 1 (relative to center)", "Exp. 1 (relative to CoG)", \
		"Experiment 2 (relative to CoG)", "Saliency-model simulation"]
	
	yLim = [-.3, .3]
	yTitle = "normalised landing position"
	
	fig = plt.figure()
	title = "Effect of contrast"
	plt.suptitle(title)
	plt.subplots_adjust(wspace = 0)

	
	for sacc in ["1", "2"]:#, "3"]:
		copyColList = colList[:]
		plt.subplot(1,2, int(sacc))
		plt.title("sacc = %s"% (sacc))

		#linestyles = ['o-', ',--', 'x:' #TODO
		for exp in ["004A", "004B", "004C"]:
			dm = getDM.getDM(exp, onlyControl = False)

			# Only on-object:
			on_dm = onObject.onObject(dm, sacc)
			
			if exp == "004A":
			
				dvList = ["endX%sNorm" % sacc, "endX%sCorrNorm" % sacc]
			else:
				dvList = ["endX%sNorm" % sacc]
				
						
			for dv in dvList:

				#If wanted, trim the data
				if trim:
					trim_dm = on_dm.selectByStdDev(keys = ["contrast_side", "file"], dv = dv)
				else:
					trim_dm = on_dm

				# Get pivot matrix:
				pm = PivotMatrix(trim_dm, ["contrast_side"], ["file"], dv=dv, colsWithin=True)

				col = copyColList.pop()
				#Constants.plotLineSymbols = [linestyles.pop()]
				pm.plot(fig = fig, nLvl1 = 1, colors = [col])
				
				if exp != "004C":
					am = AnovaMatrix(trim_dm, ["contrast_side"], dv, subject = "file")
					print exp, dv				
					print am
					#raw_input()
				
		plt.ylim(yLim)
		if sacc == "1":
			plt.ylabel(yTitle)
		if sacc == "2":
			plt.legend(lLegend)
			plt.yticks([])
		plt.axhline(0, color = "#888a85", linewidth = 2)
		plt.xlabel("Contrast manipulation")
	
	for ext in [".png", ".svg"]:
		plt.savefig("Figure_S1%s" % ext)


if __name__ == "__main__":
	
	contrastSide()
	
