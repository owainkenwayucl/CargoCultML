# Global variables to control max recursion depth.  This is intended to
# limit memory blow-up attacks
MAX_DEPTH=4096
UNLIMITED_DEPTH=False

# Check to see if current depth is OK.
def depth_ok(depth): 
    return (UNLIMITED_DEPTH or (MAX_DEPTH >= depth))