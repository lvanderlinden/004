#!/usr/bin/env python
# Filename: simulationDM.py

"""
DESCRIPTION:
Creates dm that is comparable to the 'real' dm's used for
the analyses of experiment 1 and 2.
"""

# Import Python modules:
import sys
import numpy as np
import os
os.chdir('/home/lotje/Documents/PhD Marseille/Studies/004 - Single-object experiment - Handle-orientation effect/analysis 004')

# Import own modules:
from exparser.CsvReader import CsvReader
import drawBox
import constants

# Constants:
fName = "/home/lotje/Documents/PhD Marseille/Studies/004 - Single-object experiment - Handle-orientation effect/analysis 004/simulation/data.csv"

heavyHandle = ["chisel", "screwdriver", "sharpeningsteel"]

printSum = False

if __name__ == "__main__":
	
	# Get dictionary containing w and h of imaginary boxes around the stimuli:
	boxDict = drawBox.boxDict()

	# OpenSesame output file is opened as dm. The fixation values will 
	# be added to this dm.
	dm = CsvReader(fName, delimiter = ",").dataMatrix()
	
	# The varialbe 'corrDirection' is determined in ascParser,
	# and doesn't exist for the simulation data.
	# Therefore we add it manually:
	dm = dm.addField("corrDirection", dtype = str)
	
	# Make new column headers:
	for sacc in range(1,4):
		
		# Landing position:
		dm = dm.addField('endX%s' % sacc, dtype=str)
		dm = dm.addField('endY%s' % sacc, dtype = str)
		
		# Normalised landing position:
		dm = dm.addField('endX%sNorm' % sacc, dtype = str)
		dm = dm.addField('endY%sNorm' % sacc, dtype = str)
		
		# Landing position where positive indicates ToHandle"
		dm = dm.addField('endX%sNormToHandle' % sacc, dtype = str)
		
		# Timestamps for each fixation
		dm = dm.addField('saccLat%s' % sacc, dtype=str)

		# IMPORTANT TO NOTE:
		# Give the landing positions the starting value '', such that 
		# the same criteria can be applied to the real and the simulated
		# saccades. In the real dm's, the value '' indicates that a certain
		# landing position was not detected (e.g. endX2 does not exist if
		# participants made only one saccade). The same criterion should
		# be applied for the simulated dm, because sometimes participants
		# looked four times on the fix dot, and one time at the object, etc.
		# These landing positions should not get the value 0!!
		# This is done automatically by making the new variables (see above)
		# strings. Every empty cell gets the value "".		
		
		
	# Walk through all cycles in the dm, and open the small simulation dm
	# corresponding to the current trial:	
	
	for i in dm.range():
		
		trial = dm[i]
		trialNr = dm['count_trial_sequence'][i]
		handleSide = trial['handle_side'][0]
		pictName = trial['pict'][0]
		boxWidth, boxHeight = boxDict[pictName]
		stim = trial['object'][0]
		
		# Add variables from simulation to dm:
		print 'Trial %d (%s)' % (trialNr, handleSide)
		
		# Open the small dm:
		sim = CsvReader('simulation/simulation/csv/%.4d.csv' \
			% trialNr).dataMatrix()	
		
		# Add corrDirection:
		if stim in heavyHandle:
			dm["corrDirection"][i] = "correction towardsHandle"
		else:
			dm["corrDirection"][i] = "correction awayHandle"
			
		fixNr = 1	
		
		for fix in sim:
			t = fix['t'][0]
			dx = fix['x'][0]-constants.xCen
			dy = fix['y'][0]-constants.yCen
			
			xNorm = (dx/boxWidth)*constants.rescale
			yNorm = (dy/boxHeight)*constants.rescale
			
			if handleSide == 'left':
				xToHandle = xNorm * -1
			else:
				xToHandle = xNorm
			
			
			# If saccade is large enough:
			if abs(dy) > constants.minSaccSize:
				
				print 'trial = ', trialNr
				print 'sacc = ', fixNr
				print 'dev = ', dy
				print 'th = ', constants.minSaccSize
				print 'y coord = ', fix['y']
				print				
				#raw_input()  
				
				# Save all the variables to the dm:
				
				# TODO: compare with ascParser
				dm['saccLat%s' % fixNr][i] = t
				dm['endX%s' % fixNr][i] = dx
				dm['endY%s' % fixNr][i] = dy
				dm['endX%sNorm' % fixNr][i] = xNorm
				dm['endY%sNorm' % fixNr][i] = yNorm
				dm['endX%sNormToHandle' % fixNr][i] = xToHandle

				fixNr += 1

#			if int(xNorm) == 0:
#				if fixNr == 2:
#					if abs(dy) > constants.minSaccSize:
#						print fix['t']
#						print dy
#						raw_input()

			if fixNr > 3:
				break
			
	# Save the dm containing the simulation data:
	dm.save('dm_004C_simulation.csv')

	if printSum:
		print '\nSummary:\n'
		for gap in (None, 'overlap', 'zero'):	
			print 'Gap: %s' % gap
			if gap == None:
				_dm = dm
			else:
				_dm = dm.select('gap == "%s"' % gap, verbose=False)	
			fix1 = _dm['endX1NormToHandle'].mean()
			fix2 = _dm['endX2NormToHandle'].mean()
			fix3 = _dm['endX3NormToHandle'].mean()
			t1 = _dm['saccLat1'].mean()
			t2 = _dm['saccLat2'].mean()
			t3 = _dm['saccLat3'].mean()
			print '%.2f (%.2f)\t%.2f (%.2f)\t%.2f (%.2f)' % (fix1, t1, fix2, t2, fix3, \
				t3)
