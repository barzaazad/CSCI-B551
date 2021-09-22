#!/usr/local/bin/python3
#
# route_pichu.py : a maze solver
#
# Submitted by : Barza Fayazi-Azad (bfayazi)
#
# Based on skeleton code provided in CSCI B551, Fall 2021.

import sys


# Parse the map from a given filename
def parse_map(filename):
        with open(filename, "r") as f:
                return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]


# Check if a row,col index pair is on the map
def valid_index(pos, n, m):
        return 0 <= pos[0] < n and 0 <= pos[1] < m


# Find the possible moves from position (row, col)
# Add a current path variable to the moves function that will track the path of moves
# that we have taken using 'U','D','L','R' characters
def moves(map, current_path, row, col):
        moves = ((row + 1, col, current_path + 'D'), (row - 1, col, current_path + 'U'), (row, col - 1, current_path + 'L'), (row, col + 1, current_path + 'R'))

        # Return only moves that are within the house_map and legal (i.e. go through open space ".")
        return [move for move in moves if valid_index(move, len(map), len(map[0])) and (map[move[0]][move[1]] in ".@")]


# Perform search on the map
#
# This function MUST take a single parameter as input -- the house map --
# and return a tuple of the form (move_count, move_string), where:
# - move_count is the number of moves required to navigate from start to finish, or -1
#    if no such route exists
# - move_string is a string indicating the path, consisting of U, L, R, and D characters
#    (for up, left, right, and down)

def search(house_map):
        # Find pichu start position
        pichu_loc = [(row_i, col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if
                     house_map[row_i][col_i] == "p"][0]
        # Add the current path to the fringe - initial state will be an empty string since there is no path at first
        fringe = [(pichu_loc, 0, '')]
        # Record a list of cell locations that have been visited already - initial state will be the pichu location
        cells_visited = [pichu_loc]

        while fringe:
                # Adjust our pop method to account for the current path variable we've added to the fringe
                (curr_move, curr_dist, current_path) = fringe.pop()
                for move in moves(house_map, current_path, *curr_move):
                        # Record what the next move's position will be
                        next_move = (move[0], move[1])
                        if house_map[move[0]][move[1]] == "@":
                                return (curr_dist + 1, move[2])  # If we reach the desired location,
                                                                 # return current distance + 1 as the number of
                                                                 # moves and our path output from the moves function
                        else:
                                # Need to make sure we're not repeating cells (i.e. going backwards or in loops)
                                # If our next move is unvisited, then add it to the fringe and to our cells visited list
                                if next_move not in cells_visited:
                                        cells_visited.append(next_move)
                                        fringe.append((next_move, curr_dist + 1, move[2]))
        # If there is no solution, display path length -1 and no path
        return (-1,"")

# Main Function
if __name__ == "__main__":
        house_map = parse_map(sys.argv[1])
        print("Shhhh... quiet while I navigate!")
        solution = search(house_map)
        print("Here's the solution I found:")
        print(str(solution[0]) + " " + solution[1])