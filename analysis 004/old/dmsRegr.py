#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: regressionAnalyses.py

# Import Python modules:
import sys

# Import own modules:
from exparser.EyelinkAscFolderReader import EyelinkAscFolderReader
from exparser.DataMatrix import DataMatrix
from exparser.PivotMatrix import PivotMatrix
from exparser.AnovaMatrix import AnovaMatrix
from exparser import Constants

# Import own modules:
import getDM
import onObject

if __name__ == "__main__":
	

	for exp in ["004B", "004A"]:
		
		dm = getDM.getDM(exp = exp)
		
		for sacc in ["1", "2", "3"]:
						
			# Only first sacc for the moment:
			if sacc != "1":
				continue

			# Determine variable names:			
			dvList = ["endX%sNormToHandle"% sacc]
			if exp == "004A":
				dvList.append("endX%sCorrNormToHandle" % sacc)
			
			dv2 = "saccLat%s" % sacc
			
			for dv1 in dvList:
				
				# Only trials on which the variable has a value:
				sacc_dm = onObject.onObject(dm, sacc)
				
				# Trim on both variables:
				dm_trim1 = sacc_dm.selectByStdDev(["file"], dv1)
				dm_trim1 = dm_trim1.removeField("__dummyCond__")
				dm_trim1 = dm_trim1.removeField("__stdOutlier__")
				dm_trim2 = dm_trim1.selectByStdDev(["file"], dv2)
				
				# Save dm:
				dm_trim2.save("dm_exp%s_sacc%s_%s" % (exp, sacc, dv1))