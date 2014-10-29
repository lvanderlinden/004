# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 10:45:41 2013

@author: lotje
"""

import sys
import os
from matplotlib import pyplot as plt
from scipy import stats
import pylab

# Import own modules:
from exparser.EyelinkAscFolderReader import EyelinkAscFolderReader
from exparser.DataMatrix import DataMatrix
from exparser.PivotMatrix import PivotMatrix
from exparser.AnovaMatrix import AnovaMatrix
from exparser import Constants
import getDM
import onObject

exp = "004B"

dm = getDM.getDM(exp)

print dm["xCoG"].mean()
sys.exit()

# Only second saccades:
dm_on = onObject.onObject(dm, "2")

var1 = "endX1NormToHandle"
var2 = "endX2NormToHandle"
x = dm_on[var1]
y = dm_on[var2]

pylab.plot(x, y, 'x')
slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)

pylab.plot(x, intercept + slope * x, 'r-')
plt.xlabel(var1)
plt.ylabel(var2)
plt.axhline(0)
plt.axvline(0)
pylab.show()