"""
DESCRIPTION:
Create DM containing CoG per stimulus. 
"""

import sys
import cog
import os
import numpy as np
from exparser.CsvReader import CsvReader
from matplotlib import pyplot as plt
from scipy import ndimage, misc
from PIL import Image, ImageDraw

from exparser.TangoPalette import *

stimList = ["chisel", "chisel2", "mallet", "paintbrush", "screwdriver", \
	"wrench", "fork", "knife", "peeler", "sharpeningsteel", "spoon", \
		"spoon2", "washingbrush", "hammer"]

r = 10
for stim in stimList:
	
	for stimType in ["object"]:
		path = "final/%s_%s.png" % (stimType, stim)
		_src = ndimage.imread(path)[:,:,:3]	
		src = np.empty(_src.shape, dtype=np.uint32)
		src[:] = _src
		x,y = cog.cog(src.copy())

		print x, y
			
		im = Image.open(path)
		
		w, h = im.size
		
		x = x +w/2
		y = y +h/2
		
		print x, y
		
		#sys.exit()
		
		draw = ImageDraw.Draw(im)
		draw.ellipse((w/2-r, h/2-r, w/2+r, h/2+r), fill = green[1], outline = "black")
		draw.ellipse((x-r, y-r, x+r, y+r), fill = blue[1], outline = "black")
		plt.imshow(im)
		plt.savefig("Test_%s.png" % stim)
	