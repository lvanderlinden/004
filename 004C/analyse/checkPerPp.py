from exparser.DataMatrix import DataMatrix
import numpy as np


f = ".cache/004C_lat_driftcorr_False.npy"
dm = DataMatrix(np.load(f))

for pp in dm.unique("file"):
	print pp
	ppDm = dm.select("file == '%s'" % pp, verbose = False).select("xNorm1 != -1000")
	