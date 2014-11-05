"""
DESCRIPTION:
Apply some selection criteria
"""
from exparser.Cache import cachedDataMatrix, cachedArray

@cachedDataMatrix
def selectDm(dm):
	
	"""
	Apply some selection criteria.
	
	Returns filtered dm
	"""

	exp = dm["expId"][0]
	dm = dm.select("mask_side == 'control'")

	if exp == "004C":
		dm = dm.select("practice == 'no'")
	if exp != "004C":
		dm = dm.select("cond != 'practice'")
		dm = dm.select("rep != 'practice'")
	dm = dm.select("saccLat1 != ''")
	dm = dm.select("saccLat1 > 0")
	dm = dm.select("xNorm1 != ''")
	dm = dm.select("xNorm1 != -1000")
	
	## As in analyses for previous JoV V1:
	dm = dm.select("checkFixDotFailed == 'False'")
	dm = dm.select("checkObjectFailed == 'False'")

	if exp == "004A":
		dm = dm.select('durCheck1 < 1000')
		dm = dm.select('durCheck2 < 1000')
		dm = dm.select("accuracy == 1")
	
	if exp == "004C":
		dm = dm.select("file != '004C3'")
		dm = dm.select("correct == 1")
	return dm
