#!/usr/bin/env python
from saliency import simulateScanpath
from exparser.DataMatrix import DataMatrix
import os
from PIL import Image, ImageDraw

for frame in os.listdir('frames'):
	print frame
	im = Image.open('frames/' + frame)
	dr = ImageDraw.Draw(im)
	l = simulateScanpath(im)
	
	i = 1
	for p in l[1:]:
		t = p[0]
		x = p[1]
		y = p[2]
		dr.ellipse((x-5,y-5,x+5,y+5), outline='red')
		dr.text((x,y), '%d(%.0f)' % (i,t), fill='green')
		i += 1
	im.save('simulation/png/%s' % frame)	
	dm = DataMatrix(l)
	dm.save('simulation/csv/%s.csv' % frame[:-4])	
