# Simple quintris program! v0.2
# D. Crandall, Sept 2021

from AnimatedQuintris import *
from SimpleQuintris import *
from kbinput import *
from operator import itemgetter
import time, sys

class HumanPlayer:
    def get_moves(self, quintris):
        print("Type a sequence of moves using: \n  b for move left \n  m for move right \n  n for rotation\n  h for horizontal flip\nThen press enter. E.g.: bbbnn\n")
        moves = input()
        return moves

    def control_game(self, quintris):
        while 1:
            c = get_char_keyboard()
            commands =  { "b": quintris.left, "h": quintris.hflip, "n": quintris.rotate, "m": quintris.right, " ": quintris.down }
            commands[c]()

#####
# This is the part you'll want to modify!
# Replace our super simple algorithm with something better
#
class ComputerPlayer:
    def get_height(self, board):
        height = 0
        for i in range(0, len(board)-1):
            for x in range(0, len(board[0])-1):
                if board[i][x] == "x":
                    height = i 
                    return height
        return height


    def evaluate_function(self, current_state, future_state, quintris):
        modified_state, score = quintris.remove_complete_lines(future_state, 0)

        current_height = self.get_height(current_state)
        modified_height = self.get_height(future_state)

        score = modified_height - current_height
        return score

    #This will return possible coordinates to place the piece
    def get_possible_moves(self, piece, moves, board, row, col, quintris):
        futures = []
        piece_length = len(piece)
        piece_height = len(piece[0])
        print(piece_height, piece_length)

        for i in range(0, len(board[0])-piece_length):
            direct = i - col
            move = ""

            if (direct < 0):
                direct = direct * -1
                move = "b" * direct
            elif (direct > 0):
                move = "m" * direct

            for x in range(len(board)-piece_height, 0, -1):
                if board[x][i] != "x":
                    print(x, i)
                    future_state, score = quintris.place_piece(board, 0, piece[0], x, i)
                    future_score = self.evaluate_function(board, future_state, quintris)
                    futures.append(((x, i), moves + move, future_state, future_score))     
                break
        return futures

    def expectimax(self, node, node_type):
        return True

    def build_tree(self):
        return True

    def add_node(self, node, node_type):
        temp = Node(node, node_type)
        return temp

    def get_best_moves(self,piece_states, current_piece, current_row, current_col, quintris, board):
        futures = []
        for state in piece_states:
             piece_move = self.get_possible_moves(state[0], state[1], board, current_row, current_col, quintris)
             best_move = max(piece_move,key=lambda item:item[3])
             futures.append(best_move)
        return futures

    # This will return all possible, non-duplicate states of a piece
    def get_possible_states(self, piece, quintris):
        temp_states = [[[piece[0]], ""], [[quintris.rotate_piece(piece[0], 90)], "n"], [[quintris.rotate_piece(piece[0], 180)], "nn"], [[quintris.rotate_piece(piece[0], 270)], "nnn"], [[quintris.hflip_piece(piece[0])], "h"], [[quintris.rotate_piece(quintris.hflip_piece(piece[0]), 90)], "hn"], [[quintris.rotate_piece(quintris.hflip_piece(piece[0]), 180)], "hnn"], [[quintris.rotate_piece(quintris.hflip_piece(piece[0]), 270)], "hnnn"] ]

        possible_states = []
        state_list = []

        for state in temp_states:
            if state[0] not in state_list:
                possible_states.append(state)
                state_list.append(state[0])

        return possible_states

    # This function should generate a series of commands to move the piece into the "optimal"
    # position. The commands are a string of letters, where b and m represent left and right, respectively,
    # and n rotates. quintris is an object that lets you inspect the board, e.g.:
    #   - quintris.col, quintris.row have the current column and row of the upper-left corner of the 
    #     falling piece
    #   - quintris.get_piece() is the current piece, quintris.get_next_piece() is the next piece after that
    #   - quintris.left(), quintris.right(), quintris.down(), and quintris.rotate() can be called to actually
    #     issue game commands
    #   - quintris.get_board() returns the current state of the board, as a list of strings.
    #
    def get_moves(self, quintris):
        piece_set = quintris.PIECES
        board = quintris.get_board()

        current_piece = quintris.get_piece()
        next_piece = quintris.get_next_piece()

        possible_states = self.get_possible_states(current_piece, quintris)
        moves = self.get_best_moves(possible_states, current_piece[0], current_piece[1], current_piece[2], quintris, board)
        move = max(moves,key=lambda item:item[3])

        # Initialize node
        root = self.add_node(0, "root")

        #return random.choice("mnbh") * random.randint(1, 10)
        return move[1]
       
    # This is the version that's used by the animted version. This is really similar to get_moves,
    # except that it runs as a separate thread and you should access various methods and data in
    # the "quintris" object to control the movement. In particular:
    #   - quintris.col, quintris.row have the current column and row of the upper-left corner of the 
    #     falling piece
    #   - quintris.get_piece() is the current piece, quintris.get_next_piece() is the next piece after that
    #   - quintris.left(), quintris.right(), quintris.down(), and quintris.rotate() can be called to actually
    #     issue game commands
    #   - quintris.get_board() returns the current state of the board, as a list of strings.
    #
    def control_game(self, quintris):
        # another super simple algorithm: just move piece to the least-full column
        while 1:
            time.sleep(0.1)

            board = quintris.get_board()
            column_heights = [ min([ r for r in range(len(board)-1, 0, -1) if board[r][c] == "x"  ] + [100,] ) for c in range(0, len(board[0]) ) ]
            index = column_heights.index(max(column_heights))

            if(index < quintris.col):
                quintris.left()
            elif(index > quintris.col):
                quintris.right()
            else:
                quintris.down()

class Node:
    def __init__(self, value, node_type):
        self.value = value
        self.children = []
        self.node_type = node_type

class prev_pieces:
    def __init__(self, pieces):
        self.pieces = []

###################
#### main program

(player_opt, interface_opt) = sys.argv[1:3]

try:
    if player_opt == "human":
        player = HumanPlayer()
    elif player_opt == "computer":
        player = ComputerPlayer()
    else:
        print("unknown player!")

    if interface_opt == "simple":
        quintris = SimpleQuintris()
    elif interface_opt == "animated":
        quintris = AnimatedQuintris()
    else:
        print("unknown interface!")

    quintris.start_game(player)

except EndOfGame as s:
    print("\n\n\n", s)



