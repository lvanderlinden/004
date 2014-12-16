#!/usr/bin/env python
# Filename: simDm.py

"""
DESCRIPTION:
Creates dm that is comparable to the 'real' dm's used for
the analyses of experiment 1 and 2.
"""

import sys
from exparser.CsvReader import CsvReader
from matplotlib import pyplot as plt
from exparser.Cache import cachedDataMatrix
from exparser.DataMatrix import DataMatrix
import addCoord
import addLat
import selectDm
import numpy as np
import addCommonFactors

# Constants:

xc = 1024/2
yc = 768/2

ythr = 100

@cachedDataMatrix
def dmSim():

	"""
	"""
	
	dm = CsvReader('./simulation/data.csv').dataMatrix()

	# X coordinates, where positive values indicate a deviation towards the handle
	dm = dm.addField('sacc1_ex', dtype=float)
	dm = dm.addField('sacc2_ex', dtype=float)
	dm = dm.addField('sacc3_ex', dtype=float)

	dm = dm.addField('sacc1_ey', dtype=float)
	dm = dm.addField('sacc2_ey', dtype=float)
	dm = dm.addField('sacc3_ey', dtype=float)
	
	dm = dm.addField("trialId", dtype = str)


	# Timestamps for each fixation
	dm = dm.addField('saccLat1', dtype=float)
	dm = dm.addField('saccLat2', dtype=float)
	dm = dm.addField('saccLat3', dtype=float)

	for i in dm.range():
		
		trial = dm[i]
		trialNr = dm['count_trial_sequence'][i]
		dm["trialId"][i] = trialNr
		handleSide = trial['flip'][0]
		print 'Trial %d (%s)' % (trialNr, handleSide)
		sim = CsvReader('simulation/simulation/csv/%.4d.csv' % trialNr).dataMatrix()	
		
		fixNr = 1	
		for fix in sim:
			t = fix['t'][0]

			dx = fix['x'][0]
			dy = fix['y'][0]
			dm["sacc%s_ey" % fixNr][i] = dy
			dm['sacc%d_ex' % fixNr][i] = dx
			dm['saccLat%d' % fixNr][i] = t
			fixNr += 1
			if fixNr > 3:
				break
	dm.save('dm_simulation.csv')
	
	dm = dm.addField("expId", dtype = str, default = "sim")
	dm = dm.addField("symm", dtype = str, default = "asymm")
	dm = dm.addField("saccCount", default = 3)
	dm = dm.addField("mask_side", dtype = str, default = "control")
	dm = dm.addField("cond", dtype = str, default = "not_practice")
	dm = dm.addField("rep", dtype = str, default = "not_practice")
	dm = dm.addField("checkFixDotFailed", dtype = str, default = "False")
	dm = dm.addField("checkObjectFailed", dtype = str, default = "False")
	dm = dm.addField("file", dtype = str, default = "sim")
	return dm


def simAvg():
	
	"""
	Creates
	"""
	
	dm = dm.select("gap == 'zero'")
	d = {}
	
	for stimType in dm.unique("stim_type"):
		stimDm = dm.select("stim_type == '%s'" % stimType)
		for sacc in [1,2]:
			mDev = gapDm['xNorm%s' % sacc].mean()
			d[stimType, sacc]= mDev
	
	return d

if __name__ == "__main__":
	
	dm = dmSim(cacheId = "dm_sim_raw")
	dm = addCommonFactors.addCommonFactors(dm, \
		cacheId = "dm_sim_common_factors")
	dm = addCoord.addCoord(dm, cacheId = "dm_sim_coord")
	#dm = addLat.addLat(dm, cacheId = "dm_sim_lat_driftcorr")
	dm = selectDm.selectDm(dm, cacheId = "dm_sim_select_driftcorr")
	
	f = ".cache/dm_sim_select_driftcorr.npy"
	dm = DataMatrix(np.load(f))
	
	nPlot = 0

	plt.show()
	sys.exit()
	
