#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: parse.py

"""
DESCRIPTION:
From samples to dm with one trial per row.
"""

import sys
import os
import numpy as np
from exparser.DataMatrix import DataMatrix
from exparser.EyelinkAscFolderReader import EyelinkAscFolderReader
from exparser.CsvReader import CsvReader
from exparser.Cache import cachedDataMatrix, cachedArray
import constants

class MyReader(EyelinkAscFolderReader):
	
	def __init__(self, rtDm=None, **kwargs):
		
		"""
		Constructor.
		
		Keyword arguments:
		rtDm		--	A DataMatrix with RTs. (default=None)
		"""
		
		#self.rtDm = rtDm
		super(MyReader, self).__init__(**kwargs)
	
	# Perform some initalization before we start parsing a trial
	def initTrial(self, trialDict):
		
		"""
		Initialize a trial:
		
		Arguments:
		trialDict -- a trial dictionary
		"""

		# Set starting values:
		self.waitForSacc = False
		#self.stimOnset = None
		self.waitForFix = False
		self.saccOnset = None
		#self.rt = None
		
		self.saccCount = 0
		self.fixCount = 0

		# Make column headers where, in princicpe, the data from 10 saccades
		# can be saved.
		# Note that we have to do this because only the intersection of 
		# column headers is retained when merging pp DMs:
		for i in range(1,11):
			for event in ["sacc", "fix"]:
				for prop in ["duration", "eTime", "x", "y", "ex", "ey", \
					"sTime", "size", "sx", "sy"]:
					trialDict["%s%s_%s" % (event,i, prop)] = -1000
	
	def startTrial(self, l):
		
		"""
		Determines whether a list corresponds to the start of a trial
		"""
	
		# MSG	6343114 start_trial 2
		if len(l) == 4 and l[0] == 'MSG' and "start_trial" in l[2]:
			
			# Remember trial count:
			self.trialCount = l[2].split("_")[-1]
			
			return True			
		
		return None

		
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
			
			# The time stamp of the stimulus (necessary for calculating 
			# latencies):
			self.stimOnset = l[1]

			# TODO:
			# After stimulus presentation, start searching for fixations and 
			# saccades
			#self.waitForSacc = True
			self.waitForFix = True
		
		# TODO TODO TODO: CHECK!
		# Below is different than 008B, because here we don't know the response
		# onset yet when parsing. So only the criteria relative to stimulus
		# onset are used.
		if self.waitForFix:

			fix = self.toFixation(l)
			if fix != None:

				# The y coordinate of the fixation position should have
				# a certain distance from the fixation dot:
				if fix['y'] > constants.thUpper or fix["y"] < constants.thLower:
					
					# Fixation should end after stimulus onset.
					if fix["eTime"] >= self.stimOnset:				
					
						self.fixCount +=1
						
						# Save all available sacc info:
						for i in fix:
							trialDict["fix%s_%s" % (self.fixCount, i)] = fix[i]
						
					#self.waitForSacc = True		
						
		# TODO: is it a good idea to not look at saccades at all?
		#if self.waitForSacc:
			#sacc = self.toSaccade(l)
			
			#if sacc != None:
			
				## Saccade should start after stimulus onset:
				#if sacc["sTime"] >= self.stimOnset:
					#self.saccCount +=1
					
					## Save all available sacc info:
					#for i in sacc:
						#trialDict["sacc%s_%s" % (self.saccCount, i)] = sacc[i]
					##self.waitForFix = True
		
		# Determine RT by taking stim onset 
		# (rather than the absolute trial onset) into account:
		# MSG	12966144 response given = 7
		if 'response' in l and 'given' in l:
			trialDict['rtOnset'] = l[1]
			trialDict['RT'] = l[1] - self.stimOnset
			
			# Stop waiting for saccade:
			self.waitForSacc = False
			self.waitForFix = False
			




	# Perform some finalization after we we have parsed a trial. 
	def finishTrial(self, trialDict):
		
		"""
		Finalizes the trial.

		Arguments:
		trialDict -- a trial dictionary
		"""

		# Write some variables to dict
		trialDict["saccCount"] = self.saccCount
		trialDict["fixCount"] = self.fixCount
		print self.saccCount, self.fixCount
		print trialDict["file"], trialDict["count_trial_sequence"]
		
		#print "trial count = ", trialDict["count_trial_sequence"]
		
		# TODO: not sure about this reasoning because we used different criteria
		# compared to 008B (only based on stim onset, not on response onset)
		## In theory, there always be should be one more fixation than a saccade,
		## unless there were no saccades nor fixations detected, or there was
		## a fixation that started within the SR interval but never ended.
		## The latter was checked by hand, which is why the assertion below
		## is still save.
		#assert(self.saccCount in (0, self.fixCount-1, self.fixCount))
		#if self.saccCount == self.fixCount and self.saccCount != 0:
			#raw_input()

@cachedDataMatrix
def parseAsc(driftCorr = False):

	"""
	Parses ASC files.
	
	Keyword arguments:parseAsc
	driftCorr		--- Boolean indicating whether or not to apply offline 
						driftcorrection. Set to False, because ONLINE
						drift correction was activated in OpenSesame
	"""
	dm = MyReader(maxN=None, acceptNonMatchingColumns = True) \
		.dataMatrix()
		
	return dm

	
	
