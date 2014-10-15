from matplotlib import pyplot as plt
from scipy import ndimage
import sys
import os
import numpy as np



plt.rc("font", family="arial")
plt.rc("font", size=10)

# Define constants:
path = "/home/lotje/Documents/PhD Marseille/Studies/004 - Single-object experiment - Handle-orientation effect/004B/experiment"

# Size of the bitmaps:
width = 720
height = 540

# Centers of the bitmap:
xCen = width/2
yCen = height/2

# Color:
gravCol = "#f57900"
cenCol = "#3465a4"

invert = True
edgeDetect = True
col = True

fig = plt.figure()
plt.subplots_adjust(hspace=0)
subPlot = 0


for mask in ["right", "control", "left"]:
	subPlot +=1

	src = "./plots after mask is applied/asymm_kitchen_knife_mask_%s.jpg" % mask
	# Read if the image is a string and not a numpy array
	path, ext = os.path.splitext(src)
	pict = path.split("/")[-1]
	figName = "CoG calculation %s invert = %s edgeDetect = %s.svg"%(pict, invert, edgeDetect)
	
	
	
	if isinstance(src, basestring):
		src = plt.imread(src)
		
	src = np.array(src, np.uint32)
	# Invert the 0-1 values
	
	original = src
	
	# Invert:
	src = 1-src
		
	# Edge detection using Sobel operator, see
	# <http://scipy-lectures.github.com/advanced/image_processing/index.html#edge-detection>
	
	sx = ndimage.sobel(src, axis=0, mode='constant')
	sy = ndimage.sobel(src, axis=1, mode='constant')
	src = np.hypot(sx, sy)
	
	# Get center of mass	
	
	if col:
		y, x, col = ndimage.measurements.center_of_mass(src)
	else:
		y, x = ndimage.measurements.center_of_mass(src)
	
	plt.subplot(3,1,subPlot)
	plt.imshow(1-original)
	# Indicate center of image with widht = 720, height = 540:
	line1 = plt.axvline(xCen, color = cenCol, linewidth = 3)
	plt.axhline(yCen, color = cenCol,linewidth = 3)
	plt.xticks([])
	plt.yticks([])
	
	# Indicate center of gravity:
	line2 = plt.axvline(x, linestyle = "--", color = gravCol, linewidth = 2)
	plt.axhline(y, linestyle = "--", color = gravCol, linewidth = 2)
	#plt.legend([line1, line2], ["Absolute center", "Center of gravity"], loc = 'best')
	#plt.annotate('%.1f,%.1f' % (x,y), (x,y))
	
for ext in [".svg", ".png"]:
	plt.savefig("CoG_per_contrast%s" % ext)
	
plt.show()
	
	
