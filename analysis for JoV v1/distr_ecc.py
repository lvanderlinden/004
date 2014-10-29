 
f = "selected_dm_004A_WITH_drift_corr_onlyControl_True.csv"

from exparser.CsvReader import CsvReader
from matplotlib import pyplot as plt
import numpy as np
dm = CsvReader(f).dataMatrix()
print dm.columns()
y_ecc = abs(dm["y_stim"])/33.

print np.mean(y_ecc)
print np.std(y_ecc)
plt.hist(y_ecc, bins = 10)
plt.show()