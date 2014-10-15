# Import Python modules:
import numpy as np
import os
import sys
from matplotlib import pyplot as plt
import scipy

# Import own modules:
from exparser.DataMatrix import DataMatrix
from exparser.PivotMatrix import PivotMatrix
from exparser.AnovaMatrix import AnovaMatrix
import getDM

if __name__ == "__main__":
	
	for exp in ["004A", "004B"]:
		
		# Get dm:
		dm = getDM.getDM(exp = exp, driftCorr = True)

		x = dm['endX1CorrNorm']
		y = dm['endY1CorrNorm']
		
		fit = scipy.polyfit(x,y,1)
		fit_fn = scipy.poly1d(fit)
		
		slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(x,y)
		stats = "slope = %.2f, intercept = %.2f, R = %.2f, p = %.3f, SE = %.2f" \
			% (slope, intercept, r_value, p_value, std_err)
		print stats
		fig = plt.figure()
		name = "Correlation between x and y trims"
			
		plt.plot(x,y, 'yo', x, fit_fn(x), '--k')
		plt.show()