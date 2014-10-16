"""
DESCRIPTION:
Create block_loop content
"""

from exparser.CsvReader import CsvReader


srcDm = "/home/lotje/Documents/PhD Marseille/Studies/004 - Single-object experiment - Handle-orientation effect/004C/stimuli/cog_per_stim.csv"
dm = CsvReader(srcDm).dataMatrix()

stimList = ["chisel", "chisel2", "mallet", "paintbrush", "screwdriver", \
	"wrench", "fork", "knife", "peeler", "sharpeningsteel", "spoon", \
		"spoon2", "washingbrush", "hammer"]

f = open("blockloop.csv", "w")


for direction in [-20, 0, 20]:
	for stimType in ["object", "non-object"]:
		for flip in ["left", "right"]:
			for vf in ["upper","lower"]:
				for gap in ["zero", "overlap"]:
					for stim in stimList:
						_dm = dm.select("stim_type == '%s'" % stimType)
						_dm = _dm.select("name == '%s'" % stim)
						assert(len(_dm)==1)
						cog = _dm["xCoG"][0]
						if flip == "left":
							cog = cog * -1
						
						print "object = ", stim
						print "flip = ", flip
						print "cog = ", cog
						#raw_input()
						f.write(",".join([str(direction), \
							stimType, flip, vf, gap, stim, str(cog)]) + "\n")
f.close()