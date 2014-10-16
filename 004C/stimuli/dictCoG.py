"""
DESCRIPTION:
Create DM containing CoG per stimulus. 
"""

import sys
import cog
import os
import numpy as np
from exparser.CsvReader import CsvReader
from matplotlib import pyplot as plt
from scipy import ndimage, misc

fCoG = open("cog_per_stim.csv", "w")
fCoG.write(",".join(["name", "stim_type", "xCoG"])+"\n")

src = "final"


stimList = ["chisel", "chisel2", "mallet", "paintbrush", "screwdriver", \
	"wrench", "fork", "knife", "peeler", "sharpeningsteel", "spoon", \
		"spoon2", "washingbrush", "hammer"]

for stim in stimList:
	print stim
	for stimType in ["object", "non-object"]:
		#print stimType
		#print "%s_%s.jpg" % (stimType, stim)
		path = "final/%s_%s.jpg" % (stimType, stim)
		#print path
		#raw_input()
		_src = ndimage.imread(path)[:,:,:3]	
		src = np.empty(_src.shape, dtype=np.uint32)
		src[:] = _src

		x,y = cog.cog(src.copy())
		#print x
		#sys.exit()
		fCoG.write(",".join([stim, stimType, str(x)]) + "\n")

fCoG.close()

dm = CsvReader("cog_per_stim.csv").dataMatrix()
print dm
lCols = ["blue", "red"]

fig = plt.figure()
for stimType in dm.unique('stim_type'):
	_dm = dm.select("stim_type == '%s'" % stimType)
	cog = _dm["xCoG"]
	col = lCols.pop()
	plt.plot(cog, color = col, label = stimType)
plt.legend()
plt.show()