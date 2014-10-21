import getDm
import parse
from exparser.Cache import cachedDataMatrix, cachedArray
from matplotlib import pyplot as plt
from exparser.TangoPalette import *
import numpy as np

dm = parse.parseAsc(cacheId = "parsed")
dm = getDm.addCoord(dm,cacheId = "with_coord")
dm = getDm.addLat(dm, cacheId = "with_lat")

def yNormDist(y):
	
	"""
	Normalizes y axis distribution plots such that it ranges between 0 and 1.
	
	Arguments:
	y		--- y axis values
	"""

	# Normalise:
	y = abs(y)
	
	_min = float(np.min(y))
	_max = float(np.max(y))
	
	yNorm = (y-_min)/(_max-_min)
	
	return yNorm

def plotDist(dm, dv, col=None, label=None, bins = 10):
	
	"""
	Arguments:
	dm		--- DataMatrix instance
	dv		--- dependent variable
	col 	--- color
	"""
	
	if col == None:
		col = blue[1]

	# Determine y:
	y, edges = np.histogram(dm[dv], bins = bins)
	yNorm = yNormDist(y)
	# Determine x:
	x = .5*edges[1:] + .5*edges[:-1]
	# Plot:
	plt.plot(x, yNorm, marker='.', color = col, markeredgecolor = col,\
		markerfacecolor = col, markeredgewidth = 1, label = label)


def select(dm):
	
	"""
	Apply some selection criteria.
	"""

	dm = dm.select("saccLat1 != ''")
	dm = dm.select("saccLat1 > 0")
	dm = dm.select("xNorm1 != ''")
	dm = dm.select("xNorm1 != -1000")
	
	return dm

def gap(dm, norm=True, dv = "saccLat1"):
	
	"""
	Plots sacc lat distributions as a function of gap condition.
	
	Arguments:
	dm		--- DataMatrix instance
	
	Keyword arguments:
	norm	--- Boolean indicating whether or not to remove BS variance.
	"""

	lCols = [orange[1], blue[1]]
	
	if not norm:
		dv = dv
	
	elif norm:
		dm = dm.addField("ws_%s" % dv)
		dm = dm.withinize(dv, "ws_%s" % dv, "file")
		dv = "ws_%s" % dv
	
	for gap in dm.unique("gap"):
		_dm = dm.select("gap == '%s'" % gap)
		col = lCols.pop()
		plotDist(_dm, dv, col=col, label = gap)
	plt.legend(loc = 'best', frameon =False)
	plt.savefig("gap.png")


def lpDist(dm, norm = False):

	"""
	Plots landing positions of first and second fixation as a function of
	stimulus type.
	"""
	
	for fix in (1, 2):
		
		plt.subplot(2,1,fix)
		plt.title("fix = %s" % fix)
		_dm = dm.select("xNorm%s != ''" % fix)
		_dm = _dm.select("xNorm%s != -1000" % fix)
		
		dv = "xNorm%s" % fix
		
		if not norm:
			dv = dv
	
		elif norm:
			_dm = _dm.addField("ws_%s" % dv)
			_dm = _dm.withinize(dv, "ws_%s" % dv, "file")
			dv = "ws_%s" % dv

		lCols = [orange[1], blue[1]]	

		for stimType in dm.unique("stim_type"):
			col = lCols.pop()
			__dm = _dm.select("stim_type == '%s'" % stimType)
			plotDist(__dm, dv, col=col, label = stimType, bins = 30)
			plt.axvline(0, color = gray[3], linestyle = "--")
		plt.legend()
		plt.savefig("lp.png")

def timecourse():
	
	"""
	"""

if __name__ == "__main__":
	
	dm = select(dm)
	#gap(dm)
	lpDist(dm)
	
	
