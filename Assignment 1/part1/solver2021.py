#!/usr/local/bin/python3
# solver2021.py : 2021 Sliding tile puzzle solver
#
# Code by: Barza Fayazi-Azad (bfayazi)
#
# Based on skeleton code by D. Crandall & B551 Staff, September 2021
#

import sys
import heapq

ROWS=5
COLS=5


# Correct indices for all the cells - will be used to calculate manhattan distance
correct_placement = {1: (0, 0), 2: (0, 1), 3: (0, 2), 4: (0, 3), 5: (0,4), 6: (1,0), 7:(1,1), 8:(1,2), 9:(1,3),
                    10:(1,4), 11:(2,0), 12:(2,1), 13:(2,2), 14:(2,3), 15:(2,4), 16:(3,0), 17:(3,1), 18:(3,2),
                    19:(3,3), 20:(3,4), 21:(4,0), 22:(4,1), 23:(4,2), 24:(4,3), 25:(4,4)}



# Convert index to get row and column value
def index_to_rc(index):
    return (int(index/5), index % 5)


# Rotate a row to the left
def slide_row_left(row):
    return row[1:] + row[0:1]

# Successors of rotating rows to the left
def row_left_successors(state, row):
    rotated_row = slide_row_left(state[row*5:(row*5)+5])
    return (tuple(state[0:row*5] + rotated_row + state[(row*5)+5:]))


# Rotate a row to the right
def slide_row_right(row):
    return row[-1:] + row[0:-1]

# Successors of rotating a row to the right
def row_right_successors(state, row):
    rotated_row = slide_row_right(state[row*5:(row*5)+5])
    return (tuple(state[0:row*5] + rotated_row + state[(row*5)+5:]))


# Rotate a column up
def slide_col_up(col):
    return col[1:] + col[0:1]

# Successors of rotating a column up
def col_up_successors(state, col):
    rotated_col = slide_col_up(state[col:col+21:5])
    return (tuple(state[0:col] + tuple([rotated_col[0]])) + state[col+1:col+5] + tuple([rotated_col[1]]) + state[col+6:col+10] + tuple([rotated_col[2]]) + state[col+11:col+15] + tuple([rotated_col[3]]) + state[col+16:col+20] + tuple([rotated_col[4]]) + state[col+21:])


# Rotate a column down
def slide_col_down(col):
    return col[-1:] + col[0:-1]

# Successors of rotating a column down
def col_down_successors(state,col):
    rotated_col = slide_col_down(state[col:col + 21:5])
    return (tuple(state[0:col] + tuple([rotated_col[0]])) + state[col + 1:col + 5] + tuple([rotated_col[1]]) + state[col + 6:col + 10] + tuple([rotated_col[2]]) + state[col + 11:col + 15] + tuple([rotated_col[3]]) + state[col + 16:col + 20] + tuple([rotated_col[4]]) + state[col + 21:])


# Rotate outer ring clockwise
def rotate_outer_clockwise(state):
    return (tuple([state[5]]) + tuple(state[0:4]) + tuple([state[10]]) + tuple(state[6:9]) + tuple([state[4]]) + tuple([state[15]]) + tuple(state[11:14]) + tuple([state[9]]) + tuple([state[20]]) + tuple(state[16:19]) + tuple([state[14]]) + tuple([state[21]]) + tuple(state[22:25]) + tuple([state[19]]))

# Rotate outer ring counterclockwise
def rotate_outer_counter(state):
    return (tuple([state[1]]) + tuple(state[2:5]) + tuple([state[9]]) + tuple([state[0]]) + tuple(state[6:9]) + tuple([state[14]]) + tuple([state[5]]) + tuple(state[11:14]) + tuple([state[19]]) + tuple([state[10]]) + tuple(state[16:19]) + tuple([state[24]]) + tuple([state[15]]) + tuple(state[20:23]) + tuple([state[23]]))


# Rotate inner ring clockwise
def rotate_inner_clockwise(state):
    return (tuple(state[0:6]) + tuple([state[11]]) + tuple(state[6:8]) + tuple(state[9:11]) + tuple([state[16]]) + tuple([state[12]]) + tuple([state[8]]) + tuple(state[14:16]) + tuple(state[17:19]) + tuple([state[13]]) + tuple(state[19:]))


# Rotate inner ring counterclockwise
def rotate_inner_counter(state):
    return (tuple(state[0:6]) + tuple(state[7:9]) + tuple([state[13]]) + tuple(state[9:11]) + tuple([state[6]]) + tuple([state[12]]) + tuple([state[18]]) + tuple(state[14:16]) + tuple([state[11]]) + tuple(state[16:18]) + tuple(state[19:]))


# Calculate manhattan distance for a singular cell
def cell_manhattan(row,col,correct_row,correct_col):
    return abs(row - correct_row) + abs(col - correct_col)


# Calculate manhattan distance for the entire board
def board_manhattan(state):
    total_manhattan = 0
    for index, val in enumerate(state):
        row, col = index_to_rc(index)
        total_manhattan += cell_manhattan(row,col,correct_placement[val][0],correct_placement[val][1])
    return total_manhattan


def printable_board(board):
    return [ ('%3d ')*COLS  % board[j:(j+COLS)] for j in range(0, ROWS*COLS, COLS) ]


# return a list of possible successor states
def successors(state):
    # What to return:
        # return the new board states
        # return the direction moved
        # return the manhattan distance for each new board state

    # Successor states are as follows:
        # each row (1-5) moved one spot to the left
        # each row (1-5) moved one spot to the right
        # each column (1-5) moved one spot to the left
        # each column (1-5) moved one spot to the right
        # rotate outer ring clockwise
        # rotate outer ring counterclockwise
        # rotate inner ring clockwise
        # rotate inner ring counterclockwise

    # initiate empty successors list
    successors_list = []

    # Since up to 5 rows/columns can be rotated, loop through all of their possible successor states
    for i in range(0, 5):
        successors_list.append(
            [(row_left_successors(state, i)), 'L' + str(i + 1), board_manhattan(row_left_successors(state, i))])
        successors_list.append(
            [(row_right_successors(state, i)), 'R' + str(i + 1), board_manhattan(row_right_successors(state, i))])
        successors_list.append(
            [(col_up_successors(state, i)), 'U' + str(i + 1), board_manhattan(col_up_successors(state, i))])
        successors_list.append(
            [(col_down_successors(state, i)), 'D' + str(i + 1), board_manhattan(col_down_successors(state, i))])

        # Since outer/inner ring rotations can only happen once each way, no need to loop
    successors_list.append([(rotate_outer_clockwise(state)), 'Oc', board_manhattan(rotate_outer_clockwise(state))])
    successors_list.append([(rotate_outer_counter(state)), 'Occ', board_manhattan(rotate_outer_counter(state))])
    successors_list.append([(rotate_inner_clockwise(state)), 'Ic', board_manhattan(rotate_inner_clockwise(state))])
    successors_list.append([(rotate_inner_counter(state)), 'Icc', board_manhattan(rotate_inner_counter(state))])

    return successors_list



# check if we've reached the goal
def is_goal(state):
    # If the sorted state is equal to the current state
    return sorted(state) == list(state)




def solve(initial_board):
    """
    1. This function should return the solution as instructed in assignment, consisting of a list of moves like ["R2","D2","U1"].
    2. Do not add any extra parameters to the solve() function, or it will break our grading and testing code.
       For testing we will call this function with single argument(initial_board) and it should return 
       the solution.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """
    # Using heapq module to represent a priority queue. This will help to prioritize the successor state with the lowest total cost from the heuristic function
    # Heappush: Used to insert elements into the heap data structure
    # Heappop: Used to remove and return the smallest elements from the heap data structure
    # More information on heapq module and sample implementation can be found here (https://docs.python.org/3/library/heapq.html) and here (https://www.geeksforgeeks.org/heap-queue-or-heapq-in-python/)

    # Need to keep track of whether a state has been visited or not - using dictionary for speed purposes
    # Originally tried list and dictionary was faster
    visited_states = {tuple(initial_board):True}
    # Initialize an empty fringe
    fringe = []


    # Two variables for search - current path which is the final result and the current cost which is our total cost so far of the search
    current_path = []
    current_cost = 0

    # Insert starting elements into the fringe (manhattan distance of the initial board, current_state (which includes current board, current cost and current path))
    heapq.heappush(fringe, (board_manhattan(initial_board), (initial_board, current_cost, current_path)))

    # While fringe is populated
    while fringe:
        # Pop out elements from the fringe
        _, (state, current_cost, current_path) = heapq.heappop(fringe)
        # Get all the possible successor states from the current state
        for (next_state, move, manhattan_cost) in successors(state):
            # if the successor state is a goal state, return the current path plus the final move
            if is_goal(next_state):
                return current_path + [move]
            else:
                # If the state has not been visited, add it to the visited dict
                if next_state not in visited_states.keys():
                    visited_states[next_state] = True
                    # heuristic value of the state
                    heuristic_val = current_cost + 1 + manhattan_cost
                    # Push next set of elements into the fringe (heuristic value of the state, state of the board, current cost + 1, current path + latest move
                    heapq.heappush(fringe, (heuristic_val, (next_state, current_cost + 1, current_path + [move])))

    return False





# Please don't modify anything below this line
#
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a board filename"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]

    if len(start_state) != ROWS*COLS:
        raise(Exception("Error: couldn't parse start state file"))

    print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))

    print("Solving...")
    route = solve(tuple(start_state))
    
    print("Solution found in " + str(len(route)) + " moves:" + "\n" + " ".join(route))
