#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: parse.py

"""
DESCRIPTION:
From samples to dm with one trial per row.

Note that we use saccade events instead of fixation events. This is because
it often occurred that a fixation started but not ended (before the 
stop-recording item), which is why we loose a lot of trials.

TODO: to make th LP dependent on ECC, we need to know ECC while parsing.
"""

import pylab
import sys
import os
import numpy as np
from exparser.DataMatrix import DataMatrix
from exparser.EyelinkAscFolderReader import EyelinkAscFolderReader
from exparser.CsvReader import CsvReader
from exparser.Cache import cachedDataMatrix, cachedArray
import constants
from matplotlib import pyplot as plt

class MyReader(EyelinkAscFolderReader):
	
	def __init__(self,  exp, **kwargs):
		
		"""
		Constructor.
		
		Keyword arguments:
		rtDm		--	A DataMatrix with RTs. (default=None)
		"""
		
		self.exp = exp
		super(MyReader, self).__init__(**kwargs)
	
	# Perform some initalization before we start parsing a trial
	def initTrial(self, trialDict):
		
		"""
		Initialize a trial:
		
		Arguments:
		trialDict -- a trial dictionary
		"""

		# Set starting values:
		#self.stimOnset = None
		self.waitForSacc= False
		
		self.saccCount = 0
		
		# In previous 2 experiments: manually adapt count_trial_sequence because
		# it was not logged:
		if self.exp != "004C":
			self.count_trial_sequence = 0

		# Make column headers where, in princicpe, the data from 10 saccades
		# can be saved.
		# Note that we have to do this because only the intersection of 
		# column headers is retained when merging pp DMs:
		for i in range(1,11):
			for prop in ["duration", "eTime", "ex", "ey", \
				"sTime", "size", "sx", "sy"]:
				trialDict["sacc%s_%s" % (i, prop)] = -1000
		
		# In Exp 004A, those Booleans will be set to true in the unlikely 
		# event of a failed fixation check on the fixation dot and/or object.
		trialDict['checkFixDotFailed'] = False
		trialDict['checkObjectFailed'] = False

		
	def parseLine(self, trialDict, l):
		
		"""
		Parse a single line (in list format) from a trial

		Arguments:
		trialDict 	-- the dictionary of trial variables
		l 			-- a list
		"""


		# MSG	6352138 display stimulus
		if len(l) == 4 and l[2] == 'display' and l[3] == "stimulus":
			#print "yes"
			#sys.exit()
			trialDict['stim_onset'] = l[1]
			self.tracePhase = 'stim'
			
			# The time stamp of the stimulus (necessary for calculating 
			# latencies):
			self.stimOnset = l[1]
			self.waitForSacc = True
		
		if self.waitForSacc:

			sacc = self.toSaccade(l)
			if sacc != None:

				# The y coordinate of the fixation position should have
				# a certain distance from the fixation dot:
				if sacc['ey'] > constants.thUpper or sacc["ey"] < constants.thLower:
					
					# Fixation should end after stimulus onset.
					if sacc["eTime"] >= self.stimOnset:				
					
						self.saccCount +=1
						
						# Save all available sacc info:
						for i in sacc:
							trialDict["sacc%s_%s" % (self.saccCount, i)] = sacc[i]
		
		if self.exp == "004A":
			# Fox Exp 004A:
			# Determine the time stamp of the onset of the central fixation dot 
			# (which was the start fot he first fixation check):
			# MSG	31238826 display fixation
			if 'display' in l and 'fixation' in l:
				trialDict['timestampFixOnset'] = l[1]
			
			# Determine the success of the first fixation check (on the central 
			# fix dot):
			# MSG	2374487 fixation on fixdot check failed for 4000 samples in a row
			if 'fixation' in l and 'fixdot' in l and 'samples' in l and 'failed' in l:
				trialDict['checkFixDotFailed'] = True
			
			# Determine the success of the second fixation check (on the object):
			# MSG	2383406 fixation on object check failed for 4000 samples in a row
			if 'fixation' in l and 'object' in l and 'failed' in l:
				trialDict['checkObjectFailed'] = True

			# Determine the duration of the first fixation check (on the central fix
			# dot):
			# MSG	31239346 fixation on fixdot check successfull
			if 'fixation' in l and 'fixdot' in l and 'successfull' in l:
				trialDict['durCheck1'] = l[1] - trialDict['timestampFixOnset']

			# Determine the success of the second fixation check (on the object):
			# MSG	31239765 fixation on object check successfull
			if 'fixation' in l and 'object' in l and 'successfull' in l:
				self.timestampSuccess = l[1]
				trialDict['durCheck2'] = l[1] - self.stimOnset

		# Determine RT by taking stim onset 
		# (rather than the absolute trial onset) into account:
		# MSG	12966144 response given = 7
		if 'response' in l and 'given' in l:
			trialDict['rtOnset'] = l[1]
			trialDict['RT'] = l[1] - self.stimOnset
			
			# Stop waiting for fixations:
			self.waitForSacc = False
			self.tracePhase = None



	# Perform some finalization after we we have parsed a trial. 
	def finishTrial(self, trialDict):
		
		"""
		Finalizes the trial.

		Arguments:
		trialDict -- a trial dictionary
		"""

		# Write some variables to dict
		trialDict["saccCount"] = self.saccCount
		
		# Add some extra variables for first 2 experiments:
		if self.exp != "004C":
			trialDict["count_trial_sequence"] = self.count_trial_sequence
			self.count_trial_sequence +=1
			
		trialDict["expId"] = self.exp
		trialDict["offlineDriftCorr"] = self.offlineDriftCorr
		
		print trialDict["file"], trialDict["count_trial_sequence"], \
			trialDict['saccCount'], trialDict['trialId']
		
		
@cachedDataMatrix
def parseAsc(exp, offlineDriftCorr = None):

	"""
	Parses ASC files.
	
	Arguments:
	exp 			--- {"004A", "004B", "004C"}, experiment Id
	
	Keyword arguments:
	driftCorr		--- Boolean indicating whether or not to apply offline 
						driftcorrection. Set to False, because ONLINE
						drift correction was activated in OpenSesame
	"""
	
	if offlineDriftCorr == None:
		raise Exception("Please specificy whether offline drift correction should be enabled")
	
	path = "/home/lotje/Documents/PhD Marseille/Studies/004/%s/data/ASC" % exp
	
	dm = MyReader(exp, maxN=None, acceptNonMatchingColumns = True, \
		path = path, offlineDriftCorr= offlineDriftCorr).dataMatrix()
	
	return dm

if __name__ == "__main__":
	
	for exp in ["004B", "004C"]:
		dm = parseAsc(exp = exp, cacheId = "%s_parsed" % exp)

	
	
