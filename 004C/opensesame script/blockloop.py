"""
DESCRIPTION:
Create block_loop content
"""

stimList = ["chisel", "chisel2", "mallet", "paintbrush", "screwdriver", \
	"wrench", "fork", "knife", "peeler", "sharpeningsteel", "spoon", \
		"spoon2", "washingbrush"]

f = open("blockloop.csv", "w")


for direction in [-20, 0, 20]:
	for stim_type in ["object", "non-object"]:
		for flip in ["left", "right"]:
			for vf in ["upper","lower"]:
				for gap in ["zero", "overlap"]:
					for stim in stimList:
						f.write(",".join([str(direction), \
							stim_type, flip, vf, gap, stim]) + "\n")
f.close()