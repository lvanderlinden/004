#!/usr/bin/env python
# Filename: simulationDM.py

"""
DESCRIPTION:
Creates dm that is comparable to the 'real' dm's used for
the analyses of experiment 1 and 2.
"""

# Import modules:
from exparser.CsvReader import CsvReader

# Constants:

xc = 1024/2
yc = 768/2

ythr = 100

if __name__ == "__main__":
	
	dm = CsvReader('data.csv').dataMatrix()
	dm = dm.select('mask_side == "control"')
	dm = dm.select('symm == "asymm"')
	#dm = dm.select('gap == "overlap"')
	#dm = dm.select('handle_side == "right"')

	#dm = dm.select('object == "screwdriver"')

	# X coordinates, where positive values indicate a deviation towards the handle
	dm = dm.addField('refix1', dtype=float)
	dm = dm.addField('refix2', dtype=float)
	dm = dm.addField('refix3', dtype=float)

	# Timestamps for each fixation
	dm = dm.addField('tfix1', dtype=float)
	dm = dm.addField('tfix2', dtype=float)
	dm = dm.addField('tfix3', dtype=float)

	for i in dm.range():
		
		trial = dm[i]
		trialNr = dm['count_trial_sequence'][i]
		handleSide = trial['handle_side'][0]
		print 'Trial %d (%s)' % (trialNr, handleSide)
		sim = CsvReader('simulation/csv/%.4d.csv' % trialNr).dataMatrix()	
		
		fixNr = 1	
		for fix in sim:
			t = fix['t'][0]
			dx = fix['x'][0]-xc
			dy = fix['y'][0]-yc
			if abs(dy) > ythr:			
				if handleSide == 'left':
					dx *= -1.			
				print fixNr, dx
				dm['refix%d' % fixNr][i] = dx
				dm['tfix%d' % fixNr][i] = t
				fixNr += 1
			if fixNr > 3:
				break

	print '\nSummary:\n'
	for gap in (None, 'overlap', 'zero'):	
		print 'Gap: %s' % gap
		if gap == None:
			_dm = dm
		else:
			_dm = dm.select('gap == "%s"' % gap, verbose=False)	
		fix1 = _dm['refix1'].mean()
		fix2 = _dm['refix2'].mean()
		fix3 = _dm['refix3'].mean()
		t1 = _dm['tfix1'].mean()
		t2 = _dm['tfix2'].mean()
		t3 = _dm['tfix3'].mean()
		print '%.2f (%.2f)\t%.2f (%.2f)\t%.2f (%.2f)' % (fix1, t1, fix2, t2, fix3, \
			t3)
	dm.save('dm_004C_simulation.csv')