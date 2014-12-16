from scipy import ndimage, misc
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
#f = "/home/lotje/Media/Pictures/MARIAGE_SOAZIG/IMGP2226.JPG"
#pic = Image.open(f)
#pix = np.array(pic.getdata()).reshape(pic.size[0], pic.size[1], 3)

#for i in pix:
#	print i
#	raw_input()


a = \
[[0,0,0,0,0],
[0,0,1,0,0],
[0,1,1,0,0],
[0,0,0,1,0],
[0,0,0,0,0]]

gx = \
[[-1,0,1],
[-2,0,2],
[-1,0,1]
]

gy = \
[[-1,-2,-1],
[0,0,0],
[1,2,1]
]

a = np.asarray(a)
plt.imshow(a, interpolation = 'none')
#plt.show()

sx = ndimage.sobel(a, axis=0, mode='constant')
sy = ndimage.sobel(a, axis=1, mode='constant')

print "input = "
print a[1:4,1:4]
print

print "input * gx = "
xoutput = a[1:4,1:4] * gx
print xoutput#[1:4,1:4]

print "input * gy = "
youtput = a[1:4, 1:4] * gy
print youtput#[1:4,1:4]
sys.exit()

#sys.exit()


s = np.hypot(sx, sy)

print "X = ",
#print sx
print sx[1:4,1:4]
print
print "Y = ",
print sy[1:4,1:4]
print
print "Sobel = ",
print s[1:4,1:4]
print


sys.exit()


a