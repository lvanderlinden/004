# 

"""
DESCRIPTION:

"""
import numpy as np
import sys
import collections
import itertools
import random
import copy

# Define constants:
handleCond = ["handle_left", "handle_right"]
maskCond = ["mask_left", "mask_right", "mask_control"]
condList = list(itertools.product(handleCond, maskCond))

repList = [0,1,2,3,4,5,6]
letterList = collections.deque(['A','B','C','D','E','F'])
pictList =\
	["symm_garage_leveller", "asymm_kitchen_spoon2", "symm_garage_ruler", \
	"asymm_kitchen_spoon", "asymm_garage_chisel", "symm_kitchen_carrot", \
	"asymm_kitchen_sharpeningsteel", "asymm_garage_wrench", \
	"asymm_kitchen_washingbrush", "asymm_garage_screwdriver", \
	"symm_kitchen_roller", "asymm_kitchen_knife", "asymm_kitchen_peeler", \
	"asymm_garage_hammer", "asymm_garage_mallet", "asymm_kitchen_fork", \
	"asymm_garage_paintbrush", "asymm_garage_chisel2"]

# Create complete trial list for one block:
allPictures = pictList * len(condList)
#for obj in allPictures:
#	print obj
#sys.exit()

def getLSD(blockNr=1):
	
	"""
	Create array according to the constraints of a Latin Square Design:
	
	Returns:
	array 	--- containing repetition in columns and objects in rows
				filled with conditions according to LSD procedure
	"""
	
	# Shuffle the picture list:
	random.shuffle(pictList)

	array = np.zeros((19,7),dtype = '|S100')
	
	_letterList = copy.deepcopy(letterList)
	_letterList.rotate(-1*blockNr+1)

	array[0] = repList
	index = 0
	for i in range(len(pictList)):
		col = i +1
		index +=1
		array[col,0] = pictList[i]
		array[col,1:] = list(_letterList)
		_letterList.rotate(-1)
		if index in range(6,19,6):
			index = 0
			
	return array

def getDict():
	
	"""
	Create dictionary where the identifiers A to F refer to a randomly picked
	condition.
	
	returns:
	randomDict --- with identifier (A-F) as key and corresponding to condition as value
	"""
	
	# Shuffle the list:
	random.shuffle(condList)
	
	# Make a dictionary:
	randomDict = {}
	
	for i in range(len(condList)):
		randomDict[letterList[i]] = condList[i]
	
	return randomDict

# The script:


if __name__ == "__main__":

	a = getLSD(blockNr=2)
	print a
	d = getDict()

	# TODO: this should be pseudorandom, with minimum and maximum difference:
	_allPictures = copy.deepcopy(allPictures)
	random.shuffle(_allPictures)
	
	for i in range(len(allPictures)):
	
		# Determine the picture for the current trial:
		pict = _allPictures.pop()

		# Make a dictionary for counting the repetitions:
		icount = {} 
		# First set all values in the dictionary to 0:
		for i in allPictures:
			icount[i] = 0

		# Determine the repetition:
		for i in _allPictures:
			icount[i] = icount.get(i, 0) + 1
		rep = 6 - (icount[pict])
		
		# Look up the letter in the cell corresponding to column = rep, row = picture:
		for _a in a:
			if pict == _a[0]:
				letter = _a[rep]
				break
		# Look up the condition corresponding to the letter
		cond = d[letter]
