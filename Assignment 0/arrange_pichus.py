#!/usr/local/bin/python3
#
# arrange_pichus.py : arrange agents on a grid, avoiding conflicts
#
# Submitted by : Barza Fayazi-Azad (bfayazi)
#
# Based on skeleton code in CSCI B551, Fall 2021.

import sys

# Parse the map from a given filename
def parse_map(filename):
	with open(filename, "r") as f:
		return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]

# Count total # of pichus on house_map
def count_pichus(house_map):
    return sum([ row.count('p') for row in house_map ] )

# Return a string with the house_map rendered in a human-pichuly format
def printable_house_map(house_map):
    return "\n".join(["".join(row) for row in house_map])

# check if the row is a valid row
def check_row(house_map, row, col):
    # check the columns behind pichu for conflicts
    checker = False
    for i in range(col-1,-1,-1):
        if house_map[row][i] == "p":
            return checker
        if house_map[row][i] in ["X","@"]:
            checker = True
            break
    # check the columns in front of pichu for conflicts
    for i in range(col+1,len(house_map[0])):
        if house_map[row][i] == "p":
            checker = False
            return checker
        if house_map[row][i] in ["X","@"] and checker is True:
            return checker

    return True

# check if the column is a valid column
def check_col(house_map,row,col):
    # check the rows behind pichu for conflicts
    checker = False
    for i in range(row-1,-1,-1):
        if house_map[i][col] == "p":
            return checker
        if house_map[i][col] in ["X","@"]:
            checker = True
            break
    # check the rows in front of pichu for conflicts
    for i in range(row+1, len(house_map)):
        if house_map[i][col] == "p":
            checker = False
            return checker
        if house_map[i][col] in ["X","@"] and checker is True:
            return checker

    return True

# Check if the top left diagonal is valid
def check_tl_diag(house_map,row,col):
    checker = False
    # check top left diag
    for r,c in zip(range(row-1,-1,-1), range(col-1,-1,-1)):
        if house_map[r][c] == "p":
            return checker
        if house_map[r][c] in ["X","@"]:
            checker = True

    return True

# Check if the bottom left diagonal is valid
def check_bl_diag(house_map,row,col):
   # check bottom left diag
    checker = False
    for r, c in zip(range(row+1, len(house_map)), range(col-1, -1, -1)):
        if house_map[r][c] == "p":
            return checker
        if house_map[r][c] in ["X", "@"]:
            checker = True

    return True

# Check if the top right diagonal is valid
def check_tr_diag(house_map,row,col):
    # check top right diag
    checker = False
    for r, c in zip(range(row-1, -1, -1), range(col+1, len(house_map[0]))):
        if house_map[r][c] == "p":
            return checker
        if house_map[r][c] in ["X", "@"]:
            checker = True

    return True

# Check if the bottom right diagonal is valid
def check_br_diag(house_map,row,col):
    # check bottom right diag
    checker = False
    for r,c in zip(range(row+1,len(house_map)), range(col+1,len(house_map[0]))):
        if house_map[r][c] == "p":
            return checker
        if house_map[r][c] in ["X","@"]:
            checker = True

    return True

# Check all of the diagonals at once
def check_diag(house_map,row,col):
    return check_tl_diag(house_map,row,col) and check_bl_diag(house_map,row,col) \
           and check_tr_diag(house_map,row,col) and check_br_diag(house_map,row,col)



# Check the rows, columns, and diagonals of the pichu positions in the successor states at once
def check_row_col_diag(house_map,row,col):
    return check_row(house_map,row,col) and check_col(house_map,row,col) and check_diag(house_map,row,col)



# Add a pichu to the house_map at the given position, and return a new house_map (doesn't change original)
def add_pichu(house_map, row, col):
    return house_map[0:row] + [house_map[row][0:col] + ['p',] + house_map[row][col+1:]] + house_map[row+1:]

# Get list of successors of given house_map state
# Add the check_row_col_diag function to make sure all of our possible successors satisfy that condition
def successors(house_map):
    return [ add_pichu(house_map, r, c) for r in range(0, len(house_map)) for c in range(0,len(house_map[0])) if house_map[r][c] == '.'
             and check_row_col_diag(house_map,r,c)]

# check if house_map is a goal state
def is_goal(house_map, k):
    return count_pichus(house_map) == k



# Arrange agents on the map
#
# This function MUST take two parameters as input -- the house map and the value k --
# and return a tuple of the form (new_house_map, success), where:
# - new_house_map is a new version of the map with k agents,
# - success is True if a solution was found, and False otherwise.
#
def solve(initial_house_map,k):
    fringe = [initial_house_map]
    # Keep track of visited states
    visited_states = []
    while len(fringe) > 0:
        for new_house_map in successors( fringe.pop() ):
            if is_goal(new_house_map,k):
                return(new_house_map,True)
            else:
                # Add successor state to fringe + visited states if not previously visited
                if new_house_map not in visited_states:
                    visited_states.append(new_house_map)
                    fringe.append(new_house_map)


# Main Function
if __name__ == "__main__":
    house_map=parse_map(sys.argv[1])
    # This is k, the number of agents
    k = int(sys.argv[2])
    print ("Starting from initial house map:\n" + printable_house_map(house_map) + "\n\nLooking for solution...\n")
    solution = solve(house_map,k)
    print ("Here's what we found:")
    print (printable_house_map(solution[0]) if solution else "False")


