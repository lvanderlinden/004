#tmp.py

from PIL import Image
from matplotlib import pyplot as plt

from matplotlib.backends.backend_pdf import PdfPages
pp = PdfPages('test.pdf')
	

plt.rc("font", family="ubuntu")
plt.rc("font", size=12)

fileNames = ['fig1.png', 'fig2.png', 'fig3.png']
titleList = ["exp 1 uncorrected", "exp 1 corrrected", "exp 2"]
fig = plt.figure(figsize = (20,10))
plt.suptitle("Landing positions as a function of Contrast Side and Handle Side")
plt.subplots_adjust(hspace = 0, wspace = 0)
plotNr = 0
titleNr = 0
for f in fileNames:
	plotNr +=1
	plt.subplot(1,3,plotNr)
	plt.title(titleList[titleNr])
	img = Image.open(f)
	plt.imshow(img)
	plt.xticks([])
	plt.yticks([])
	titleNr +=1

pp.savefig(fig)


pp.close()
