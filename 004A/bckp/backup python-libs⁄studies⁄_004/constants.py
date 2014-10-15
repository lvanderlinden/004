#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: constants.py

"""
DESCRIPTION:

"""

# Minimum displacement before calling something a saccade.
# Example:
# if sacc != None and sacc['size'] > constants.minSaccSize:
# 	self.saccOnset = sacc['sTime']

minSaccSize = 100

CoGCorrTooLarge = 8 # in px
xCen = 512
yCen = 384

ratioPxDegr = 34

# Dummy variable to give all during-parsing-determined variables a starting
# value.
parseDummyVar = -1000