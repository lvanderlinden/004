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

fig = plt.figure(figsize = (5,10))
plt.subplots_adjust(hspace=0)

src = "./plots after mask is applied/asymm_garage_hammer_mask_control.jpg"
# Read if the image is a string and not a numpy array
path, ext = os.path.splitext(src)
pict = path.split("/")[-1]

if isinstance(src, basestring):
	src = plt.imread(src)
	
src = np.array(src, np.uint32)

plt.subplot(2,1,1)
plt.imshow(1-src)
plt.xticks([])
plt.yticks([])
plt.axvline(xCen, color = cenCol, linewidth = 3)
plt.axhline(yCen, color = cenCol,linewidth = 3)

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

plt.subplot(2,1,2)
fig = plt.figure()
plt.imshow(src)#1-original)
# Indicate center of image with widht = 720, height = 540:
plt.axvline(xCen, color = cenCol, linewidth = 3)
#plt.axhline(yCen, color = cenCol,linewidth = 3)
plt.xticks([])
plt.yticks([])

# Indicate center of gravity:
plt.axvline(x, linestyle = "--", color = gravCol, linewidth = 2)
#plt.axhline(y, linestyle = "--", color = gravCol, linewidth = 2)

for ext in [".svg", ".png"]:
	plt.savefig("CoG_calculation%s" % ext)

plt.show()


