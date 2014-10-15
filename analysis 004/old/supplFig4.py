"""
Supplementary material Figure 3
	- The statistical tests (one-sample t-tests) are performed on pp's
		condition means. This does not take WS variance into account,
		and therefore I did NOT use PivotMatrix and WS error bars,
		but the means and error terms as derived from the collapsed
		dm's.
"""

# Import Python modules:
import numpy as np
import os
import sys
from matplotlib import pyplot as plt
import scipy

# Import own modules:
from exparser.DataMatrix import DataMatrix
from exparser.PivotMatrix import PivotMatrix
from exparser.AnovaMatrix import AnovaMatrix
import getDM
import onObject

dst = "/home/lotje/Documents/PhD Marseille/Studies/004 - Single-object experiment - Handle-orientation effect/manuscript/sources"

critVal = 2.44
plt.rc("font", family="arial")
plt.rc("font", size=7)

colList = ["#f57900","#3465a4", "red"]
	
lLegend = ["Relative to CoG", "Saliency simulation"]
	
yLim = [-.3, .3]
yTitle = "Normalised landing position"

fig = plt.figure(figsize = (6,3))
plt.subplots_adjust(wspace = 0)
letList = ["c", "b","a"]
for sacc in ["1", "2", "3"]:#, "3"]:
	copyColList = colList[:]
	ax = plt.subplot(1,3, int(sacc))
	
	
	plt.title("%s) Saccade %s" % (letList.pop(), sacc))

	for exp in ["004A", "004B", "004C"]:
		dm = getDM.getDM(exp, onlyControl = False)

		# Only on-object:
		on_dm = onObject.onObject(dm, sacc)
		
		dv = "endX%sNorm" % sacc
			
		trim_dm = on_dm.selectByStdDev(keys = ["contrast_side", "file"], dv = dv)

		if exp != "004C":
			am = AnovaMatrix(trim_dm, ["contrast_side"], dv, subject = "file")
			print exp, dv				
			print am
	
		lM = []
		lErr = []
	
		for contrast in trim_dm.unique("contrast_side"):
			

			
			print contrast	
			
			contrast_dm = trim_dm.select("contrast_side == '%s'" % contrast)
			
			cm = contrast_dm.collapse(["file"], dv)
			cm._print(sign=5)
			
			print "sacc = %s, nr observations = %s" % (sacc, cm["count"].mean())
			
			
			M = cm["mean"].mean()
			SE = cm['mean'].std() / np.sqrt(len(cm))
			CI = SE * critVal
			lM.append(M)
			lErr.append(CI)
			
			ref = 0
			t, p = scipy.stats.ttest_1samp(cm['mean'], ref)				
			p_corr = min(1, float(p * 3.))
			print 'T test scipy'
			print dv, contrast
			print "M = %.3f, SE = %.3f, t(16) = %.2f, p = %.4f" % \
				(M, SE, t, p_corr)
			#raw_input()
		xData = range(len(lM))
		yData = lM
		yErr = lErr

		col = copyColList.pop()
		plt.errorbar(xData, yData, yerr=yErr, fmt='o-',\
		linewidth = 1.5, marker = "o", color = col, linestyle = \
		"-", markerfacecolor='white', markeredgecolor=col, \
		markeredgewidth=2)
	
	plt.ylim(yLim)
	if sacc == "1":
		plt.ylabel(yTitle)
	else:
		ax.yaxis.set_ticklabels([])

	if sacc == "2":
		plt.legend(lLegend, frameon = False)

	plt.axhline(0, color = "#888a85", linewidth = 1.5, linestyle = "--")
	if sacc == "2":	
		plt.xlabel("High-contrast side")
	spacing = 0.5
	xTicks = range(0,3)
	xLabels = ["Left", "Control", "Right"]
	plt.xticks(xTicks, xLabels, rotation = .5)
	plt.xlim(min(xTicks)-spacing, max(xTicks)+spacing)


for ext in [".png", ".svg"]:
	plt.savefig("Figure_S4%s" % ext)
plt.savefig(os.path.join(dst, "Figure_S4.png"))
plt.show() 



