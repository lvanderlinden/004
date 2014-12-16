from matplotlib import pyplot as plt
import getDm
import constants
from exparser.TangoPalette import *
import numpy as np
from exparser.PivotMatrix import PivotMatrix
from exparser.CsvReader import CsvReader
import scipy
import getDm

def plotFullModel(dm, sacc):
	
	"""
	"""


	fig = plt.figure(figsize = (15, 5))
	plt.suptitle("Sacc = %s" % sacc)
	ax1 = plt.subplot(141)
	lCols = ["blue", "red", "orange", "yellow", "green", "pink"]
	
	xVar = "sacc%s_ex" % sacc
	yVar = "sacc%s_ey" % sacc
	
	dm = dm.select("%s != ''" % xVar)
	dm = dm.select("%s != ''" % yVar)

	dm = dm.select("%s != -1000" % xVar)
	dm = dm.select("%s != -1000" % yVar)

	for a in dm.unique("realAngle"):
		_dm = dm.select("realAngle == %s" % a)
		col = lCols.pop()
		plt.scatter(_dm[xVar], _dm[yVar], color = col, marker = ".", label = a)
	plt.axvline(constants.xCen, color = gray[3], linestyle = '--')
	plt.axhline(constants.yCen, color = gray[3], linestyle = '--')

	ax2 = plt.subplot(142)
	pm = PivotMatrix(dm, ["stim_type", "realAngle"], ["file"], "xNorm1", colsWithin =True)
	pm.linePlot(fig = fig)
	pm.save("PM.csv")
	pm._print()
	plt.axhline(0, color = gray[3], linestyle = "--")

	ax3 = plt.subplot(143)
	plt.title("object")
	dmObj= dm.select("stim_type == 'object'")
	#slope, intercept, r_value, p_value, std_err  = scipy.stats.linregress(stimObj["ecc"], stimObj["xNorm1"])
	x = dmObj["ecc"]
	y = dmObj["xNorm%s" % sacc]
	fit = scipy.polyfit(x,y,1)
	fit_fn = scipy.poly1d(fit)
	plt.plot(x,y, 'yo', x, fit_fn(x), '--k')

	ax4 = plt.subplot(144)
	plt.title("non-object")
	dmNo= dm.select("stim_type == 'non-object'")
	#slope, intercept, r_value, p_value, std_err  = scipy.stats.linregress(stimObj["ecc"], stimObj["xNorm1"])
	x = dmNo["ecc"]
	y = dmNo["xNorm%s" % sacc]
	fit = scipy.polyfit(x,y,1)
	fit_fn = scipy.poly1d(fit)
	plt.plot(x,y, 'yo', x, fit_fn(x), '--k')

	plt.savefig("./plots/Full_model_004C_sacc%s.png" % sacc)
	plt.show()
	
if __name__ == "__main__":
	
	#dm = CsvReader("DM_004C.csv").dataMatrix()
	dm=getDm.getDm("004C", cacheId = "004C_final")
	
	for sacc in ["1", "2"]:
		#if sacc == "1":
		#	continue
		
		plotFullModel(dm, sacc)