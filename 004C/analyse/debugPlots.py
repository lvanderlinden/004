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

def plotSaccades(trialDm, fig, xSaccId, ySaccId):
	
	"""
	Plots all detected saccades from a given trial.
	
	Arguments:
	trialDm		--- dm containing info from 1 trial
	fig 		--- pyplot figure instance
	xSaccId		--- string indicating the column header for the x coordinate 
					of the saccade.
					string formatting is used to indicate the saccade count.
	ySaccId		--- string indicating the column header for the y coordinate 
					of the saccade.
					string formatting is used to indicate the saccade count.
	"""

	# Plot raw landing positions:
	if xSaccId == "xNorm%s":
		r = .1
	else:
		r = 6
	
	
	saccCount = int(trialDm["saccCount"][0])
	for sacc in range(1, saccCount +1):
		
		# HACK:
		if sacc > 5:
			continue

		x = trialDm[xSaccId % sacc][0]
		y = trialDm[ySaccId % sacc][0]
		
		lp = plt.Circle((x,y), r, color = "blue")
		fig.gca().add_artist(lp)


def plotRaw(trialDm, fig):
	
	"""
	Plots raw landing positions.
	The only conversion that is carried out, is that stim coordinates
	are converted from PsychoPy coordinates (origin = center, up = positive)
	are converted to 'normal' screen coordinates (origin = top left).
	
	Arguments:
	trialDm		--- dm containing info from 1 trial
	fig 		--- pyplot figure instance
	"""
	
	# Limits axes:
	plt.xlim(0, constants.w)
	plt.ylim(0, constants.h)
	
	# From Psychopy coordinates to normal coordinates:
	_xStim, _yStim = fromPP.fromPP((trialDm["xStim"][0], trialDm["yStim"][0]))
	
	# Draw fix and stim:
	fix = plt.Circle((constants.xCen, constants.yCen), 4, color = "black")
	stim = plt.Circle((_xStim, _yStim), 10, color = "red")
	fig.gca().add_artist(stim)
	fig.gca().add_artist(fix)
	
	# Indicate vertical meridian of the screen:
	plt.axvline(constants.xCen, linestyle = "--", color = "gray")
	
	# Plot saccades:
	plotSaccades(trialDm, fig, "sacc%s_ex", "sacc%s_ey")
	
def plotNormOnCenter(trialDm,fig):
	
	"""
	Plots coordinates normalized on screen center, such that origin is 
	screen center and up = negative.
	
	Arguments:
	trialDm		--- dm containing info from 1 trial
	fig 		--- pyplot figure instance
	"""
	
	# Limits axes:
	plt.xlim(-constants.xCen, constants.xCen)
	plt.ylim(-constants.yCen, constants.yCen)
	
	# Fix and stim:
	fix = plt.Circle((0, 0), 4, color = "black")
	stim = plt.Circle((trialDm["xStim"][0], -(trialDm["yStim"][0])), 10, color = "red")
	fig.gca().add_artist(stim)
	fig.gca().add_artist(fix)

	# Vertical meridian:
	plt.axvline(0, linestyle = "--", color = "gray")

	# Sacc coordinates normalized on screen center:
	plotSaccades(trialDm, fig, "xNormOnCenter%s", "yNormOnCenter%s")
	
def plotRot(trialDm, fig):
	
	"""
	Plot rotated landing positions.
	Rotated is such that all landing positions are normalized on vertical 
	meridian in UVF.
	
	Arguments:
	trialDm		--- dm containing info from 1 trial
	fig 		--- pyplot figure instance
	"""
	
	# Limits axes:
	plt.xlim(-constants.xCen, constants.xCen)
	plt.ylim(-constants.yCen-2, constants.yCen)
	
	# TODO: not correct!!!
	# Bbox around stimulus. Note that we couldn't plot this before,
	# because of the rotation.
	wStim = trialDm["wBoxScaled"][0]
	hStim = trialDm["hBoxScaled"][0]
	
	if trialDm["expId"][0] != "004A":
		left = -trialDm["xCogScaled"][0] - wStim/2
	else:
		left = 0-wStim/2
	
	bbox = plt.Rectangle((left, \
		(-abs(trialDm["yStim"][0]))-hStim/2), wStim, hStim, color = "yellow")
	fig.gca().add_artist(bbox)

	# Fix and stim.
	fix = plt.Circle((0, 0), 4, color = "black")
	if trialDm["expId"][0] != "004A":
		stim = plt.Circle((-trialDm["xCogScaled"][0], -abs(trialDm["yStim"][0])), 10, color = "red")
	else:
		stim = plt.Circle((0, -abs(trialDm["yStim"][0])), 10, color = "red")
	fig.gca().add_artist(stim)
	fig.gca().add_artist(fix)

	# Vertical meridian:
	plt.axvline(0, linestyle = "--", color = "gray")

	# Plot saccades:
	plotSaccades(trialDm, fig, "xRot%s", "yRot%s")

def plotFlip(trialDm, fig):
	
	"""
	Plot flipped landing positions.
	FLipped such that all landing positions are normalized on handle side
	= right.
	TODO: LVF?
	
	Arguments:
	trialDm		--- dm containing info from 1 trial
	fig 		--- pyplot figure instance
	"""
	
	# Limits axes:
	
	plt.xlim(-constants.xCen, constants.xCen)
	plt.ylim(-constants.yCen, constants.yCen)

	# Vertical meridian:
	plt.axvline(0, linestyle = "--", color = "gray")
	
	# Stim, fix and bbox:
	fix = plt.Circle((0, 0), 4, color = "black")
	
	if trialDm["expId"][0] != "004A":
		if trialDm["flip"] == "left":
			xStimFlipped = trialDm["xCogScaled"][0]
		else:
			xStimFlipped = -trialDm["xCogScaled"][0]
	else:
		xStimFlipped = 0
	stim = plt.Circle((xStimFlipped, -abs(trialDm["yStim"][0])), 10, color = "red")

	
	wStim = trialDm["wBoxScaled"][0]
	hStim = trialDm["hBoxScaled"][0]
	
	if trialDm["expId"][0] != "004A":
		left = xStimFlipped - wStim/2
	else:
		left = 0 - wStim/2
	
	bbox = plt.Rectangle((left, (-abs(trialDm["yStim"][0]))-hStim/2), wStim, hStim, color = "yellow")
	fig.gca().add_artist(bbox)
	fig.gca().add_artist(stim)
	fig.gca().add_artist(fix)
	
	# Plot flipped saccades:
	plotSaccades(trialDm, fig, "xFlipped%s", "yFlipped%s")
	
def plotFinal(trialDm, fig):
	
	"""
	Plot final normalized LPs.
	Normalized such that all landing positions are normalized on stimulus
	width.
	
	Arguments:
	trialDm		--- dm containing info from 1 trial
	fig 		--- pyplot figure instance
	"""
	

	# Absolute center:
	if trialDm["flip"][0] == "left":
		xStimFlipped = trialDm["xCogScaled"][0]
	elif trialDm["flip"][0] == "right":
		xStimFlipped = -trialDm["xCogScaled"][0]
	else:
		raise Exception("flip should have the value left or right")
	
	# Cog and absolute center:
	if trialDm["expId"][0] != "004A":
		cog = 0
		absCenter = xStimFlipped/trialDm["wBoxScaled"][0]
	else:
		cog = trialDm["xCogScaled"][0]/trialDm["wBoxScaled"][0]
		absCenter = 0

	plt.axvline(cog, linestyle = "--", color = "green", label = "cog")
	plt.axvline(absCenter, linestyle = "--", color = "orange", label = "abs")

	
	plt.legend(frameon=False, loc = 'best')

	# Bbox:
	if trialDm["expId"][0] != "004A":
		left = xStimFlipped/trialDm["wBoxScaled"]-.5
	else:
		left = -.5
	bbox = plt.Rectangle((left, -.5), 1, 1, color = "yellow")
	fig.gca().add_artist(bbox)
	plt.xlim(-2,2)
	plt.ylim(-2,2)
	
	# Final normalized LPs:
	plotSaccades(trialDm, fig, "xNorm%s", "yNorm%s")

def debugPlot(trialDm):
	
	"""
	TODO: check!!!
	"""
	
	# Init figure:
	fig = plt.figure(figsize = (5,20))
	
	name = trialDm["stim_name"][0]
	stimType = trialDm["stim_type"][0]
	plt.suptitle("%s_%s" % (name, stimType))

	# Plot 1: Raw coordinates:
	plt.subplot(5,1,1)
	vf = trialDm["visual_field"][0]
	angle = trialDm["realAngle"][0]
	plt.title("%s\nreal a = %s" % (vf, angle))
	plotRaw(trialDm, fig)

	# Plot 2: Normalized on center of the screen:
	plt.subplot(5,1,2)
	plt.title("norm on screen center")
	plotNormOnCenter(trialDm, fig)
	
	# Plot 3: Rotated LP:
	plt.subplot(5,1,3)
	plt.title("rotate:\n norm on vertical meridian UVF")
	plotRot(trialDm, fig)

	# Plot 4: Normalize on handle side:
	plt.subplot(5,1,4)
	plt.title("flip = %s" % trialDm["flip"][0])
	plotFlip(trialDm, fig)
	
	# Plot 5: Normalize on object width:
	plt.subplot(5,1,5)
	plt.title("Final DV")
	plotFinal(trialDm, fig)
	
	# Save:
	exp = trialDm["expId"][0]
	expPath = os.path.join(dstPlots, exp)
	if not os.path.exists(expPath):
		os.makedirs(expPath)
		
	figPath = os.path.join(expPath, "%s_%s.png" % (trialDm["file"][0], \
		str(trialDm["trialId"][0])))
	plt.savefig(figPath)
	#plt.show()
	
	plt.clf()
	pylab.close()
	#raw_input()
if __name__ == "__main__":
	
	for exp in ["004A", "004B", "004C"]:
		
		if exp != "004B":
			continue

		dm = getDm.getDm(exp, cacheId = "%s_final" % exp)
		
		for i in dm.range():
			if dm["stim_name"][i] != "screwdriver":
				continue
			if dm["stim_type"][i] != "object":
				continue
			if dm["mask_side"][i] != "control":
				continue

			# Save 1 in 40 trials:
			#if i % 100 != 99:
			#	continue
			
			trialDm = dm[i]
			debugPlot(trialDm)
