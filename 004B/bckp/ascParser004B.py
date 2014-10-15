#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: ascParser.py

"""
DESCRIPTION:

Parser for 004B

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
- yCoordinates:
	-normalise
	- correct for cog

- add direction to minimum y ecc eye movements?
- rtFromLanding == rtFromStim???

CHANGELOG:
27-06-2013:
	- Determine end and start x coordinates for all saccades.
	- Determine latencies for all saccades

28-06-2013:
	- Determine number of within-object saccades
	- Correct all x coordinates for CoG (with and without mask taken into account)
		during parsing
	- Normalize all x coordinates such that 0.5 refers to the middle of the bitmap.

29-06-2013:
	- Determine properties of within-object fixations
	
01-07-2013:
	- Threshold for saccades and fixations to occur in the dm:
		eyes should have crossed horizontal line between
		center and half of the minimum y eccentricity (regardless of upper
		or lower visual field)
	- Individual trial plots are saved, and show the 'to the object' eye
		movements that fitted the above criteria. Also, the width of the object
		is indicated by green lines.
	- The size of the imaginary box around the objects is divided by the scaling factor
		used in OpenSesame.
	- rtFromLanding is determined here (and not in getDM anymore)
	- Total gaze duration is calculated by adding the fixation durations of all
		within-object fixations
	- xCoG is plotted in trial plots
	- Y coordinates of the target are converted from PsychoPy to normal coordinates, 
		and then the y coordinates of the EM's are converted as if the target
		was presented with y center = 0. 

02-07-2013:
- New y coordinates are used to:
	- normalise according to object height 
	- correct for cog


	
"""

# Import Python libraries:
import numpy as np
from matplotlib import pyplot as plt
import sys, os

# Import own modules:
from exparser.EyelinkAscFolderReader import EyelinkAscFolderReader
from exparser.DataMatrix import DataMatrix
from exparser.CsvReader import CsvReader
from exparser.PivotMatrix import PivotMatrix
import studies._004.getCoG
import studies._004.constants
import studies._004.drawBox

trialId = 0

# Declare constants:

# Stimulus was always presented on the vertical center of the 
# screen:
xStimPsycho = 0

# Folder called 'data', containing ASCs per participant, can be found here:
src = '/home/lotje/Documents/PhD Marseille/Studies/004B - One-object experiment - Orientation effect - aligned to CoG/Analysis'

# Plots should be save here:
dst = '/home/lotje/Documents/PhD Marseille/Studies/004B - One-object experiment - Orientation effect - aligned to CoG/Analysis/plots/plots per trial'

# Boolean indicating whether or not to plot EM properties per trial:
plotPerTrial = True

# If asc files are going to be parsed, create the dictionary containing the CoG
# per stimulus. If asc files are not (re)parsed, this can be skipped.

if "--parse" in sys.argv:

	# Get dictionary containing x and y after correction for CoG and mask:
	d= studies._004.getCoG.gravDictMask(show=False, edgeDetect=True,invert = True, \
		printScreen=False)
	
	# Get dictionary containing w and h of imaginary boxes around the stimuli:
	boxDict = studies._004.drawBox.boxDict()

class MyReader(EyelinkAscFolderReader):
	
	# Perform some initalization before we start parsing a trial
	def initTrial(self, trialDict):
		
		"""
		Initialize a trial:
		
		Arguments:
		trialDict -- a trial dictionary
		"""
		
		# Make the counters counter global:
		
		# trialId is NOT reset for every trial (but IS reset for
		# every pp:
		global trialId
		trialId += 1
		
		# saccCount IS reset for every pp:
		global saccCount, fixCount
		saccCount = 0
		fixCount = 0
		
		# Create some Booleans and give them starting values:
		self.waitForSacc = False
		self.waitForFix = False
		self.saccOnset = None
		self.stimTime = None
		
		# Fixation checks do not have to be verified anymore, because
		# no gaze contingent stuff was used in the second study.

		
		# Give endX2 a starting value because this variable is needed
		# for determining refixProb (i.e., it should exist, even if there
		# was not a second fixtion).
		trialDict["endX2"] = ''
		
		# Give eTimeSacc1 a starting value because this variable is needed
		# for determinging rtFromLanding (i.e., it should exist, even if 
		# there was not even a first saccade):
		trialDict['eTimeSacc1'] = ''
		
		# Create empty lists for collecting the raw fixation and saccade
		# properties that we'll need for plotting purposes, and make them
		# global:
		rawFix = []
		rawSacc = []
		global rawFix, rawSacc
		
		
	# Perform some finalization after we we have parsed a trial. 
	def finishTrial(self, trialDict):
		
		"""
		Finalizes the trial.

		Arguments:
		trialDict -- a trial dictionary
		"""

		# Determine the size of the imaginary box:
		w, h = boxDict[trialDict["picture_name"]]
		
		# Add to trial dict:
		trialDict["boxWidth"] = w/studies._004.constants.rescale
		trialDict["boxHeight"] = h/studies._004.constants.rescale
		

		# Convert PsychoPy y coordinates to normal coordinates:
		
		# Target y coordinate in PsychoPy coordinates (used in OpenSesame)
		yStimPsycho = trialDict['y_stim']
		
		# Target y coordinate converted to normal (0,0 = top left):
		yStimNormal = (trialDict['y_stim']*-1) + studies._004.constants.yCen
		trialDict['yStimNormal'] = yStimNormal 

		# We need some trial information for the CoG calculations below.
		# We read this info from the trialDict:
		l = trialDict['picture_name'].split('_')
		trialDict['symm'] = l[0]
		
		obj = trialDict["object"]
		handle = trialDict["handle_side"]
		maskSide = "mask_%s"%trialDict["mask_side"]
		
		# Add coordinates of the object after correcting for nr of pixels
		# and edges:
		
		# Regardless of mask (based on original bitmap):
		trialDict['xCoG'] = xStimPsycho + d[obj,"mask_control", handle][0]
		trialDict['yCoG'] = yStimNormal + d[obj,"mask_control", handle][1]
		trialDict['yCoGZero'] = 0 + d[obj,"mask_control", handle][1] # TODO: correct?
		
		# With mask taken into account:
		trialDict['xCoGMask'] = xStimPsycho + d[obj,maskSide, handle][0]
		trialDict['yCoGMask'] = yStimNormal + d[obj,maskSide, handle][1] # TODO: correct? verdere gevolgen?
		trialDict['yCoGMaskZero'] = 0 + d[obj,maskSide, handle][1]
			
		# Determine the direction of the correction (i.e. whether CoG is left
		# or right from center-center:
		
		# Based on control object;
		trialDict['corrDirection'] = d[obj,"mask_control", handle][2]
		
		# Based on mask condition:
		trialDict['corrDirectionMask'] = d[obj,maskSide, handle][2]
		
		# Determine RT from landing:
		if trialDict['eTimeSacc1'] != '':
			trialDict['rtFromLanding'] = trialDict['timestampResponse'] - trialDict["eTimeSacc1"]
		
		# Make a variable indicating whether or not a refixation was made 
		# (irrespective of how many):
		if trialDict["endX2"] != '':
			trialDict["refixProb"] = 1
		else:
			trialDict["refixProb"] = 0
		
		# Save counters:
		trialDict["saccCount"] = saccCount
		trialDict["fixCount"] = fixCount
		
		# TODO: why??
		# MSG	14329200 var cond ('handle_left', 'mask_left')
		del trialDict['cond']
		
		# TODO: why??
		# If the variable 'response' is not an int, change it to -1 (otherwise
		# the dm can't handle the 'None's or 'timeout's
		if type(trialDict['response']) != int:
			trialDict['response'] = -1

		# Determine the x coordinate of the target, which was determined
		# in OpenSesame like so:
		# x_stim_corr = x_stim - float(xCoG)
		# where x_stim = 0 (center of the screen in PsychoPy coordinates)
		
		# Target x coordinate:
		trialDict['xStim'] = studies._004.constants.xCen - trialDict['xCoG']
		

		# Create all coordinates that are corrected for the CoG,
		# with and without mask taken into account:
		# Also, create coordinates that are normalized to the size of the
		# object:
		
		for i in range(1,saccCount+1):
			
			# X COORDINATES:
			
			# Correct for CoG without mask taken into account 
			# (all objects are treated as the control condition in the Mask manipulation):
			trialDict["endX%sCorr" % i] = trialDict["endX%s" % i] - trialDict["xCoG"]
			trialDict["startX%sCorr" % i] = trialDict["startX%s" % i] - trialDict["xCoG"]
			
			# With mask taken into account (CoG depends on mask condition)
			trialDict["endX%sCorrMask" % i] = trialDict["endX%s" % i] - trialDict["xCoGMask"]
			trialDict["startX%sCorrMask" % i] = trialDict["startX%s" % i] - trialDict["xCoGMask"]
			
			# Y COORDINATE:
			
			# Determine different kinds of y coordinates (note that these are more complex
			# than x coordinates, since objects were not presented on y Cen but with a 
			# a variable vertical eccentricity).
			
			# Actual landing position:

			# y landing position as if y center of target = zero:
			
			trialDict['endY%s'%i] = trialDict['endYRaw%s' % i] - trialDict['yStimNormal']
			trialDict['startY%s'%i] = trialDict['startYRaw%s' % i] - trialDict['yStimNormal']
			
			# y landing position normalised according to height of the imaginary box:
			trialDict['endY%sNorm'%i] = trialDict['endY%s'%i]/trialDict['boxHeight']
			trialDict['startY%sNorm'%i] = trialDict['startY%s'%i]/trialDict['boxHeight']
			
			# Correct for CoG (no distinction between with and without mask here):
			trialDict['endY%sCorr'%i] = trialDict['endY%s'%i] - trialDict['yCoGZero']
			trialDict['startY%sCorr'%i] = trialDict['startY%s'%i] - trialDict['yCoGZero']
			
			# Determine corrected normalised y landing position:
			trialDict['endY%sCorrNorm'%i] = trialDict['endY%sCorr'%i]/trialDict['boxHeight']
			trialDict['startY%sCorrNorm'%i] = trialDict['startY%sCorr'%i]/trialDict['boxHeight']
			
			print
			print '		Target coordinates:'
			print
			print trialDict['y_stim'], '= PsychoPy y coordinate'
			print trialDict['yStimNormal'], '= converted to EyeLink y coordinate'
			
			print
			print '		Saccade coordinates:'
			print
			print trialDict['endYRaw%s' % i],'= absolute landing position in EyeLink coordinates'
			print trialDict['endY%s'%i], '= landing position as if target y center = zero'
			print trialDict['endY%sNorm'%i], '= landing position normalised to object height'
			print trialDict['visual_field']
			
			#sys.exit()

			# X COORDINATES:
			
			for var in ["endX%s" % i, "startX%s" % i, "endX%sCorr" % i, "endX%sCorrMask" % i, \
				"startX%sCorr" % i, "startX%sCorrMask" % i]:
				
				# Convert to visual degrees:
				trialDict["%sDegrees"%var] = trialDict[var]/studies._004.constants.ratioPxDegr
				# Normalize:
				trialDict["%sNorm"%var] = trialDict[var]/trialDict["boxWidth"]
			
			# Y COORDINATES:
			
			for var in ['endY%s' % i, "startY%s" % i]:
				# Convert to visual degrees:
				trialDict["%sDegrees"%var] = trialDict[var]/studies._004.constants.ratioPxDegr
				# Normalize is already done above.
				#trialDict["%sNorm"%var] = trialDict[var]/trialDict["boxHeight"]
			
				
		# Add total gaze duration:
		gazeDur = 0
		for i in range(1, fixCount +1):
			if trialDict["durationFix%s" % i] != '':
				gazeDur += trialDict["durationFix%s" % i]
		trialDict['gazeDur'] = gazeDur
		
		if plotPerTrial:
		
			# Plot saccade landing positions per trial:
			fig = plt.gcf()

			# Title:
			plt.title("%s handle  = %s mask = %s"%(trialDict["object"],\
				trialDict["handle_side"], trialDict["mask_side"]))
			
			# Retain screen size:
			plt.xlim(0, studies._004.constants.screenW)
			plt.ylim(0, studies._004.constants.screenH)
			
			# Plot thresholds: 
			plt.axhline(studies._004.constants.yCen+\
				studies._004.constants.minSaccSize, color = 'orange')
			plt.axhline(studies._004.constants.yCen-\
				studies._004.constants.minSaccSize, color = 'orange')
			
			# Plot width of the object:
			plt.axvline(trialDict['xStim']+(trialDict["boxWidth"]/2), \
				color = 'green')
			plt.axvline(trialDict['xStim']-(trialDict["boxWidth"]/2), \
				color = 'green')

			# Plot center:
			plt.axhline(studies._004.constants.yCen, color = 'gray')
			plt.axvline(studies._004.constants.xCen, color = 'gray')
			
			# Plot center of gravity is not necessary anymore for 004B
			
			# Plot coordinates of the stimulus:
			plt.axhline(trialDict['yStimNormal'], color = 'lightblue')
			plt.axvline(trialDict['xStim'], color = 'lightblue')
			# Plot height:
			plt.axhline(trialDict['yStimNormal'] + trialDict['boxHeight']/2, color = 'lightblue')
			plt.axhline(trialDict['yStimNormal'] - trialDict['boxHeight']/2, color = 'lightblue')
			
			# Trick to deduce x and y coordiantes from list, see:
			# http://stackoverflow.com/questions/2282727/draw-points-using-matplotlib-pyplot-x1-y1-x2-y2
			
			plt.plot(*sum(rawSacc, []), marker = 'o', color='r')
			plt.plot(*sum(rawFix, []), marker = 'o', color = 'b')
			
			
			dstPp = os.path.join(dst, trialDict['file'])
			
			if not os.path.exists(dstPp):
				os.makedirs(dstPp)
				
			dstPlot = os.path.join(dstPp, '%s.png'%trialId)
			print dstPlot
			plt.savefig(dstPlot)
			#plt.show()
			#sys.exit()
			plt.clf()
			
		
	def parseLine(self, trialDict, l):
		
		"""
		Parse a single line (in list format) from a trial

		Arguments:
		trialDict -- the dictionary of trial variables
		l -- a list
		"""
		
		# MSG	14327176 display stimulus
		if len(l) > 3 and l[2] == 'display' and l[3] == 'stimulus':
			
			trialDict['stimOnset'] = l[1]
			
			# After stimulus presentation, start searching for a saccade:
			self.waitForSacc = True
			# The time stamp of the stimulus (necessary for calculating 
			# latencies):
			self.stimOnset = l[1]
			
		if self.waitForFix:

			fixation = self.toFixation(l)
			
			# If the line is not empty, the EyeLink algo detected something
			# as a fixation:
			if fixation != None:
				
				yFix = fixation['y'] - studies._004.constants.yCen
				
				if abs(yFix) > studies._004.constants.minSaccSize:
					
					global fixCount
					fixCount +=1 
					
					# Save duration:
					trialDict["durationFix%s" % fixCount] = fixation["duration"]
					
					# Save coordinates (relative to center):
					trialDict["xFix%s"% fixCount] = fixation["x"] - studies._004.constants.xCen
					trialDict["yFix%s"% fixCount] = fixation["y"] - studies._004.constants.yCen
				
				
					# Add to the temp list:
					rawFix.append([fixation['x'], fixation['y']])
		
		if self.waitForSacc:
			
			# If the line is not empty, the EyeLink algo detected smth as a saccade.
			sacc = self.toSaccade(l)
			
			if sacc != None:
				
				# Extra checks: 
				# The eyes must be somewhat at the top or bottom of 
				# the screen (i.e., not still at the center):
				
				yLanding = sacc['ey'] - studies._004.constants.yCen
				
				if abs(yLanding) > studies._004.constants.minSaccSize:
					
					# Start waiting for a fixation:
					self.waitForFix = True
					
					# Add 'one' to the saccade counter:
					global saccCount
					saccCount +=1
					
					# Determine all the properties of this saccade and store them in
					# variables which have the saccade counter in their name:
					
					# Save the time stamp of the saccade:
					self.saccOnset = sacc['sTime']
					
					# Save the coordinates of the saccade relative to center = 0,0:
					trialDict['startX%s'%saccCount] = sacc['sx'] - studies._004.constants.xCen
					#trialDict['startY%s'%saccCount] = sacc['sy'] - studies._004.constants.yCen
					trialDict['endX%s'%saccCount] = sacc['ex'] - studies._004.constants.xCen
					#trialDict['endY%s'%saccCount] = sacc['ey'] - studies._004.constants.yCen
					
					# Save the raw coordinates relative to upperleft = 0,0
					# (i.e. default EyeLink coordinats):
					trialDict['startXRaw%s'%saccCount] = sacc['sx']
					trialDict['startYRaw%s'%saccCount] = sacc['sy']
					trialDict['endXRaw%s'%saccCount] = sacc['ex']
					trialDict['endYRaw%s'%saccCount] = sacc['ey']

					trialDict["saccDur%s"%saccCount] = sacc["duration"]
					
					# Time stamps of the saccades:
					trialDict["sTimeSacc%s"%saccCount] = sacc["sTime"] # timestamp start of saccade
					trialDict["eTimeSacc%s"%saccCount] = sacc["eTime"] # timestampf end of saccade
					
					# Save the saccade latency:
					trialDict['saccLat%s'%saccCount] = sacc['sTime']-self.stimOnset
					trialDict['saccLandingTime%s'%saccCount] = sacc['eTime']-self.stimOnset
					
					# Add end coordinates to temp list:
					rawSacc.append([sacc['ex'], sacc['ey']])
					
				
		# Determine the time stamp of the onset of the central fixation dot 
		# (which was the start fot he first fixation check):
		# MSG	31238826 display fixation
		if 'display' in l and 'fixation' in l:
			trialDict['timestampFixOnset'] = l[1]
		
		# The success of the fixation checks is not applicable in 004B.
		# Determine the success of the second fixation check (on the object):
		
		# Determine the reaction time by taking the onset of the stimulus 
		# (rather than the absolute trial onset) into account:
		# MSG	12966144 response given = 7
		if 'response' in l and 'given' in l:
			trialDict['timestampResponse'] = l[1]
			trialDict['rtFromStim'] = l[1] - self.stimOnset
			# rtFromSuccess is not applicable in 004B.
			
		# TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO
		self.waitForSacc = True
					
		
	def startTrial(self, l):
		
		"""
		Determines whether a line corresponds to the start of a trial
		"""

		# MSG	14320597 start_trial
		# Adapt the trial ID:
		global trialId
		if len(l) > 2 and l[0] == 'MSG' and l[2] == self.startTrialKey:
			return trialId
	
		#return None
	
# Call the above only if --parse in sys.argv. Otherwise, open the saved dm 
# called 'data.csv' (because it takes quite long to parse all ASC files).

def parseAsc(driftCorr = False):
	
	if driftCorr:
		fName = "data_WITH_drift_corr.csv"
	else:
		fName = "data_NO_drift_corr.csv"
	
	if '--parse' in sys.argv:
		dm = MyReader(maxN=None,offlineDriftCorr = driftCorr).dataMatrix()		
		dm.save(fName)
	else:
		
		a = np.genfromtxt(fName, dtype=None, delimiter=",")
		dm = DataMatrix(a)
					
		#dm = CsvReader(fName, delimiter=',').dataMatrix()
		
	
	return dm
	
if __name__ == "__main__":
	
	parseAsc(driftCorr = True)
