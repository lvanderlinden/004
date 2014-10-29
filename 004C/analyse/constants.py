# Copied from constants in OpenSesame script:
ratio = 34
scale = 3

wStim = 720.
hStim= 540.

w = 1024
h = 768

xCen = w/2
yCen = h/2

srcStim = "/home/lotje/Documents/PhD Marseille/Studies/004/004C/opensesame script"

# The y position of the eyes should be at least 2 degrees (?) from the 
# center of the display

# TODO: Change for new ecc:
minYDistFromFix = 2 * ratio
#minYDistFromFix = 0

thLower = yCen - minYDistFromFix
thUpper =  yCen + minYDistFromFix

