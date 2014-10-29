#!/usr/bin/env python
#-*- coding:utf-8 -*-

from exparser.DataMatrix import DataMatrix
from exparser.RBridge import RBridge
import numpy as np

#N = 200
#
#a = np.zeros((2*N,),dtype=[('c', str), ('s', int), ('v', float), ('vr', float)])
#dm = DataMatrix(a, structured=True)
#dm['c'][:N] = 'A'
#dm['s'][:N] = range(N)
#dm['v'][:N] = np.random.rand(N) - .05
#dm['c'][N:] = 'B'
#dm['s'][N:] = range(N)
#dm['v'][N:] = np.random.rand(N) + .05
#dm['vr'] = dm['v']
#dm['vr'][:N] *= -1
#
#print dm
#R = RBridge()
#R.load(dm)
#lm = R.lmer('v ~ c + (1|s)')
#lm._print(sign=10)
#lm = R.lmer('vr ~ (1|s)')
#lm._print(sign=10)


## Import Python modules:
#import numpy as np
#import os
#import sys
from matplotlib import pyplot as plt
import scipy.stats

# Import own modules:
from exparser.PivotMatrix import PivotMatrix
from exparser.AnovaMatrix import AnovaMatrix
from exparser.CsvReader import CsvReader
import getDM
import onObject

src = 'selected_dm_004B_WITH_drift_corr_onlyControl_True.csv'
dm = CsvReader(src).dataMatrix()

sacc = "1"	
dvNorm = "endX1CorrNormToHandle"
dvRaw = "endX1CorrNorm"

dm = onObject.onObject(dm, sacc)
	
print "ANOVA"
am = AnovaMatrix(dm, ["handle_side"], dvRaw, "file")._print(ret=True)
print am

print 'One-sample test scipy'
cm = dm.collapse(["file"], dvNorm)
ref = 0

t, p = scipy.stats.ttest_1samp(cm['mean'], ref)				
print "t = ",t
print "p = ", p

# Paired-samples t-test:
print "paired samples t-test"
l = []
for handle in dm.unique("handle_side"):
	handle_dm = dm.select("handle_side == '%s'" % handle)
	cm = handle_dm.collapse(["file"], dvRaw)
	l.append(cm["mean"])
t, p = scipy.stats.ttest_rel(l[0], l[1])

print "t = ",t
print "p = ", p
