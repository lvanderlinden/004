"""
DESCRIPTION:
Create block_loop content
"""

from exparser.CsvReader import CsvReader
from matplotlib import pyplot as plt

fNew = "cog_per_stim_004C.csv"
dmNew = CsvReader(fNew).dataMatrix()

lStim = ["chisel", "chisel2", "mallet", "paintbrush", "screwdriver", \
	"wrench", "fork", "knife", "peeler", "sharpeningsteel", "spoon", \
		"spoon2", "washingbrush", "hammer"]

def cogDict():
	
	"""
	In 004B, I didn't log the cog nor the x coordinates of the stimulus.
	Therefore, we need to read in this information from the csv file that
	was also used when running the experiment in OpenSesame.
	
	We read this csv file in as a dictionary containing the following key-value
	arrangement:
	key = (object, mask, flip), tuple
	value = xCog
	"""

	f = "cog_dict_004B.csv"
	f = open(f, "r")
	
	d = {}
	
	for line in f:
		for char in ['"', '(', ')', ' ', "'"]:
			line =  line.replace(char,'')
		
		stimName, mask, flip, xCog, yCog, dirCog = line.split(",")
		mask = mask.replace("mask_", '')
		d[stimName, mask, flip] = xCog
		
	return d

fOld = open("cog_per_stim_004B.csv", "w")
fOld.write(",".join(["object", "xCog"]) + "\n")
d = cogDict()

for stim in lStim:
	xCog = d[stim, "control", "right"]
	fOld.write(",".join([stim, xCog]) + "\n")
fOld.close()

dmOld = CsvReader("cog_per_stim_004B.csv").dataMatrix()

# Sort on object:
dmOld.sort("object")
dmNew.sort("name")

fig = plt.figure()
plt.plot(dmOld["xCog"], color = "red")
plt.plot(dmNew["xCog"], color = "blue")
plt.show()

fig = plt.figure()
plt.plot(dmOld["xCog"], dmNew["xCog"], '.')
from scipy.stats import linregress
print linregress(dmOld["xCog"], dmNew["xCog"])
plt.show()

	
