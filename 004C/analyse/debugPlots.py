"""
DESCRIPTION:
Debug plots showing how we processed coordinates to get from raw coordinates to 
dv.
"""

import getDm
import parse
from exparser.Cache import cachedDataMatrix, cachedArray
from exparser.PivotMatrix import PivotMatrix
from matplotlib import pyplot as plt
from exparser.TangoPalette import *
import numpy as np
import sys
import selectDm
import constants
import os
import pylab
import fromPP
import constants
from exparser.TangoPalette import *
import random

dstPlots = "./debug plots"

def debugPlot(trialDm):
	
	"""
	"""
	
	fig = plt.figure(figsize = (5,20))
	
	exp = trialDm["expId"][0]
	
	name = trialDm["stim_name"][0]
	print name
	stimType = trialDm["stim_type"][0]
	vf = trialDm["visual_field"][0]
	flip = trialDm["flip"][0]
	angle = trialDm["realAngle"][0]
	#TODO: check this change!!!
	#xCog = trialDm["xCog"]/constants.scale
	xCog = trialDm["xCogScaled"]
	wStim = trialDm["wBoxScaled"][0]
	hStim = trialDm["hBoxScaled"][0]

	
	plt.suptitle("%s_%s" % (name, stimType))
	
	# Plot 1: Raw coordinates:
	plt.subplot(5,1,1)
	plt.title("%s\nreal a = %s" % (vf, angle))
	plt.xlim(0, constants.w)
	plt.ylim(0, constants.h)
	
	xStim = trialDm["xStim"][0]
	yStim = trialDm["yStim"][0]
	
	# Psychopy coordinates:
	_xStim, _yStim = fromPP.fromPP((xStim, yStim))
	
	fix = plt.Circle((constants.xCen, constants.yCen), 4, color = "black")
	stim = plt.Circle((_xStim, _yStim), 10, color = "red")
	
	plt.axvline(constants.xCen, linestyle = "--", color = "gray")
	fig.gca().add_artist(stim)
	fig.gca().add_artist(fix)
	
	saccCount = int(trialDm["saccCount"][0])
	
	for sacc in range(1, saccCount +1):
		
		# HACK:
		if sacc > 5:
			continue
		
		x = trialDm["sacc%s_ex" % sacc][0]
		y = trialDm["sacc%s_ey" % sacc][0]
		
		lp = plt.Circle((x,y), 6, color = "blue")
		fig.gca().add_artist(lp)

	# Plot 2: Normalized on center of the screen:
	plt.subplot(5,1,2)
	plt.xlim(-constants.xCen, constants.xCen)
	plt.ylim(-constants.yCen, constants.yCen)
	plt.axvline(0, linestyle = "--", color = "gray")
	fix = plt.Circle((0, 0), 4, color = "black")
	stim = plt.Circle((xStim, -abs(yStim)), 10, color = "red")
	
	fig.gca().add_artist(stim)
	fig.gca().add_artist(fix)
	
	saccCount = int(trialDm["saccCount"][0])
	
	for sacc in range(1, saccCount +1):
		
		if sacc > 5:
			continue
		
		x = trialDm["xNormOnCenter%s" % sacc][0]
		y = trialDm["yNormOnCenter%s" % sacc][0]
		
		lp = plt.Circle((x,y), 6, color = "blue")
		fig.gca().add_artist(lp)

	# Plot 3: Rotated LP:
	plt.subplot(5,1,3)
	
	plt.xlim(-constants.xCen, constants.xCen)
	plt.ylim(-constants.yCen-2, constants.yCen)
	plt.axvline(0, linestyle = "--", color = "gray")
	fix = plt.Circle((0, 0), 4, color = "black")
	stim = plt.Circle((-xCog, -yStim), 10, color = "red")
	bbox = plt.Rectangle((-xCog - wStim/2, (-abs(yStim))-hStim/2), wStim, hStim, color = "yellow")

	fig.gca().add_artist(bbox)
	fig.gca().add_artist(stim)
	fig.gca().add_artist(fix)
	
	saccCount = int(trialDm["saccCount"][0])
	
	for sacc in range(1, saccCount +1):
		
		if sacc > 5:
			continue
		
		x = trialDm["xRot%s" % sacc][0]
		y = trialDm["yRot%s" % sacc][0]
		
		lp = plt.Circle((x,y), 6, color = "blue")
		fig.gca().add_artist(lp)


	# Plot 4: Normalize on handle side:
	plt.subplot(5,1,4)

	plt.title("flip = %s" % flip)
	plt.xlim(-constants.xCen, constants.xCen)
	plt.ylim(-constants.yCen, constants.yCen)
	plt.axvline(0, linestyle = "--", color = "gray")
	fix = plt.Circle((0, 0), 4, color = "black")
	# TODO: check stim!!!
	if flip == "left":
		xStimFlipped = xCog
	else:
		xStimFlipped = -xCog
	stim = plt.Circle((xStimFlipped, -abs(yStim)), 10, color = "red")
	
	bbox = plt.Rectangle((xStimFlipped - wStim/2, (-abs(yStim))-hStim/2), wStim, hStim, color = "yellow")
	fig.gca().add_artist(bbox)
	fig.gca().add_artist(stim)
	fig.gca().add_artist(fix)
	
	saccCount = int(trialDm["saccCount"][0])
	
	for sacc in range(1, saccCount +1):
		
		if sacc > 5:
			continue
		
		x = trialDm["xFlipped%s" % sacc][0]
		y = trialDm["yFlipped%s" % sacc][0]
		
		lp = plt.Circle((x,y), 6, color = "blue")
		fig.gca().add_artist(lp)
	
	# Plot 5: Normalize on object width:
	plt.subplot(5,1,5)
	plt.axvline(0, linestyle = "--", color = "gray", label = "cog")
	plt.axhline(0, linestyle = "--", color = "gray")
	plt.axvline(xStimFlipped/wStim, linestyle = "--", color = "red", label = "abs")
	bbox = plt.Rectangle((-.5, -.5), 1, 1, color = "yellow")
	fig.gca().add_artist(bbox)
	plt.xlim(-2,2)
	plt.ylim(-2,2)
	
	for sacc in range(1, saccCount +1):
		
		if sacc > 5:
			continue
		
		x = trialDm["xNorm%s" % sacc][0]
		y = trialDm["yNorm%s" % sacc][0]
		
		lp = plt.Circle((x,y), .1, color = "blue", fill=False)
		fig.gca().add_artist(lp)
		
	expPath = os.path.join(dstPlots, exp)
	if not os.path.exists(expPath):
		os.makedirs(expPath)
		
	figPath = os.path.join(expPath, "%s_%s.png" % (trialDm["file"][0], str(trialDm["trialId"][0])))
	plt.savefig(figPath)
	#plt.show()
	#sys.exit()
	plt.clf()
	pylab.close()
	
if __name__ == "__main__":
	
	for exp in ["004A", "004B", "004C"]:

		dm = getDm.getDm(exp, cacheId = "%s_final" % exp)
		
		for i in dm.range():
			# Save 1 in 40 trials:
			if i % 40 != 39:
				continue
			
			trialDm = dm[i]
			debugPlot(trialDm)
