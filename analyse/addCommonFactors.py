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

def cogDict():
	
	"""
	In 004B, I didn't log the cog nor the x coordinates of the stimulus.
	Therefore, we need to read in this information from the csv file that
	was also used when running the experiment in OpenSesame.
	
	We read this csv file in as a dictionary containing the following key-value
	arrangement:
	key = (object, mask, flip), tuple
	value = xCog
	"""

	f = "cog_dict_004B.csv"
	f = open(f, "r")
	
	d = {}
	
	for line in f:
		for char in ['"', '(', ')', ' ', "'"]:
			line =  line.replace(char,'')
		
		stimName, mask, flip, xCog, yCog, dirCog = line.split(",")
		mask = mask.replace("mask_", '')
		d[stimName, mask, flip] = xCog
		
	return d


def addCog(dm):
	
	"""
	In 004B, I didn't log the cog nor the x coordinates of the stimulus.
	Therefore, we need to read in this information from the csv file that
	was also used when running the experiment in OpenSesame.
	"""

	# Get cog dictionary:
	d = cogDict()

	dm = dm.addField("xCog")

	for i in dm.range():
		
		stimName = dm["object"][i]
		mask = dm["mask_side"][i]
		flip = dm["handle_side"][i]
		
		xCog = d[stimName, mask, flip]
		dm["xCog"][i] = xCog
		
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