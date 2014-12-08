from exparser.DataMatrix import DataMatrix
import numpy as np


f = ".cache/004C_lat_driftcorr_False.npy"
dm = DataMatrix(np.load(f))

for pp in dm.unique("file"):
	ppDm = dm.select("file == '%s'" % pp, verbose = False)
	_ppDm = ppDm.select("xNorm1 == -1000", verbose = False)
	print pp, float(len(_ppDm))/float(len(ppDm))