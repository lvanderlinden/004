def getPerc(start, end):
	
	"""
	"""
	
	perc =100.-((float(end)/float(start))*100.)
	
	return perc

# Exp1:
# Sacc 1:
# Uncorrected:
start = 2111
end = 2047
perc = getPerc(start,end)
#print perc
# Corrected:
end = 2035
perc = getPerc(start,end)
#print perc
	
# Sacc 2:
# Uncorrected:
start = 1489
end = 1409
perc = getPerc(start,end)
#print perc
# Corrected:
end = 1408
perc = getPerc(start,end)
#print perc

# Exp 2:
# Sacc 1:
start = 2318
end = 2227
perc = getPerc(start,end)
#print perc

# Sacc 2:
start = 1487
end = 1414
perc = getPerc(start,end)
#print perc

# Supplementary Materials:
start = 4569
end = 4421
perc = getPerc(start,end)
#print perc

start = 2902
end = 2799
perc = getPerc(start,end)
#print perc
