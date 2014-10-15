# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 10:52:37 2014

@author: lotje

DESCRIPTION:
Check saccade latencies
"""

#from exparser.DataMatrix import DataMatrix
import getDM
import constants

print constants.yCen
print constants.minSaccSize
print constants.yCen + constants.minSaccSize

dm = getDM.getDM("004A", noFiltering = True, driftCorr=False)
dm = dm.select("file == 'SS04.asc'")

#	_dm = dm.select("overall_rep == '1'").select("object == 'peeler'").\
#		select("handle_side == 'left'").select("mask_side == 'control'")

#	_dm = dm.select("overall_rep == '1'").select("object == 'ruler'").\
#		select("handle_side == 'right'").select("mask_side == 'left'")

_dm = dm.select("overall_rep == '1'").select("object == 'screwdriver'")#.\
	#select("handle_side == 'right'").select("mask_side == 'left'")


print len(_dm)
print "visual field = ", _dm["visual_field"]
print "start sacc coordinations = ", _dm["startXRaw1"], _dm["startYRaw1"]
print "end sacc coordinates = ", _dm["endXRaw1"], _dm["endYRaw1"]
print "fix coordinates = ", _dm["xFix1"] + constants.xCen, _dm["yFix1"] + constants.yCen

print "sacc lat = ", _dm["saccLat1"]
print _dm["saccLat2"]
print _dm["saccLat3"]
print _dm["saccLat4"]
