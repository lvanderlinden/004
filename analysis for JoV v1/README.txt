applyMasK:
	
	Loads image and applies mask.
	
	Purpose of this module: We need to create those images because
	we need to calculat the CoG of these images.
	
	TODO:
		How do I know for sure that the current mask is identical
		to the mask made with PsychoPy in the experiment?
		
		I have to check this! Maybe this explains why in 004B
		the eyes do not land on the CoG when mask is applied.
		
		Best would be to apply mask with psychopy just as in
		OpenSesame.
	

geCoG:
	
	Calculates center of gravity of a given object (with or without edge detection)
	and stores all CoG's in a dictionary per object per handle side per mask side.
	
	Purpose: I want to determine the CoG for each object to be able to correct for this 
	during data analysis. I want to do this while parsing the raw data, such that
	the CoG values already exist in the data matrix.
	
	While walking through the asc files, the exact trial info (the picture, the 
	mask side (control, left or right), and orientation (handle left or handle right)
	can be used to determine the corresponding (offline-determined) coordinates of the CoG.

	
	The structure of the dictionary is like so:
		
		Key = object, mask side, location (tuple)
		Value = xCoG, yCoG (tuple)
		
		So: dictionary[(object,  mask_side, handle_side)] = (x,y)
		For example: dictionary[('knife',  'mask_left', 'right')] = (354.76, 266.98)
				
	TODO: 
		Check whether this structure is still used (and still desirable)
	
	NOTE:
		The coordinates are exact (relative to the top left of the bitmap) rather than
		relative to the center-center??

drawBox:
	
	Following Pajak & Nuthmann (2013), an imaginary just-fitting rectangly is drawn
	around the objects to determine an object's 'personal' width and height.
	This will enable us to normalize all landing positions.

constants:
	
	Contains constant variables in studies 004A and 004B