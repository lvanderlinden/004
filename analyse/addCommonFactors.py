"""
DESCRIPTION:
Makes sure dm's for all experiments contain the factors that we need for
calculating the dv.
"""


import sys
import os
import numpy as np
from exparser.Cache import cachedDataMatrix, cachedArray
from exparser.CsvReader import CsvReader
import parse
import addCoord

def addAngle(dm):
	
	"""
	Add the factor realAngle
	"""
	
	dm = dm.addField("realAngle")
	
	dm["realAngle"] = 0
	iLower = dm.where("visual_field == 'lower'")
	dm["realAngle"][iLower] = 180

	return dm

def addCog(dm):
	
	"""
	Use NEW CoG calculation.
	"""

	# Get cog dictionary:
	f = "compare cogs/cog_per_stim_004C.csv"
	cogDm = CsvReader(f).dataMatrix()

	dm = dm.addField("xCog", default = -1000)
	
	for i in dm.range():
		
		stimName = dm["object"][i]
		flip = dm["handle_side"][i]
		symm = dm["symm"][i]
		
		if symm == "symm":
			continue
		
		xCogUnrot = cogDm.select("name == '%s'" % stimName, verbose = False)["xCog"][0]
		
		if flip == "left":
			xCog = xCogUnrot * -1
		elif flip == "right":
			xCog = xCogUnrot
		
		dm["xCog"][i] = xCog
		
		#print "object = ", stimName
		#print "symm = ", symm
		#print "flip = ", flip
		#print "cog = ", xCog
		
	return dm


@cachedDataMatrix
def addCommonFactors(dm):
	
	"""
	Add properties
	
	Arguments:
	dm		--- A datamatrix instance.
	"""
	
	if dm["expId"][0] != "004C" and dm["expId"][0] != "sim":
		dm = addAngle(dm)
		
		# Rename some variables that had different names in 004A/004B vs 004C:
		
		dm = addCog(dm)
		dm = dm.addField("xStim")
		dm = dm.addField("yStim")
		dm = dm.addField("flip", dtype = str)
		dm = dm.addField("stim_name", dtype = str)
		dm = dm.addField("stim_type", dtype = str, default = "object")
		
		dm["yStim"] = dm["y_stim"]
		dm["flip"] = dm["handle_side"]
		dm["stim_name"] = dm["object"]

	if dm["expId"][0] == "004B":
		dm["xStim"] = 0 - dm["xCog"]

	if dm["expId"][0] == "004A":
		dm["xStim"] = 0
	
	if dm["expId"][0] == "004C":
		
		# Set mask side to control:
		dm = dm.addField("mask_side", dtype = str, default = 'control')
		
	# Indicating whether or not the angle deviates from the vertical meridian.
	if dm["expId"][0] == "004C":
	
		dm = dm.addField("devAngle", dtype = str, default = "yes")
		dm["devAngle"][dm.where("realAngle == 0")] = "no"
		dm["devAngle"][dm.where("realAngle == 180")] = "no"

	
	else:
		dm = dm.addField("devAngle", dtype = str, default = "no")
	
	return dm
	
if __name__ == "__main__":
	
	for exp in ["004B", "004C"]:
		dm = parse.parseAsc(exp = exp, cacheId = "%s_parsed" % exp)
		dm.save("test_%s.csv" % exp)
		dm = addCommonFactors(dm, cacheId = "%s_common_factors" % exp)
		dm = addCoord.addCoord(dm)