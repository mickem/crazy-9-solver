import itertools
import math
import time

# Skip number of iteration (continue mode)
SKIP = 000000
# How frequently we should report status (every x iterations)
TIME_SPLIT = 50000

# Constants used for arrays
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
COLOR = 0
SIDE = 1

# Tiles
# First char is Color (W=White, P=Purple, I=pInk, Y=Yellow)
# Second char is Head or But
# Order per tile is UP, RIGHT, DOWN, LEFT
tiles = [
        [ "WB", "PB", "IH", "YH" ],
        [ "YH", "PB", "IB", "PH" ],
        [ "YH", "PH", "WB", "IB" ],
        [ "IH", "PB", "YB", "WH" ],
        [ "YH", "IH", "PB", "WB" ],
        [ "PH", "IH", "WB", "YB" ],
        [ "WH", "IH", "WB", "YB" ],
        [ "WH", "YH", "PB", "IB" ],
        [ "IH", "WB", "YB", "PH" ]
    ]

# Validate that 
def sides_match(s1, s2):
    """Check if a tile matches.
       Checks that the color is the same but the shape is different.
    """
    return s1[COLOR] == s2[COLOR] and not s1[SIDE] == s2[SIDE]

def row_match(t1, t2, t3):
    """Check if a row (3 tiles) matches.
    """
    if not sides_match(t1[RIGHT], t2[LEFT]):
        return False
    if not sides_match(t2[RIGHT], t3[LEFT]):
        return False
    return True

def col_match(t1, t2, t3):
    """Check if a column (3 tiles) matches.
    """
    if not sides_match(t1[DOWN], t2[UP]):
        return False
    if not sides_match(t2[DOWN], t3[UP]):
        return False
    return True

def set_match(s):
    """Check if an entire set (3x3 tiles) matches.
    """
    global attempt_counter
    attempt_counter = attempt_counter + 1
    if not row_match(s[0], s[1], s[2]):
        return False
    if not row_match(s[3], s[4], s[5]):
        return False
    if not row_match(s[6], s[7], s[8]):
        return False
    if not col_match(s[0], s[3], s[6]):
        return False
    if not col_match(s[1], s[4], s[7]):
        return False
    if not col_match(s[2], s[5], s[8]):
        return False
    return True

def rotate_tile(s, index):
    """Create a copy of set with a single tile rotated one step.
    """
    s2 = list(s)
    tile = s[index]
    s2[index] = [tile[LEFT], tile[UP], tile[RIGHT], tile[DOWN]]
    return s2

def print_set(s):
    """Print a set (solution).
    """
    print("Solution")
    print(s[0], s[1], s[2])
    print(s[3], s[4], s[5])
    print(s[6], s[7], s[8])

def set_match_wr(s, rotindex = 0):
    """The recursive solver which solves a set with all possible rotations.
        This function recurses rotating all consecutive tiles
    """
    if rotindex > 8:
        return False
    if set_match(s):
        print_set(s)
        return True
    s = rotate_tile(s, rotindex)
    if set_match_wr(s, rotindex+1):
        return True
    s = rotate_tile(s, rotindex)
    if set_match_wr(s, rotindex+1):
        return True
    s = rotate_tile(s, rotindex)
    if set_match_wr(s, rotindex+1):
        return True
    return False

# Some variables used to keep track of things
all_perm = math.factorial(len(tiles))
process_done = 0
iter_start = time.time()
last_tell = 0
attempt_counter = 0

# Print status information periodically
def status(idx):
    global last_tell, process_done, all_perm, iter_start
    process_done = process_done + idx
    if process_done - last_tell > TIME_SPLIT:
        count = process_done - last_tell
        elap = time.time()-iter_start
        if elap < 1:
            elap = 1
        print("Trying %d of %d %f/s"%(process_done, all_perm, count/elap))
        last_tell = process_done
        iter_start = time.time()

cur_idx = 0
skip_index = 0
solution_index = 0
global_start = time.time()
#
# Loop through all permutations of tiles solving all
#
for item in itertools.permutations(tiles):
    skip_index = skip_index + 1
    cur_idx = cur_idx + 1
    if skip_index < SKIP:
        continue
    if set_match_wr(list(item)):
        solution_index = solution_index + 1
    if cur_idx > TIME_SPLIT/10:
        status(cur_idx)
        cur_idx = 0
elap = time.time()-global_start
print("Found %d solutions from %d combinations in %d seconds"%(solution_index, attempt_counter, elap))