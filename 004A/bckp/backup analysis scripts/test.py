from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
pp = PdfPages('foo.pdf')
			  

for i in range(3):
	
	fig = plt.figure()
	
	pp.savefig(fig)
pp.close()