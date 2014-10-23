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


	dm = dm.select("practice == 'no'")
	dm = dm.select("saccLat1 != ''")
	dm = dm.select("saccLat1 > 0")
	dm = dm.select("xNorm1 != ''")
	dm = dm.select("xNorm1 != -1000")
	
	return dm
