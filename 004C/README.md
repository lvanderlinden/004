# 004C:

Experiment 3, for JoV Revision 1

## stimuli

### shape.py
Makes new shapes out of two real objects.
The result is the shape of a non-object.

### texture.py
Places real objects on a large canvas (e.g. a canvas filled with hammers).
This is the input file for the S&P Matlab algorithm.
The result is the texture of a non-object.

### nonObjects.py
Pastes the S&P Matlab texture of a given object on a given new shape. 
The result is a non-object of which the CoG is not yet matched.

### cog.py
Calculates center of gravity of a given input image (with or without edge detection).

### corrCoG.py
Determines the correlation between the old CoGs (used to align objects in 004B, but impossible to reproduce) and new CoGs (used to align objects in 004C).

### matchCoG.py
Reshapes non-objects such that the CoG is at the same position as the CoG of the matched object.
The result is the final non-object.

## opensesame script


