import getDm
from exparser.PivotMatrix import PivotMatrix
from matplotlib import pyplot as plt

exp = "004C"

dm = getDm.getDm(exp = exp, cacheId = "%s_final" % exp)
dm = dm.select("file != '004C19.asc'")
dm = dm.select("file != '004c8.asc'")

dm = dm.select("correct == 1")
dm = dm.selectByStdDev(["file"], "response_time")
dm = dm.select("direction == 0")
dm = dm.addField("congruency", dtype = str)
dm = dm.addField("respHand", dtype = str)
dm["respHand"][dm.where("correct_response == 1")] = "left"
dm["respHand"][dm.where("correct_response == 2")] = "right"

for i in dm.range():
	
	handle = dm["flip"][i]
	respHand = dm["respHand"][i]
	
	
	if handle == respHand:
		dm["congruency"][i] = "congruent"
		print "congruent"
	else:
		dm["congruency"][i] = "incongruent"
		print "incongruent"
	
	
	print "flip = ", dm["flip"][i]
	print "correct response = ", dm["correct_response"][i]
	print "response hand = ", dm["respHand"][i]
	print "congruency = ", dm["congruency"][i]
	
pm = PivotMatrix(dm, ["congruency", "stim_type"], ["file"], "response_time", colsWithin = True)
pm.linePlot()
plt.show()


