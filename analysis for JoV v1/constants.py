#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: constants.py

"""
DESCRIPTION:
Constant variables in studies 004A and 004B
"""

# Minimum displacement before calling something a saccade.
# Example:
# if sacc != None and sacc['size'] > constants.minSaccSize:
# 	self.saccOnset = sacc['sTime']

# Minimum vertical eccentricity = 170 px
# Max = 238

# Something is a to-object saccade if the size of the saccade is more 
# than half of the minimum eccentricity:

# Scale factor used in OpenSesame to display objects
# 3 times smaller than the original bitmaps: 
rescale = 3.

minSaccSize = 170/2
#maxFixDur = 20 # ms

CoGCorrTooLarge = 0 # in px

xCen = 512.
yCen = 384.

screenW = xCen * 2
screenH = yCen * 2

ratioPxDegr = 33
print minSaccSize/ratioPxDegr


# Dummy variable to give all during-parsing-determined variables a starting
# value.
parseDummyVar = -1000

# Shape of the original bitmap. The calculated CoG has to be divided by the
# ORIGINAL width.
# Luckily, all objects had the same size:
wBitmap = 720. # px
hBitmap = 540. # px

lAsymm = ['chisel','chisel2','fork','hammer','knife','mallet','paintbrush',
	'peeler','screwdriver','sharpeningsteel','spoon','spoon2',
	'washingbrush','wrench']

critVal = 2.64
# (1-(0.05/6)/2) = 0.4958
# See: http://www.statisticshowto.com/articles/how-to-find-a-critical-value-in-ten-seconds-two-tailed-test/
# Looking up this value in a z-table gives 2.64 as the critical value
# see: http://en.wikipedia.org/wiki/Standard_normal_table

if __name__ == "__main__":
	
	w = wBitmap/rescale/ratioPxDegr
	h = hBitmap/rescale/ratioPxDegr
	
	print w
	print h
	