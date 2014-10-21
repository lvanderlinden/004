# 004

Landing positions as a function of handle side.
In revision for JoV.

## 004C

The additional experiment for the revision

### parse.py()

- From EyeLink events to dm containing raw fixation coordinates and time stamps.
- If fix_y is too close to the center (to the fix dot), the fixation is skipped (not used for the analysis).
- I don't look at saccade events.

### bbox.py()

- Determines the width and height of a bbox around the non-white pixels in the PNG file.
- We need these new width and height to normalize LPs (see [normOnWidth.py] relative to the actual stimulus (rather than the w and h of the PNG file)

### getDm.py()

Converts raw coordinates to meaningful coordinates:

- [centralOrigin.py] Normalize such that origin = (0,0)
- [rotate.py] Rotate as if object was presented at -90 in UVF
- [flip.py] Normalize on orientation, as if handle was always to the right
- [normOnWidth.py] Normalize on object width
	
### centralOrigin.py

- From OpenSesame coordinates (origin at top left) to normalized coordinates (origin at center)
- This is necessary to be able to rotate the landing positions

### rotate.py

- Rotates LPs as if object was always presented with a rotation angle of -90 degrees, that is, in the UPV with the CoG aligned on the vertical meridian
- For the formula, see: [http://en.wikipedia.org/wiki/Rotation_(mathematics)](http://en.wikipedia.org/wiki/Rotation_(mathematics))

### flip.py

- Flips landing positions if flip condition was "left".
- We can do this, because the LPs are already normalized on rotation (see [rotate.py])
- TODO: check whether this is ok

### normOnWidth.py

- Normalizes objects on object width, such that LPs become a percentile of the overall width.
- TODO: check with CoG

