from exparser.CsvReader import CsvReader
from matplotlib import pyplot as plt

f = "Sylvie.csv"

dm = CsvReader(f).dataMatrix()
dm = dm.addField("trial_dur")

for i in dm.range():
	# Skip the very first trial because it doesn't have a previous trial:
	if i == 0:
		dm["trial_dur"][i] = -1000
	else:
		s = dm["time_correct_response"][i-1]
		e = dm["time_correct_response"][i]

		dur = e-s
		dm["trial_dur"][i] = dur

# Exclude first trial, which was skipped:
dm = dm.select("trial_dur > 0")
dm["trial_dur"] = dm["trial_dur"]/1000/60

#import analyse
#analyse.plotDist(dm, "trial_dur", bins = 100)
#plt.show()

plt.hist(dm["trial_dur"], bins=100)
plt.show()

# Exclude trials that took longer than 1 minute, because this was probably a 
# break:

#dm = dm.select("trial_dur < 60000")
#ms = dm["trial_dur"].sum()
#sec = ms/1000.
#mins = sec/60.
#print mins