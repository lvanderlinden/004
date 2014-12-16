import getDm
from exparser.Cache import cachedDataMatrix

dm = getDm.getDm(exp = "004A", cacheId = "004A_final")

for i in dm.columns():
	
	if not "cog" in i and not "CoG" in i and not "Cog" in i:
		if not i in ["object", "flip"]:
			if not "wBox" in i:
				if not i in ["xNorm1", "xNormOnCenter1", "xNormCorr1"]:
					dm = dm.removeField(i)
			
dm.save("test_cog.csv")