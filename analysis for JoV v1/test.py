#!/usr/bin/env python
#-*- coding:utf-8 -*-

""" 
DESCRIPTION:
Plots landing position as a function of sacc latency (and other predictors, if
wanted), using LMM.
"""


from exparser.CsvReader import CsvReader
from exparser.RBridge import RBridge

src = "/home/lotje/Documents/PhD Marseille/Studies/004 - Single-object experiment - Handle-orientation effect/analysis 004/selected_dm_004B_WITH_drift_corr_onlyControl_True.csv"
dm = CsvReader(src).dataMatrix()
dm = dm.select("endX1NormToHandle == ''")
 dvRaw = "endX1Norm"
dvNorm = "endX1NormToHandle"
nsim = 10

R = RBridge()
R.load(dm)
print "Condition in DV"
# Run a full LME
lmerDm = R.lmer(\
	'%s ~ (1|file) + (1|object)'\
	% (dvNorm), nsim=nsim, printLmer=True)
lmerDm._print(sign=5)
lmerDm.save('lme_condition_in_dv.csv')

print "Condition as factor"
lmerDm = R.lmer(\
	'%s ~ handle_side + (1|file) + (1|object)'\
	% (dvRaw), nsim=nsim, printLmer=True)
lmerDm._print(sign=5)
lmerDm.save('lme_condition_as_factor.csv')
