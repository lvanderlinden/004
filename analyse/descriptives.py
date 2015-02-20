"""
DESCRIPTION:
Get descriptives (e.g. mean eccentricity etc.)
"""

import parse
import getDm
import selectDm
import constants


from matplotlib import pyplot as plt


def descrEcc(dm):
	
	"""
	Descriptives eccentricity
	"""
	
	print "M ecc = ", dm["ecc"].mean()/constants.ratio
	print "SD ecc = ", dm["ecc"].std()/constants.ratio
	print "Min ecc = ", min(dm["ecc"])/constants.ratio
	print "Max ecc = ", max(dm["ecc"])/constants.ratio
	
def descrStimSize(dm):

	"""
	"""
	
	# TODO: bounding box sometimes too wide
	
	for var in ["wBoxScaled", "hBoxScaled"]:
		print "Descriptives ", var
		cm = dm.collapse(["stim_name", "stim_type"], var)
		
		for stimType in cm.unique("stim_type"):
			
			print "	stim type = ", stimType
			_cm = cm.select("stim_type == '%s'" % stimType, verbose = False)
			print "		M = ", _cm["mean"].mean()/constants.ratio
			print "		Min = ", min(_cm["mean"])/constants.ratio
			print "		Max = ", max(_cm["mean"])/constants.ratio

def descrCog(dm):
	
	"""
	Descriptives per stimulus type per object
	"""
	
	dm = dm.select("flip != 'left'", verbose = False)
	#var = "xCogNorm"
	var = "xCogScaledDegr"
	print "Descriptives ", var
	cm = dm.collapse(["stim_name", "stim_type"], var)
	cm.save("%s_per_object.csv" % var)
	for stimType in cm.unique("stim_type"):
		
		print "	stim type = ", stimType
		_cm = cm.select("stim_type == '%s'" % stimType, verbose = False)
		print "		M = ", _cm["mean"].mean()
		print "		Min = ", min(_cm["mean"])
		print "		Max = ", max(_cm["mean"])

def descrDurFb(dm):
	
	"""
	Descriptives duration feedback item (set to 0 in OS, but in practice
	it stays on screen while the next trial is prepared, i.e., for several
	100 ms)
	"""
	
	pass
	
if __name__ == "__main__":
	
	#dm = parse.parseAsc(exp = "004B", cacheId = "parsed")
	#dm = getDm.addCoord(dm,cacheId = "with_coord")
	#dm = getDm.addLat(dm, cacheId = "with_lat")
	#dm = selectDm.select(dm, cacheId = "selection")
	exp = "004C"
	dm = getDm.getDm(exp = exp, cacheId = "%s_final" % exp)

	descrCog(dm)
	sys.exit()
	descrStimSize(dm)
	descrEcc(dm)
	descrDurFb(dm)