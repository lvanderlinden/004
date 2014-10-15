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

def refixLaunch(exp,corr=False, trim=True, bins=8):
	
	"""
	"""
	
	src = 'selected_dm_%s_WITH_drift_corr_onlyControl_True.csv' % exp
	dm = CsvReader(src).dataMatrix()
	
	lat1 = "saccLat1"
	lat2 = "saccLat2"
	if corr:
		fix1 = "endX1CorrNormToHandle"
		fix2 = "endX2CorrNormToHandle"
	else:
		fix1 = "endX1NormToHandle"
		fix2 = "endX2NormToHandle"
		
	for var in [lat1, lat2, fix1, fix2]:
		dm = dm.select("%s != ''" % var)
	
	# Trim the data
	if trim:
	
		dm = dm.selectByStdDev(["file"],lat2, 
			verbose=False)
		dm = dm.removeField("__dummyCond__")
		dm = dm.removeField("__stdOutlier__")
		dm = dm.selectByStdDev(["file"], fix2,
			verbose=False)
	
	dm = dm.addField('saccLat2_perc', dtype=float)
	dm = dm.calcPerc(lat2, 'saccLat2_perc', nBin=bins)
	cmLat1 = dm.collapse(['saccLat2_perc'], lat1)	
	cmX = cmLat2 = dm.collapse(['saccLat2_perc'], lat2)
	cmFix1 = dm.collapse(['saccLat2_perc'], fix1)
	cmFix2 = dm.collapse(['saccLat2_perc'], fix2)
	
	fig = plt.figure(figsize = (3,6))
	plt.subplots_adjust(left=.2, bottom=.15)
		
	colList = [orange[1], blue[1]]
	nRows = 3
	nCols = 1
	nPlot = 0
	lTitles = ["Landing pos 2", "Landing pos 1"]
	lTitles.reverse()
	for cmY in [cmFix2, cmFix1]:#, cmLat1]:
		#nPlot +=1
		#plt.subplot(nRows, nCols, nPlot)
		color = colList.pop()
		plt.plot(cmX['mean'], cmY['mean'], marker = 'o', color=color, \
			markerfacecolor='white', markeredgecolor=color, \
			markeredgewidth=1)
		plt.xlabel("Sacc lat 2")

	plt.legend(lTitles, frameon=False, loc='best')
	plt.axhline(0, linestyle = "--", color = gray[3])
	
	plt.savefig("Launch_site_refixations_%s_corr_%s.png" % (exp, corr))

if __name__ == "__main__":
	
	for exp in ["004B", "004A"]:
		refixLaunch(exp, corr=False)

		if exp == "004A":
			refixLaunch(exp, corr=True)
