import constants

def fromPP((x,y)):
	
	"""
	Converts Psychopy coordinates to normal coordinates
	
	Keyword arguments:
	x,y		--- to-be-converted coordinates, tuple
	
	
	Returns converted coordinates
	"""
	
	x, y = (x,y)
	
	_x = constants.xCen + x
	_y = constants.yCen - y
	
	return _x, _y