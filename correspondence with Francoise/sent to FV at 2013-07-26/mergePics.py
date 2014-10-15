#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Filename: mergePics.py

"""
DESCRIPTION:

TODO:
xlabels and y labels?
"""
from PIL import Image
from matplotlib import pyplot as plt

from matplotlib.backends.backend_pdf import PdfPages
pp = PdfPages('Timecourses.pdf')
	

def mergePics(lFigPaths, nRows = None, nCols = None, supTitle = None, lTitles = None, \
	figSize = None, hSpace = 0, wSpace = 0, fontFamily = "ubuntu", fontSize = 16):
	
	"""
	lFigPaths 	--- list of to-be-merged pictures
	nRows
	nCols
	
	Keyword arguments:
	supTitle
	lTitles -- list of titles for subplots
	"""
	
	plt.rc("font", family=fontFamily)
	plt.rc("font", size=fontSize)
	
	if lTitles == None:
		lTitles = [""]*len(lFigs)
	
	if supTitle == None:
		supTitle = ""
	
	fig = plt.figure(figsize = figSize)
	plt.suptitle(supTitle)
	plt.subplots_adjust(hspace = hSpace, wspace = wSpace)
	
	if nRows == None and nCols == None:
		nRows = 1
		nCols = len(lFigPaths)
	
	plotNr = 0
	titleNr = 0
	
	for f in lFigPaths:
		plotNr +=1
		plt.subplot(1,3,plotNr)
		plt.title(lTitles[titleNr])
		img = Image.open(f)
		plt.imshow(img)
		plt.xticks([])
		plt.yticks([])
		titleNr +=1
		
	return fig
	
if __name__ == "__main__":
	
	
	# ANOVA's with only Landing position as a function of handle side. 
	#lFigs = ["./Landing position as a function of handle_side - saccNr = 1.png", \
		#"./Landing position as a function of handle_side - saccNr = 2.png",\
			#"./Landing position as a function of handle_side - saccNr = 3.png"]
	
	#supTitle = "Landing positions as a function of handle side (contrast manipulation excluded)"
	#lTitles = ["saccade 1", "saccade 2", "saccade 3"]
	#fig = mergePics(lFigs, lTitles = lTitles, supTitle = supTitle, fontSize = 10)
	#plt.savefig("Figure1.png")
	
	
	# Time courses:
	#for direction in ["TO HANDLE", "TO CONTRAST"]:
		
		#if direction == "TO HANDLE":
			#var = "ToHandle"
		#if direction == "TO CONTRAST":
			#var = "ToContrast"
			
		#lFigs = ["./Landing (uncorrected) %s as a function of binned sacc lats exp 004A cousineau = True trim = False.png" % var, \
			#"./Landing (corrected) %s as a function of binned sacc lats exp 004A cousineau = True trim = False.png" % var, \
				#"./Landing (uncorrected) %s as a function of binned sacc lats exp 004B cousineau = True trim = False.png" % var]
	
		#supTitle = "Landing positions towards %s (positive = towards) as a function of binned latency" % direction
		#lTitles = ["exp 1 uncorrected", "exp 1 corrrected", "exp 2"]
	
		#fig = mergePics(lFigs, lTitles = lTitles, supTitle = supTitle, fontSize = 10)
		#plt.savefig("%s.png" % direction)
	
	# Two way ANOVA's effect Handle side and Gap
	lFigs = ["./Interaction handle and gap on endX1Norm exp 004A.png", \
		"./Interaction handle and gap on endX1CorrNorm exp 004A.png",\
			"./Interaction handle and gap on endX1Norm exp 004B.png"]
	
	supTitle = "Landing positions as a function of Handle Side and Gap (contrast manipulation excluded)"
	lTitles = ["saccade 1", "saccade 2", "saccade 3"]
	fig = mergePics(lFigs, lTitles = lTitles, supTitle = supTitle, fontSize = 10)
	plt.savefig("Figure4.png")