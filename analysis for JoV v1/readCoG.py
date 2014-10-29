import csv
import numpy as np
import sys
# TODO!

# The dict should be adapted a little bit, because the 
# keys and values are big string rather than tuples of strings:



def readCoG():
	
	"""
	"""
	
	cog_dict = {}
	
	for key, val in csv.reader(open("cog_dict.csv")):
		new_key = key.strip('()').split(',')
		
		object = new_key[0]
		object = object.strip(" \'")
		mask = new_key[1]
		mask = mask.strip(" \'")
		handle = new_key[2]
		handle = handle.strip(" '\'")
		
		new_val = val.strip('()').split(',')
		
		x = new_val[0]
		y = new_val[1]
		dir = new_val[2]
		x.strip(" \'")
		y.strip(" \'")
		dir.strip(" \'")
		
		cog_dict[object, mask, handle] = x,y,dir

	return cog_dict


if __name__ == "__main__":
	dict = readCoG()
	
	for mask in ["control", "right", "left"]:

		l = []
		for i in dict:
			if i[-1] != "right":
				continue
			if i[1] != "mask_%s" % mask:
				continue
			if i[0] in ["carrot", "ruler", "leveller", "roller"]:
				continue
			#print i[0], dict[i][0]
			l.append(float(dict[i][0]))
		a = np.asarray(l)
		avg = a.mean()/720
		print mask, avg
	sys.exit()