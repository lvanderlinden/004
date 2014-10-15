import os
import numpy as np
from PIL import Image


def sliced():

	"""
	Slices apropriate-sized rectangle from big texture canvas
	"""
	
	src = "texture output"
	dst = "texture-output-sliced"
	
	for stim in os.listdir(src):
		path = os.path.join(src, stim)

		img = Image.open(path)

		box = (0, 0, 720, 540)
		sliced = img.crop(box)
		sliced.save(os.path.join(dst, stim))
	
	
def merge():
	
	"""
	"""
	
	srcText = "texture-output-sliced"
	srcShapes = "final/non-object shapes"
	dst = "final/non-objects with texture"
	lMaskMix = os.listdir(srcShapes)
	
	for stim in os.listdir(srcText):
		print stim
		nonObject = lMaskMix.pop()
		
		path1 = os.path.join(srcText, stim)
		img1 = Image.open(path1)
		a1 = np.asarray(img1)
		#print type(a1)
		
		path2 = os.path.join(srcShapes, nonObject)
		img2 = Image.open(path2)
		a2 = np.asarray(img2)
		#print np.unique(a2), a2.dtype
		
		aFinal = a1.copy()
		#for channel in range(3):
		#	aFinal[:,:,channel] = aFinal[:,:,channel]*(a2/255)
		aFinal[np.where(a2 != 255)] = 255
		imFinal = Image.fromarray(aFinal)
		imFinal.save(os.path.join(dst,stim))
		#sys.exit()
		
if __name__ == "__main__":
	
	sliced()
	merge()