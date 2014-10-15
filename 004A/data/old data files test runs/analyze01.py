#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import numpy as np
import scipy
from matplotlib import cm
from matplotlib import pyplot as plt
import sys
from exparser.EyelinkAscFolderReader import EyelinkAscFolderReader
from exparser.DataMatrix import DataMatrix
from exparser.PivotMatrix import PivotMatrix

trialId = 0


def getDM():
	class MyReader(EyelinkAscFolderReader):

		def initTrial(self, trialDict):

			global trialId
			self.waitForSacc = False
			self.saccOnset = None
			trialDict['endX'] = -1000
			trialId += 1
			
		def finishTrial(self, trialDict):

			if self.saccOnset == None:
				trialDict['saccLat'] = -1
			else:
				trialDict['saccLat'] = self.saccOnset - self.stimOnset
			
			l = trialDict['picture_name'].split('_')
			trialDict['symm'] = l[0]
			
			# MSG	14329200 var cond ('handle_left', 'mask_left')
			del trialDict['cond']

		def parseLine(self, trialDict, l):
			
			# MSG	14327176 display stimulus
			if len(l) > 3 and l[2] == 'display' and l[3] == 'stimulus':
				self.waitForSacc = True
				self.stimOnset = l[1]
				
			if self.waitForSacc:
				sacc = self.toSaccade(l)
				if sacc != None and sacc['size'] > 100:
					self.saccOnset = sacc['sTime']
					trialDict['endX'] = sacc['ex'] - 512
					self.waitForSacc = False
					
		def startTrial(self, l):

			# MSG	14320597 start_trial
			global trialId
			if len(l) > 2 and l[0] == 'MSG' and l[2] == self.startTrialKey:
				return trialId
			return None
	
						
	if '--parse' in sys.argv:
		dm = MyReader().dataMatrix()
		dm.save('data.csv')
	else:
		m = np.genfromtxt('data.csv', dtype=None, delimiter=',')
		dm = DataMatrix(m)
	
	return dm

def select(dm):
	
	"""
	"""
	
	dm = dm.select('saccLat > 0')
	#dm = dm.select('saccLat > 50')
	dm = dm.select('saccLat < 500')
	dm = dm.select('saccLat != -1000')
	#dm = dm.select('symm == "asymm"')
	#dm = dm.select('accuracy == 1')
	dm = dm.select('catch_trial == "no"')
	return dm

def gapDistr(dm,nBin =50):
	
	
	"""
	"""
	
	dmGap = dm.select('gap == "zero"')
	dmNoGap = dm.select('gap == "overlap"')
	dmColChange = dmNoGap.select('large_fix_col == "change"')
	dmColSame = dmNoGap.select('large_fix_col == "no_change"')
	
	fig = plt.figure()

	plt.subplot(311)
	plt.title("gap zero")
	plt.hist(dmGap['saccLat'], color='blue', bins=nBin)#, histtype='step')
	plt.xlim(0,500)
	plt.xticks([])
	plt.ylabel("frequency")

	plt.subplot(312)
	plt.title("gap overlap, fixation changed size but not color")
	plt.hist(dmColSame['saccLat'], color = "green", bins = nBin)#, histtype = 'step')
	plt.xlim(0,500)
	plt.xticks([])
	plt.ylabel("frequency")

	plt.subplot(313)
	plt.title("gap overlap, fixation changed size AND color")
	plt.hist(dmColChange['saccLat'], color='red', bins=nBin)#, histtype='step')
	plt.ylabel("frequency")
	plt.xlim(0,500)
	plt.xlabel("latency")
	#plt.legend(["gap zero", "same color", "different color"])
	#plt.show()

def latBins(dm, nBin = 8):
	
	"""
	"""
	
	dm = dm.addField('saccLatBin')
	dm = dm.calcPerc('saccLat', 'saccLatBin', keys=['file'], nBin=nBin)
	
	return dm

def jitterBins(dm, nBin = 8):
	
	dm = dm.addField('jitterBin')
	dm = dm.calcPerc('jitter_dur', 'jitterBin', keys=['file'], nBin=nBin)
	
	return dm


def lumBinAn(dm, nBin = 8):
	
	"""
	"""
	
	dm = latBins(dm)
	
	pm = PivotMatrix(dm, ['mask_side', 'saccLatBin'], ['file'], dv='endX', colsWithin=False)
	pm._print()
	xLabels = range(1,nBin+1)
	xLabel = "binned latencies"
	lLabel = "contrast manipulation"
	lLabels = ["control", "more contrast right", "more contrast left"]
	#lLabels = None
	yLabel = "landing position - negative = left, positive = right"
	pm.linePlot(show=True,xLabels = xLabels, xLabel = xLabel, yLabel = yLabel, legendTitle = lLabel, lLabels = lLabels)
	plt.axhline(0, color = "grey", linestyle = "--")
	#plt.savefig("contrast_effect.jpg")

def simon(dm):
	
	"""
	"""
	

	pm = PivotMatrix(dm, ['response_hand', 'mask_side'], ['file'], dv='RT', colsWithin=False)
	pm._print()
	pm.barPlot(show=True)
	plt.title("simon effect")

def regrLatRT(dm):
	
	x = dm["saccLat"]
	y = dm["RT"]
	
	fit = scipy.polyfit(x,y,1)
	fit_fn = scipy.poly1d(fit)
	
	slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(x,y)
	print "slope = %s, intercept = %s, R = %s, p = %s, SE = %s" % (slope, intercept, r_value, p_value, std_err)

	plt.plot(x,y, 'yo', x, fit_fn(x), '--k')
	plt.xlabel("saccLat")
	plt.ylabel("RT")
	plt.show()


def gapRegr(dm):
	
	dmGap = dm.select('gap == "zero"')
	dmNoGap = dm.select('gap == "overlap"')
	dmFixGray = dmNoGap.select('large_fix_col == "change"')
	dmFixBlack = dmNoGap.select('large_fix_col == "no_change"')


	# Fixation did not change color:
	x = dmFixBlack['large_fix_size']
	y = dmFixBlack['saccLat']

	fit = scipy.polyfit(x,y,1)
	fit_fn = scipy.poly1d(fit) # fit_fn is now a function which takes in x and returns an estimate for y
	
	print "fixation did not change color"
	slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(x,y)
	print "slope = %s, intercept = %s, R = %s, p = %s, SE = %s" % (slope, intercept, r_value, p_value, std_err)

	plt.plot(x,y, 'yo', x, fit_fn(x), '--k', color = "red")

	# Fixation changed color:
	x = dmFixGray['large_fix_size']
	y = dmFixGray['saccLat']

	fit = scipy.polyfit(x,y,1)
	fit_fn = scipy.poly1d(fit) # fit_fn is now a function which takes in x and returns an estimate for y
	
	print "fixation changed color"
	slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(x,y)
	print slope, intercept, r_value, p_value, std_err

	plt.plot(x,y, 'yo', x, fit_fn(x), '--k', color = "blue")
	plt.ylabel("saccade latencies")
	plt.xlabel("changed fixation size")
	plt.show()



	#plt.show()

def vfDiff(dm,dv = "RT"):

	pm = PivotMatrix(dm, ['visual_field'],['file'], dv = dv)
	pm.barPlot(show=True)
	plt.ylabel(dv)
	plt.title("visual field difference")
	


def affordance(dm):
	
	"""
	"""
	
	dm = dm.select('symm == "asymm"')

	pm = PivotMatrix(dm, ['response_hand', 'handle_side'],['file'], dv = "RT")
	pm.barPlot(show=True)
	plt.title("affordance effect")
	
def affLumCongr(dm):
	
	dm = dm.select('symm == "asymm"')

	xLabels = ["hande left", "handle right"]
	lLabels = ["control", "more contrast right", "more contrast left"]
	yLabel = "landing position: negative = left, positive = right"
	
	pm = PivotMatrix(dm, ['handle_side', 'mask_side'], ['file'], \
		dv='endX')
	pm._print()
	pm.barPlot(xLabels = xLabels, lLabels = lLabels, yLabel = yLabel, show=True)
	plt.title("overlap between contrast and affordance")

def gapEffect(dm, dv = "saccLat"):
	
	"""
	Regardless of color change...
	"""
	
	pm = PivotMatrix(dm, ['gap'],['file'],dv =dv)
	pm._print()
	pm.barPlot(show=True)
	plt.ylabel(dv)
	plt.title("gap effect")

def fixChange(dm, nBin = 4):
	
	dmGap = dm.select('gap == "zero"')
	dmNoGap = dm.select('gap == "overlap"')
	dmFixGray = dmNoGap.select('large_fix_col == "change"')
	dmFixBlack = dmNoGap.select('large_fix_col == "no_change"')
	
	fig = plt.figure()
	
	dmFixGray = dmFixGray.addField('fixSizeBin')
	dmFixGray = dmFixGray.calcPerc('large_fix_size', 'fixSizeBin', keys=['file'], nBin=nBin)
	pm = PivotMatrix(dmFixGray, ["fixSizeBin"], ["file"], dv = "saccLat")
	pm.plot(fig=fig, nLvl1 = 1,colors = ["blue"])

	dmFixBlack = dmFixBlack.addField('fixSizeBin')
	dmFixBlack = dmFixBlack.calcPerc('large_fix_size', 'fixSizeBin', keys=['file'], nBin=nBin)
	pm = PivotMatrix(dmFixBlack, ["fixSizeBin"], ["file"], dv = "saccLat")
	pm.plot(fig=fig, nLvl1 = 1,colors = ["red"])
	plt.legend(["color change", "no color change"])
	plt.show()



dm = getDM()
dm = select(dm)
#vfDiff(dm, dv="saccLat")
#regrLatRT(dm)

#gapEffect(dm)
#lumBinAn(dm,nBin = 5)
#simon(dm)
#affordance(dm)
#affLumCongr(dm)
#fixChange(dm)
gapDistr(dm,nBin = 50)
plt.savefig("latency distributions as a function of gap condition.jpg")
#gapRegr(dm)






