modules:

getDM
Applies exclusion criteria to dm containing raw data, and adds new variables if
desired. 

analyses packages:

					package = distribution

overallDistr
Plots distribution histogram of a given dependent variable.

splitDistr
Plots distribution histograms of a given dependent variable split by a given
independent variable.

					package = anova
					
statSubplot
Plots stats in a subplot.

prettyStat
Creates pretty strings containing stats from one-factorial ANOVA.

oneFactor
Performs and plots a one-factorial ANOVA.

twoFactor
Performs and plots a two-factorial ANOVA.

threeFactor
Performs and plots a three-factorial ANOVA.


			package = regressionAnalyses
			


			package = binAnalyses
			
			
			
			
contrastBinAn
Plots landing position as a function of binned saccade latencies and contrast 
(left, right or control).

regrLatRT
Examines whether RT and saccade latencies are correlated. Interesting results
are only obtained when too-slow RT's and error trials are excluded.

regrJitter
Examines whether jitter (variable duration between fixation onset and stimulus
onset) is correlated with a certain dependent variable (RT or saccade latency).
TODO: Jitter op juiste manier berekenen!

simon
Investigates whether a given dependent variable (RT, accuracy, or saccLat) varies
as a function of side with the most contrast and response hand. 

affordance
Investigates whether a given dependent variable (RT, accuracy, or saccLat) varies 
as a function of the handle side and the response hand. 

vfDiff
Checks whether a given dependent variable (RT, accuracy, or saccLat) differs
between upper and lower visual field.

landOnHandle
Checks whether handle side has an effect on landing position, such that the 
eyes are pulled more towards the handle.


contrastHandle
Investigates whether a given dependent variable (RT, accuracy, saccLat, or 
landing position) varies as a function of the handle side and the side with the 
most contrast.


