#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: parseAsc.py

"""
DESCRIPTION:
By using the exparser function EyelinkAscFolderReader() I walk through every
line in the ASC file in order to deduce the relevant information:
- Trial information, usually contained by lines starting with 'MSG'.
- Relevant eye coordinates and their time stamps, contained by lines
	starting with e.g. 'SFIX' (start of fixation) 'EFIX' (end of fixation),
	'SSAC' (start of fixation) and 'ESAC' (end of fixation). 
If only the events from the EDF file are converted to the ASC file, this means 
that I trust that the EyeLink software correctly labeled those events.


About drift correction:
If wanted, an offline drift-correction procedure can be carried out, in order
to correct for slight drifts of the camera. Note that it's theoretically 
difficult to distinguish between whether the participant is not fixating exactly
on the cross, or whether the camera is drifted. In practice, however, the latter
seems much more likely.
Also, offline drift correction is not really necessary when landing positions 
are compared within subjects and between conditions. However, when absolute
landing positions are of interest (e.g. to determine whether there is indeed
a bias to land slightly towards the left of the center, drift correction IS 
a good idea. However, note that in this case it's still possible that the drift
occurred just after the drift correction. Looking at the angle between start
fixation and landing position will solve this.


TODO: 
- Plot trial info.
- Correct y coordinate for CoG as well?
"""

# Import Python libraries:
import math
import numpy as np
import scipy
from matplotlib import cm
from matplotlib import pyplot as plt
from scipy.stats import nanmean, nanmedian
import math
from PIL import Image, ImageDraw
import sys
import os

# Import own modules:
import studies._004.gravity as gravity
from matplotlib import pyplot as plt
from exparser.EyelinkAscFolderReader import EyelinkAscFolderReader
from exparser.DataMatrix import DataMatrix
from exparser.PivotMatrix import PivotMatrix
import studies._004.constants as constants

trialId = 0

# Declare constants:
xPsycho = 0

src = '/home/lotje/python-libs/studies/_004B'


if "--parse" in sys.argv:
	# Get dictionary containing x and y after correction for CoG and mask:
	d= gravity.gravDictMask(show=False, edgeDetect=True,printScreen=False)

class MyReader(EyelinkAscFolderReader):
	
	# Perform some initalization before we start parsing a trial
	def initTrial(self, trialDict):
		
		"""
		Initialize a trial:
		
		Arguments:
		trialDict -- a trial dictionary
		"""
		
		# Create empty lists that we will use to store saccades and fixations
		# during parsing:
		# CHECK: is this only for plotting?
		global saccList, fixList
		saccList = []
		fixList = []
		
		# Make the trial counter global:
		global trialId
		
		# Create some Booleans and give them starting values:
		self.waitForSacc = False
		self.saccOnset = None
		self.stimTime = None

		# Give to-be-determined new variables dummy values such that the 
		# success of this process can be checked later on (via dm.select()):
		trialDict['saccLat'] = trialDict['xCoG'] = trialDict['xCoGMask'] = \
			trialDict['yCoG'] = trialDict['yCoGMask'] =	trialDict['rtFromStim'] = \
			trialDict['endX'] = trialDict['endXCorr'] = trialDict['endXCorrMask'] = \
			trialDict['corrDirection'] = trialDict['corrDirectionMask'] = \
			trialDict['endY'] = \
			trialDict['startX'] = trialDict['startY'] = \
			constants.parseDummyVar
		
		## Those Booleans will be set to true in the unlikely event of 
		## a failed fixation check on the fixation dot and/or object.
		#trialDict['checkFixDotFailed'] = False
		#trialDict['checkObjectFailed'] = False
		
		# Adapt the trial counter:
		trialId += 1
		
	# Perform some finalization after we we have parsed a trial. 
	def finishTrial(self, trialDict):
		
		"""
		Finalizes the trial.

		Arguments:
		trialDict -- a trial dictionary
		"""

		# If no saccade was detected at all during a trial, saccLat is set to 
		# -1.
		if self.saccOnset == None:
			trialDict['saccLat'] = -1
		
		# If saccade onset was detected, calculate its latency from stimOnset:
		# TODO: is this correct or should I use fixCheck = succesful?
		else:
			trialDict['saccLat'] = self.saccOnset - self.stimOnset
		
		# We need some trial information for the CoG calculations below.
		# We read this info from the trialDict:
		l = trialDict['picture_name'].split('_')
		trialDict['symm'] = l[0]
		
		obj = trialDict["object"]
		handle = trialDict["handle_side"]
		maskSide = "mask_%s"%trialDict["mask_side"]
		yPsycho = trialDict["y_stim"]
		
		# Add coordinates of the object after correcting for nr of pixels
		# and edges:
		
		# Regardless of mask (based on original bitmap):
		trialDict['xCoG'] = xPsycho + d[obj,"mask_control", handle][0]
		trialDict['yCoG'] = yPsycho + d[obj,"mask_control", handle][1]
		
		# With mask taken into account:
		trialDict['xCoGMask'] = xPsycho + d[obj,maskSide, handle][0]
		trialDict['yCoGMask'] = yPsycho + d[obj,maskSide, handle][1]
		
		# Determine the direction of the correction (i.e. whether CoG is left
		# or right from center-center:
		trialDict['corrDirection'] = d[obj,"mask_control", handle][2]
		trialDict['corrDirectionMask'] = d[obj,maskSide, handle][2]
		
		# Correct the landing position (in px) according to the CoG:
		trialDict['endXCorr'] = trialDict['endX']-trialDict['xCoG']
		trialDict['endXCorrMask'] = trialDict['endX']-trialDict['xCoGMask']
		
		# TODO: why??
		# MSG	14329200 var cond ('handle_left', 'mask_left')
		del trialDict['cond']
		
		# If the variable 'response' is not an int, change it to -1 (otherwise
		# the dm can't handle the 'None's or 'timeout's
		if type(trialDict['response']) != int:
			trialDict['response'] = -1
		
	def parseLine(self, trialDict, l):
		
		"""
		Parse a single line (in list format) from a trial

		Arguments:
		trialDict -- the dictionary of trial variables
		l -- a list
		"""
		
		# MSG	14327176 display stimulus
		if len(l) > 3 and l[2] == 'display' and l[3] == 'stimulus':
			
			# After stimulus presentation, start searching for a saccade:
			self.waitForSacc = True
			# The time stamp of the stimulus (necessary for calculating 
			# latencies):
			self.stimOnset = l[1]
			
		if self.waitForSacc:
			sacc = self.toSaccade(l)
			# If EyeLink detecting something as a saccade AND the displacement
			# is larger than the minimum displacement necessary in order
			# to call something a saccade:
			if sacc != None and sacc['size'] > constants.minSaccSize:
				
				# Time stamp of the saccade:
				self.saccOnset = sacc['sTime']
				
				# Save the coordinates of the saccade:
				trialDict['startX'] = sacc['sx'] - constants.xCen
				trialDict['endX'] = sacc['ex'] - constants.xCen
				trialDict['endY'] = sacc['ey'] - constants.yCen
				trialDict['startY'] = sacc['sy'] - constants.yCen
				
				# Stop waiting for the saccade in this trial:
				self.waitForSacc = False
											
		## Determine the time stamp of the onset of the central fixation dot 
		## (which was the start fot he first fixation check):
		## MSG	31238826 display fixation
		#if 'display' in l and 'fixation' in l:
			#trialDict['timestampFixOnset'] = l[1]
		
		## Determine the duration of the first fixation check (on the central fix
		## dot):
		## MSG	31239346 fixation on fixdot check successfull
		#if 'fixation' in l and 'fixdot' in l and 'successfull' in l:
			#trialDict['durCheck1'] = l[1] - trialDict['timestampFixOnset']

		## Determine the success of the first fixation check (on the central 
		## fix dot):
		## MSG	2374487 fixation on fixdot check failed for 4000 samples in a row
		#if 'fixation' in l and 'fixdot' in l and 'samples' in l and 'failed' in l:
			#trialDict['checkFixDotFailed'] = True
		
		## Determine the success of the second fixation check (on the object):
		## MSG	31239765 fixation on object check successfull
		#if 'fixation' in l and 'object' in l and 'successfull' in l:
			#self.timestampSuccess = l[1]
			#trialDict['durCheck2'] = l[1] - self.stimOnset

		## Determine the success of the second fixation check (on the object):
		## MSG	2383406 fixation on object check failed for 4000 samples in a row
		#if 'fixation' in l and 'object' in l and 'failed' in l:
			#trialDict['checkObjectFailed'] = True
		
		## Determine the reaction time by taking the onset of the stimulus 
		## (rather than the absolute trial onset) into account:
		## MSG	12966144 response given = 7
		if 'response' in l and 'given' in l:				
			trialDict['rtFromStim'] = l[1] - self.stimOnset
			#trialDict['rtFromSuccess'] = l[1] - self.timestampSuccess

	def startTrial(self, l):
		
		"""
		Determines whether a list corresponds to the start of a trial
		"""

		# MSG	14320597 start_trial
		# Adapt the trial ID:
		global trialId
		if len(l) > 2 and l[0] == 'MSG' and l[2] == self.startTrialKey:
			return trialId
		return None
		
# Call the above only if --parse in sys.argv. Otherwise, open the saved dm 
# called 'data.csv' (because it takes quite long to parse all ASC files).
def parseAsc(driftCorr = False):
	
	if '--parse' in sys.argv:
		dm = MyReader(maxN=None,offlineDriftCorr = driftCorr).dataMatrix()		
		dm.save(os.path.join(src,'data - drift correction = %s.csv'%driftCorr))
	else:
		m = np.genfromtxt(os.path.join(src,'data - drift correction = %s.csv'%driftCorr),\
			dtype=None, delimiter=',')
		dm = DataMatrix(m)
	
	return dm

if __name__ == "__main__":
	
	dm = parseAsc()
	dm = parseAsc(driftCorr = True)
	
	
