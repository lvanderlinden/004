#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: ascParser.py

"""
DESCRIPTION:

Parser for 004


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


Free parameters:
- drift correction
- 

TODO:
- add direction to minimum y ecc eye movements? -> this will be difficult because
	visual field is not known yet at the time toSacc() is applied.
- check whether parsing for 004B went all right -> visual inspection of the 
	trial plots
- x axis normalisation is different for 004B!!!
How to normalise objects that are presented at a position corrected for CoG??
Cutoff to include within-object EM only doesn't work anymore.

# TODO: convert landing positions to visual degrees?

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

05-07-2013:
- Made script applicable for both 004A and 004B. The main differences are:
	- 004B did not have the gaze-contingent fix checks
	- 004B had variable x coordinates!
- Debug text added to trial plots
	
"""

# Import Python libraries:
import numpy as np
from matplotlib import pyplot as plt
import sys, os

# Import own modules:
from exparser.EyelinkAscFolderReader import EyelinkAscFolderReader
from exparser.DataMatrix import DataMatrix
import readCoG
import constants
import drawBox

trialId = 0

# Declare constants:

# Stimulus was always presented on the vertical center of the 
# screen:
xStimPsycho = 0

# Boolean indicating whether or not to plot EM properties per trial:
plotPerTrial = False
addText = True

plt.rc("font", family="ubuntu")
plt.rc("font", size=12)

# If asc files are going to be parsed, create the dictionary containing the CoG
# per stimulus. If asc files are not (re)parsed, this can be skipped.

if "--parse" in sys.argv:

	# Get dictionary containing x and y after correction for CoG and mask:
	d = readCoG.readCoG()
	# Get dictionary containing w and h of imaginary boxes around the stimuli:
	boxDict = drawBox.boxDict()

class MyReader(EyelinkAscFolderReader):
	
	def __init__(self, **args):
		
		self.exp = args['exp']		
		del args['exp']
		super(MyReader, self).__init__(**args)
		#EyelinkAscFolderReader.__init__(self, **args)

	# Perform some initalization before we start parsing a trial
	def initTrial(self, trialDict):
		
		"""
		Initialize a trial:
		
		Arguments:
		trialDict -- a trial dictionary
		"""
		
		# Make the counters counter global:
		
		# Plots should be save here:
		dst = "/home/lotje/Documents/PhD Marseille/Studies/004 - Single-object experiment - Handle-orientation effect/%s/results/plots/parse plots" % self.exp

		global dst
		
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
		
		if self.exp == "004A":
			# Those Booleans will be set to true in the unlikely event of 
			# a failed fixation check on the fixation dot and/or object.
			trialDict['checkFixDotFailed'] = False
			trialDict['checkObjectFailed'] = False
		
		# Give endX2 a starting value because this variable is needed
		# for determining refixProb (i.e., it should exist, even if there
		# was not a second fixtion).
		trialDict["endXRaw2"] = ''
		
		# Give eTimeSacc1 a starting value because this variable is needed
		# for determinging rtFromLanding (i.e., it should exist, even if 
		# there was not even a first saccade):
		trialDict['eTimeSacc1'] = ''
		
		# Same for endXRaw1, endX1, and endX1Norm (for plotting purposes):
		trialDict['endXRaw1'] = ''
		trialDict['endX1'] = ''
		trialDict['endX1Norm'] = ''
		
		
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
		
		
		# Make a new variable indicating the most contrasted side of the object:
		if trialDict["mask_side"] == "right":
			trialDict["contrast_side"] = "_left"
		if trialDict["mask_side"] == "control":
			trialDict["contrast_side"] = "control"
		if trialDict["mask_side"] == "left":
			trialDict["contrast_side"] = "right"

		# Determine the size of the imaginary box:
		w, h = boxDict[trialDict["picture_name"]]
		
		# Add to trial dict:
		trialDict["boxWidth"] = w/constants.rescale
		trialDict["boxHeight"] = h/constants.rescale
		

		# Convert PsychoPy y coordinates to normal coordinates:
		
		# Target y coordinate in PsychoPy coordinates (used in OpenSesame)
		yStimPsycho = trialDict['y_stim']
		
		# Target y coordinate converted to normal (0,0 = top left):
		yStimNormal = (trialDict['y_stim']*-1) + constants.yCen
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
		print obj
		print handle
		trialDict['xCoG'] = xStimPsycho + float(d[obj,"mask_control", handle][0])
		trialDict['yCoG'] = yStimNormal + float(d[obj,"mask_control", handle][1])
		trialDict['yCoGZero'] = 0 + float(d[obj,"mask_control", handle][1]) # TODO: correct?
		
		# With mask taken into account:
		trialDict['xCoGMask'] = xStimPsycho + float(d[obj,maskSide, handle][0])
		trialDict['yCoGMask'] = yStimNormal + float(d[obj,maskSide, handle][1]) # TODO: correct? verdere gevolgen?
		trialDict['yCoGMaskZero'] = 0 + float(d[obj,maskSide, handle][1])
			
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
		if trialDict["endXRaw2"] != '':
			trialDict["refixProb"] = 1
		else:
			trialDict["refixProb"] = 0
		
		# Determine the x coordinate of the target, 
		
		if self.exp == "004A":
			
			# For 004A the target was always centered on the vertical
			# meridian:
			trialDict['xStimNormal'] = constants.xCen
			
		if self.exp == "004B":
			
			# For 004B the x position was variable, and determined
			# in OpenSesame like so:
				# x_stim_corr = x_stim - float(xCoG)
			# where x_stim = 0 (center of the screen in PsychoPy coordinates)
	
			# Target x coordinate:
			trialDict['xStimNormal'] = constants.xCen - trialDict['xCoG']
		
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

		# Create all coordinates that are corrected for the CoG,
		# with and without mask taken into account:
		# Also, create coordinates that are normalized to the size of the
		# object:
		
		for i in range(1,saccCount+1):
			
			# X COORDINATES:
			
			# Correct for CoG without mask taken into account 
			# (all objects are treated as the control condition in the Mask manipulation):
			
			# The x coordinate was variable. 
			
			# So, the x landing position as if the center of the target was presented
			# at x center = 0, is relative to the actual x position of the target:
			#trialDict['endX%s'%i] = trialDict['endXRaw%s' % i] - trialDict['xStimNormal']
			#trialDict['startX%s'%i] = trialDict['startXRaw%s' % i] - trialDict['xStimNormal']
			trialDict['endX%s'%i] = trialDict['endXRaw%s' % i] - constants.xCen
			trialDict['startX%s'%i] = trialDict['startXRaw%s' % i] - constants.xCen
			
			
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
			
			# X COORDINATES:
			
			for var in ["endX%s" % i, "startX%s" % i, "endX%sCorr" % i, "endX%sCorrMask" % i, \
				"startX%sCorr" % i, "startX%sCorrMask" % i]:
				
				# Convert to visual degrees:
				trialDict["%sDegrees"%var] = trialDict[var]/constants.ratioPxDegr
				# Normalize:
				
				trialDict["%sNorm"%var] = trialDict[var]/trialDict["boxWidth"]
				
			# Make a new variable indicating whether the eyes landed towards the handle (positive)
			# or away from the handle (negative):
			for var in ["endX%sNorm" % i, "endX%sCorrNorm" % i]:
				
				if trialDict['handle_side'] == 'right':
					trialDict['%sToHandle'% var] = trialDict[var]
				if trialDict['handle_side'] == 'left':
					trialDict['%sToHandle' % var] = -trialDict[var]

				if trialDict['contrast_side'] == 'right':
					trialDict['%sToContrast'% var] = trialDict[var]
				if trialDict['contrast_side'] == '_left':
					trialDict['%sToContrast' % var] = -trialDict[var]

			# Y COORDINATES:
			
			for var in ['endY%s' % i, "startY%s" % i]:
				# Convert to visual degrees:
				trialDict["%sDegrees"%var] = trialDict[var]/constants.ratioPxDegr

				# Normalize is already done above.
				
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
			plt.suptitle("%s handle  = %s mask = %s"%(trialDict["object"],\
				trialDict["handle_side"], trialDict["mask_side"]))
			
			if addText:
				plt.subplot(2,1,1)
			# Retain screen size:
			plt.xlim(0, constants.screenW)
			plt.ylim(0, constants.screenH)
			
			# Plot thresholds: 
			plt.axhline(constants.yCen+\
				constants.minSaccSize, color = 'orange')
			plt.axhline(constants.yCen-\
				constants.minSaccSize, color = 'orange')
			
			# Plot width of the object:
			
			if self.exp == "004A":
				x = constants.xCen
			if self.exp == "004B":
				x = trialDict['xStimNormal']
			
			plt.axvline(x+(trialDict["boxWidth"]/2), color = 'green')
			plt.axvline(x-(trialDict["boxWidth"]/2), color = 'green')

			# Plot center:
			plt.axhline(constants.yCen, color = 'gray')
			plt.axvline(constants.xCen, color = 'gray')
			
			# Only plot CoG for the first experiment!
			if self.exp == "004A":
				# TODO Check whether this works as desired:
				#plt.axhline(constants.yCen+trialDict['yCoG'], color = 'red')
				plt.axhline(trialDict['yCoG'], color = 'red')
				plt.axvline(constants.xCen+trialDict['xCoG'], color = 'red')
			
			# Plot central coordinates of stimulus (i.e. the x,y position at which the stimulus
			# was centered):
			plt.axhline(trialDict['yStimNormal'], color = 'lightblue')
			plt.axvline(x, color = 'lightblue')
			
			# Plot height of the imaginary box:
			plt.axhline(trialDict['yStimNormal'] + trialDict['boxHeight']/2, color = 'lightblue')
			plt.axhline(trialDict['yStimNormal'] - trialDict['boxHeight']/2, color = 'lightblue')
			
			# Trick to deduce x and y coordiantes from list, see:
			# http://stackoverflow.com/questions/2282727/draw-points-using-matplotlib-pyplot-x1-y1-x2-y2
			
			plt.plot(*sum(rawSacc, []), marker = 'o', color='r')
			plt.plot(*sum(rawFix, []), marker = 'o', color = 'b')

			if addText:
				plt.subplot(2,1,2)
				# Debug text:
				text = "picture = %s handle side = %s \n\ncenter = %s \nxCoG = %s\nx target location: %s \n\nx coordinates first saccade:\nraw:%s\nas if target is presented at 0:%s\nnormalised: %s" % \
					(trialDict["object"], trialDict["handle_side"], constants.xCen, trialDict['xCoG'],\
					trialDict['xStimNormal'], trialDict["endXRaw1"], trialDict['endX1'], trialDict['endX1Norm'])
		
				plt.text(0.1, 0.1, text)
																					
			
			dstPp = os.path.join(dst, trialDict['file'])
			
			if not os.path.exists(dstPp):
				os.makedirs(dstPp)
				
			dstPlot = os.path.join(dstPp, '%s.png'%trialId)
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
				
				yFix = fixation['y'] - constants.yCen
				
				if abs(yFix) > constants.minSaccSize:
					
					global fixCount
					fixCount +=1 
					
					# Save duration:
					trialDict["durationFix%s" % fixCount] = fixation["duration"]
					
					# Save coordinates (relative to center):
					trialDict["xFix%s"% fixCount] = fixation["x"] - constants.xCen
					trialDict["yFix%s"% fixCount] = fixation["y"] - constants.yCen
				
				
					# Add to the temp list:
					rawFix.append([fixation['x'], fixation['y']])
		
		if self.waitForSacc:
			
			# If the line is not empty, the EyeLink algo detected smth as a saccade.
			sacc = self.toSaccade(l)
			
			if sacc != None:
				
				# Extra checks: 
				# The eyes must be somewhat at the top or bottom of 
				# the screen (i.e., not still at the center):
				
				yLanding = sacc['ey'] - constants.yCen
				
				if abs(yLanding) > constants.minSaccSize:
					
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
					trialDict['startXRaw%s'%saccCount] = sacc['sx']
					trialDict['endXRaw%s'%saccCount] = sacc['ex']
					
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
		
		# For the first experiment, verify the fixation checks:
		if self.exp == "004A":
			# Determine the duration of the first fixation check (on the central fix
			# dot):
			# MSG	31239346 fixation on fixdot check successfull
			if 'fixation' in l and 'fixdot' in l and 'successfull' in l:
				trialDict['durCheck1'] = l[1] - trialDict['timestampFixOnset']

			# Determine the success of the first fixation check (on the central 
			# fix dot):
			# MSG	2374487 fixation on fixdot check failed for 4000 samples in a row
			if 'fixation' in l and 'fixdot' in l and 'samples' in l and 'failed' in l:
				trialDict['checkFixDotFailed'] = True
			
			# Determine the success of the second fixation check (on the object):
			# MSG	31239765 fixation on object check successfull
			if 'fixation' in l and 'object' in l and 'successfull' in l:
				self.timestampSuccess = l[1]
				trialDict['durCheck2'] = l[1] - self.stimOnset

			# Determine the success of the second fixation check (on the object):
			# MSG	2383406 fixation on object check failed for 4000 samples in a row
			if 'fixation' in l and 'object' in l and 'failed' in l:
				trialDict['checkObjectFailed'] = True
			
		# Determine the reaction time by taking the onset of the stimulus 
		# (rather than the absolute trial onset) into account:
		# MSG	12966144 response given = 7
		if 'response' in l and 'given' in l:
			trialDict['timestampResponse'] = l[1]
			trialDict['rtFromStim'] = l[1] - self.stimOnset
			if self.exp == "004A":
				trialDict['rtFromSuccess'] = l[1] - self.timestampSuccess
			
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
	
		return None
	
def parseAsc(exp, driftCorr = False):
	
	"""
	Parses asc files into a data matrix for a given experiment
	
	Arguments:
	exp 		--- {"004A", "004B"}
	
	Default arguments:
	driftCorr	--- default = False
	"""
	
	# Indicate where folder containing data can be found:
	
	#global exp
	
	src = "/home/lotje/Documents/PhD Marseille/Studies/004 - Single-object experiment - Handle-orientation effect/%s/data/ASC/data" % exp
	
	if driftCorr:
		fName = "data_%s_WITH_drift_corr.csv" % exp
	else:
		fName = "data_%s_NO_drift_corr.csv" % exp
	
	if '--parse' in sys.argv:
		dm = MyReader(maxN=None, path = src, offlineDriftCorr = driftCorr, exp = exp).dataMatrix()		
		dm.save(fName)
	else:
		
		a = np.genfromtxt(fName, dtype=None, delimiter=",")
		dm = DataMatrix(a)
	
	return dm
	
	
if __name__ == "__main__":
	
	
	for exp in ["004A", "004B"]:
		
		parseAsc(exp = exp, driftCorr = True)
