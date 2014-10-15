"""
DESCRIPTION:
I can't exactly reproduce the way I calculated the CoG for 004A and 004B.

Possible explanations:
- slightly different input sources (e.g. with and without floating px removed 
	in Gimp)
- overflow issue is solved in ndimage

This scripts plots and calculates the correlation between the old and new CoG.
"""

import csv
import cog
import os
import numpy as np
from exparser.CsvReader import CsvReader
from matplotlib import pyplot as plt

fCompare = open("compare_cog.csv", "w")
fCompare.write(",".join(["stim", "xCoGOld", "xCoGNew"])+"\n")

fOld = "old_cog_dict.csv"

stimList = ["chisel", "chisel2", "mallet", "paintbrush", "screwdriver", \
	"wrench", "fork", "knife", "peeler", "sharpeningsteel", "spoon", \
		"spoon2", "washingbrush"]

src = "/home/lotje/Documents/PhD Marseille/Studies/004 - Single-object experiment - Handle-orientation effect/004C/stimuli/final/objects"

old_dict = {}
for key, val in csv.reader(open(fOld)):
	new_key = key.strip('()').split(',')
	
	stim = new_key[0]
	stim = stim.strip(" \'")
	mask = new_key[1]
	mask = mask.strip(" \'")
	handle = new_key[2]
	handle = handle.strip(" '\'")
	
	if not stim in stimList:
		continue
	
	if handle == "left":
		continue
	if mask != "mask_control":
		continue
	new_val = val.strip('()').split(',')
	
	x = new_val[0]
	y = new_val[1]
	_dir = new_val[2]
	x.strip(" \'")
	y.strip(" \'")
	_dir.strip(" \'")
	
	old_dict[stim, mask, handle] = x,y,_dir
	
	path = os.path.join(src, "object_%s.jpg" % stim)
	print path
	
	xNew, yNew = cog.cog(path,show = False, invert = True, edgeDetect = True)
	
	fCompare.write(",".join([stim, str(x), str(xNew)])+ "\n")

fCompare.close()

dm = CsvReader("compare_cog.csv").dataMatrix()

fig = plt.figure()

plt.plot(dm["xCoGOld"], dm["xCoGNew"], '.')
from scipy.stats import linregress
print linregress(dm["xCoGOld"], dm["xCoGNew"])
plt.show()

