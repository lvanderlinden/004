#!/usr/bin/env python
import os
#from saliency import saliencyMap
from PIL import Image
from matplotlib import pyplot as plt
from scipy import ndimage

f = open('saliency-cog.csv', 'w')
f.write('object,xCoG,yCoG\n')

for path in os.listdir('resources/Experiment'):
	if not path.endswith('.jpg') or path.startswith('plot-'):
		continue
	_path = 'resources/Experiment/' + path
	print path
	img = Image.open(_path)
	w, h = img.size
	# ezvision --just-initial-saliency-map --in=input.png --out=png
	salMap = saliencyMap(img)
	salMap = salMap.resize( (w, h) )
	salMap.save('saliency/%s' % path)
	y, x = ndimage.center_of_mass(ndimage.imread('saliency/%s' % path))
	plt.clf()
	plt.subplot(211)
	plt.imshow(img)
	plt.subplot(212)
	plt.imshow(salMap)
	plt.axhline(y)
	plt.axvline(x)
	plt.savefig('saliency/plot-%s' % path)	
	f.write('%s,%f,%f\n' % (path, x, y))
f.close()