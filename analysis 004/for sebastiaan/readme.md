# Data matrices:
	 
## Exp 1:
dm = "selected_dm_004A_WITH_drift_corr.csv"

dependent variables:
- normalised landing positions of saccade 1, 2, and 3 relative to absolute center (= vertical meridian):
	*endX1NormToHandle, endX2NormToHandle, endX3NormToHandle*
- normalised landing positions of saccade 1, 2 and 3 relative to CoG:
	*endX1CorrNormToHandle, endX2CorrNormToHandle, endX3CorrNormToHandle*


## Exp 2:
dm = "selected_dm_004A_WITH_drift_corr.csv:

dependent variables:
- normalised landing positions of saccade 1, 2 and 3 relative to CoG (= vertical meridian):
	*endX1NormToHandle, endX2NormToHandle, endX3NormToHandle*

# Selection criteria that could/should be applied before stat. analysis:
## Obligatory:
	
	~~~ .python
	dm = dm.select("endX%sNorm != ''" % sacc, verbose = verbose)
	# where sacc is "1", "2" or "3"
	~~~
	
## Optionally:
	
	~~~ .python
	dm = dm.selectByStdDev(keys = ["file"], dv = dv)
	# where dv is one of the aforementioned dv's
	~~~

# Factors that could be included in the analyses (same column names in both dm's):


### Continuous variables:
- saccade latency: *saccLat1, saccLat2, saccLat3"*
- eccentricity of the target (vertical distance between center of the screen and center of the stimulus): *y_stim*

### Categorical variables:
- hand of response: *response_hand*
- handle orientation: *handle_side*