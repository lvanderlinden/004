# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 15:41:50 2014
@author: lotje

DESCRIPTION:
Investigate launch site slowest refixations
"""

from exparser.CsvReader import CsvReader
from exparser.TangoPalette import *
from matplotlib import pyplot as plt
import onObject

# Set font:
plt.rc("font", family="arial")
plt.rc("font", size=7)

def ovp(exp,corr=False, trim=True, bins=8):
	
	"""
	"""
	
	src = 'selected_dm_%s_WITH_drift_corr_onlyControl_True.csv' % exp
	dm = CsvReader(src).dataMatrix()

	lat1 = "saccLat1"
	lat2 = "saccLat2"
	prob = "saccCount"
	dur1 = "durationFix1"
	dur2 = "durationFix2"
	total = "gazeDur"
	rt = "rtFromStim"
	
	if corr:
		fix1 = "endX1CorrNormToHandle"
		fix2 = "endX2CorrNormToHandle"
	else:
		fix1 = "endX1NormToHandle"
		fix2 = "endX2NormToHandle"
		
	for var in [lat1, lat2, fix1, fix2, dur1, dur2, total, rt]:
		dm = dm.select("%s != ''" % var)
	
	# Trim the data
	if trim:
	
		dm = dm.selectByStdDev(["file"],lat2, 
			verbose=False)
		dm = dm.removeField("__dummyCond__")
		dm = dm.removeField("__stdOutlier__")
		dm = dm.selectByStdDev(["file"], fix2,
			verbose=False)
	
	dm = dm.addField('land2_perc', dtype=float)
	dm = dm.calcPerc(fix2, 'land2_perc', nBin=bins)
	cmLat1 = dm.collapse(['land2_perc'], lat1)	
	cmLat2 = dm.collapse(['land2_perc'], lat2)
	cmFix1 = dm.collapse(['land2_perc'], fix1)
	cmX = cmFix2 = dm.collapse(['land2_perc'], fix2)
	cmProb = dm.collapse(['land2_perc'], prob)
	cmDur1 = dm.collapse(['land2_perc'], dur1)
	cmDur2 = dm.collapse(['land2_perc'], dur2)
	cmTotal = dm.collapse(['land2_perc'], total)
	cmRt = dm.collapse(['land2_perc'], rt)
	fig = plt.figure(figsize = (3,10))
	plt.subplots_adjust(left=.2, bottom=.15, hspace = .2)
		

	lTitles = ["dur 1", "prob", "land 1", "rt", "total", "lat 1", "lat 2", "dur 2"]
	lTitles.reverse()
	nRows = len(lTitles)
	nCols = 1
	nPlot = 0

	for cmY in [cmDur1, cmProb, cmFix1, cmRt, cmTotal, \
		cmLat1, cmLat2, cmDur2]:
			
		nPlot +=1
		ax = plt.subplot(nRows, nCols, nPlot)
		#color = colList.pop()
		color = blue[1]
		plt.plot(cmX['mean'], cmY['mean'], marker = 'o', color=color, \
			markerfacecolor='white', markeredgecolor=color, \
			markeredgewidth=1)
		plt.ylabel(lTitles.pop())

		plt.axvline(0, linestyle = "--", color = gray[3])
			
		if nPlot == nRows:
			plt.xlabel("Second landing position")
		else:
			ax.xaxis.set_ticklabels([])

	plt.savefig("ovp2_%s_corr_%s.png" % (exp, corr))

if __name__ == "__main__":
	
	for exp in ["004B", "004A"]:
		ovp(exp, corr=False)

		if exp == "004A":
			ovp(exp, corr=True)
