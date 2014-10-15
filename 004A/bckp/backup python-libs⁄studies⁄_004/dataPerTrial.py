#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import math
from PIL import Image, ImageDraw
import numpy as np
from scipy.stats import nanmean, nanmedian
from matplotlib import pyplot as plt
from exparser.EyelinkAscFolderReader import EyelinkAscFolderReader
from exparser.DataMatrix import DataMatrix
from exparser.PivotMatrix import PivotMatrix
from PIL import Image, ImageDraw



src = "/home/lotje/Documents/PhD Marseille/Studies/004 - One-object experiment - Orienation effect/Experiment"
dst = "/home/lotje/Documents/PhD Marseille/Studies/004 - One-object experiment - Orienation effect/Analysis/Plots/trialPlots"
ext = ".jpg"

class MyReader(EyelinkAscFolderReader):

	def initTrial(self, trialDict):

		# Open the image, see
		# http://www.pythonware.com/library/pil/handbook/image.htm
		# http://www.pythonware.com/library/pil/handbook/imagedraw.htm
		self.im = Image.new('RGB', (1024,768))			
		self.dr = ImageDraw.Draw(self.im)
		self.fixNr = 1
		

	def finishTrial(self, trialDict):

		pictName = trialDict["picture_name"]+ext

		# Draw a bitmap (another image) onto the image
		stimPath = os.path.join(src, pictName)
		stimIm = Image.open(stimPath)
		self.im.paste(stimIm, (100,100))
		
		pictName = "%s-%.4d.png" % (trialDict['file'], \
			trialDict['trialId'])
		
		newPath = os.path.join(dst, pictName)

		# Save the image
		self.im.save(newPath)

	def parseLine(self, trialDict, l):

		# Draw saccades as green lines
		sacc = self.toSaccade(l)
		if sacc != None:
			self.dr.line( (sacc['sx'], sacc['sy'], sacc['ex'], sacc['ey']), \
				fill='green')
				
		# Draw fixations as blue annotated circles
		fix = self.toFixation(l)
		if fix != None:
			self.dr.ellipse( (fix['x']-5, fix['y']-5, fix['x']+5, fix['y']+5), \
				fill='blue')
			s = '%d (%d)' % (self.fixNr, fix['duration'])
			self.dr.text( (fix['x'], fix['y']), s, fill='blue')
			self.fixNr += 1

dm = MyReader(maxTrialId=1).dataMatrix()
