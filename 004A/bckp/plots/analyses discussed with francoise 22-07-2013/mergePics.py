#tmp.py

from PIL import Image
from matplotlib import pyplot as plt

from matplotlib.backends.backend_pdf import PdfPages
pp = PdfPages('Timecourses.pdf')
	

plt.rc("font", family="ubuntu")
plt.rc("font", size=20)

"""
A = towards handle
B = towards contrast
"""

def mergePics(lFigPaths, nRows = None, nCols = None, supTitle = None, lTitles = None, \
	figSize = None, hSpace = None, wSpace = None):
	
	"""
	lFigPaths 	--- list of to-be-merged pictures
	nRows
	nCols
	
	Keyword arguments:
	supTitle
	lTitles -- list of titles for subplots
	"""
	
	if lTitles == None:
		lTitles = [None]*len(lFigs)
	
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
		plt.title(titleList[titleNr])
		img = Image.open(f)
		plt.imshow(img)
		plt.xticks([])
		plt.yticks([])
		titleNr +=1
		
		return fig
	

# TO HANDLE:
for direction in ["HANDLE", "CONTRAST"]:
	
	if direction == "HANDLE":
		var = "ToHandle"
	if direction == "CONTRAST":
		var = "ToContrast"
	
	fileNames = ["Landing (uncorrected) %s as a function of binned sacc lats exp 004A cousineau = True.png" % var, \
		"Landing (corrected) %s as a function of binned sacc lats exp 004A cousineau = True.png" % var, \
			"Landing (uncorrected) %s as a function of binned sacc lats exp 004B cousineau = True.png" % var]
	
	title = "Landing positions towards %s (positive = towards) as a function of binned latency" % direction
	titleList = ["exp 1 uncorrected", "exp 1 corrrected", "exp 2"]
	fig = plt.figure(figsize = (30,15))
	plt.suptitle(title)
	plt.subplots_adjust(hspace = 0, wspace = 0)
	plotNr = 0
	titleNr = 0
	for f in fileNames:
		plotNr +=1
		plt.subplot(1,3,plotNr)
		plt.title(titleList[titleNr])
		img = Image.open(f)
		plt.imshow(img)
		plt.xticks([])
		plt.yticks([])
		titleNr +=1

	pp.savefig(fig)
	plt.savefig("%s.png" %title)

pp.close()
