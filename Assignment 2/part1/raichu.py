#
# raichu.py : Play the game of Raichu
#
# Barza Fayazi-Azad (bfayazi), Kaavya Tejaswi (kpolukon), Nathaniel Priddy (ngpriddy)
#
# Based on skeleton code by D. Crandall, Oct 2021
#
import copy
import sys
import time
from math import inf

def board_to_string(board, N):
    return "\n".join(board[i:i+N] for i in range(0, len(board), N))


def board_to_list(board,N):
    list_board = []
    for i in range(0,len(board),N):
        row = board[i:i+N]
        list_board.append(list(row))
    return list_board


# All successors for pichu moves
def pichu(board,player):
    pichu_successors = []
    # Moves for player w
    if player == 'w':
        for row in range(len(board)):
            for col in range(len(board)):
                # if its a pichu
                if board[row][col] == 'w':
                    # Moving diagonally down to the right
                    if col >= 0 and col < len(board)-2 and row < len(board) - 2:
                        # taking black pichu
                        if board[row+1][col+1] == 'b' and board[row+2][col+2] == '.':
                            copyboard = copy.deepcopy(board)
                            copyboard[row][col] = '.'
                            copyboard[row+1][col+1] = '.'
                            # taking black pichu and getting raichu at same time
                            if row+2 == len(board)-1:
                                copyboard[row + 2][col + 2] = '@'
                            else:
                                copyboard[row+2][col+2] = 'w'
                            pichu_successors.append(copyboard)
                    if col >= 0 and col < len(board) - 1:
                        if board[row+1][col+1] == '.':
                            # getting a raichu by itself
                            if row+1 == len(board)-1:
                                copyboard = copy.deepcopy(board)
                                copyboard[row+1][col+1] = '@'
                                copyboard[row][col] = '.'
                                pichu_successors.append(copyboard)
                            else:
                                # simple move
                                copyboard = copy.deepcopy(board)
                                copyboard[row + 1][col + 1] = 'w'
                                copyboard[row][col] = '.'
                                pichu_successors.append(copyboard)
                    # Moving diagonally down to the left
                    if col > 1 and col <= len(board) - 1 and row < len(board)-2:
                        # taking black pichu
                        if board[row + 1][col - 1] == 'b' and board[row + 2][col - 2] == '.':
                            copyboard = copy.deepcopy(board)
                            copyboard[row][col] = '.'
                            copyboard[row + 1][col - 1] = '.'
                            # taking black pichu and getting raichu at same time
                            if row+2 == len(board) - 1:
                                copyboard[row + 2][col - 2] = '@'
                            else:
                                copyboard[row + 2][col - 2] = 'w'
                            pichu_successors.append(copyboard)
                    if col > 0 and col <= len(board) - 1:
                        if board[row + 1][col - 1] == '.':
                            # getting a raichu normally
                            if row + 1 == len(board) - 1:
                                copyboard = copy.deepcopy(board)
                                copyboard[row + 1][col - 1] = '@'
                                copyboard[row][col] = '.'
                                pichu_successors.append(copyboard)
                            else:
                                # simple move
                                copyboard = copy.deepcopy(board)
                                copyboard[row + 1][col - 1] = 'w'
                                copyboard[row][col] = '.'
                                pichu_successors.append(copyboard)
    # Moves for player b
    else:
        for row in range(len(board)):
            for col in range(len(board)):
                # if its a pichu
                if board[row][col] == 'b':
                    # Moving diagonally up to the right
                    if col >= 0 and col < len(board) - 2 and row > 1:
                        # taking white pichu
                        if board[row - 1][col + 1] == 'w' and board[row - 2][col + 2] == '.':
                            copyboard = copy.deepcopy(board)
                            copyboard[row][col] = '.'
                            copyboard[row - 1][col + 1] = '.'
                            # taking white pichu and getting raichu
                            if row -2 == 0:
                                copyboard[row - 2][col + 2] = '$'
                            else:
                                copyboard[row - 2][col + 2] = 'b'
                            pichu_successors.append(copyboard)
                    if col >= 0 and col < len(board) - 1:
                        if board[row - 1][col + 1] == '.':
                            # getting a raichu by itself
                            if row - 1 == 0:
                                copyboard = copy.deepcopy(board)
                                copyboard[row - 1][col + 1] = '$'
                                copyboard[row][col] = '.'
                                pichu_successors.append(copyboard)
                            else:
                                # simple move
                                copyboard = copy.deepcopy(board)
                                copyboard[row - 1][col + 1] = 'b'
                                copyboard[row][col] = '.'
                                pichu_successors.append(copyboard)
                    # Moving diagonally up to the left
                    if col > 1 and col <= len(board) - 1 and row > 1:
                        # taking white pichu
                        if board[row - 1][col - 1] == 'w' and board[row - 2][col - 2] == '.':
                            copyboard = copy.deepcopy(board)
                            copyboard[row][col] = '.'
                            copyboard[row - 1][col - 1] = '.'
                            # taking pichu and getting raichu
                            if row-2 == 0:
                                copyboard[row - 2][col - 2] = '$'
                            else:
                                copyboard[row - 2][col - 2] = 'b'
                            pichu_successors.append(copyboard)
                    if col > 0 and col <= len(board) - 1:
                        if board[row - 1][col - 1] == '.':
                            # getting a raichu
                            if row - 1 == 0:
                                copyboard = copy.deepcopy(board)
                                copyboard[row - 1][col - 1] = '$'
                                copyboard[row][col] = '.'
                                pichu_successors.append(copyboard)
                            else:
                                # simple move
                                copyboard = copy.deepcopy(board)
                                copyboard[row - 1][col - 1] = 'b'
                                copyboard[row][col] = '.'
                                pichu_successors.append(copyboard)

    return pichu_successors


# All successors for pikachu moves
def pikachu(board,player):
    pikachu_successors = []
    # Moves for player w
    if player == 'w':
        for row in range(len(board)):
            for col in range(len(board)):
                # if its a pikachu
                if board[row][col] == 'W':
                    # 3 steps forward jump when taking opponent piece
                    if row < len(board) - 3:
                        # Taking black pieces v1
                        if board[row+1][col] == '.' and board[row+2][col] in ('b','B') and board[row+3][col] == '.':
                            copyboard = copy.deepcopy(board)
                            copyboard[row][col] = '.'
                            copyboard[row+1][col] = '.'
                            copyboard[row+2][col] = '.'
                            # also getting a raichu while taking
                            if row+3 == len(board) - 1:
                                copyboard[row+3][col] = '@'
                            else:
                                copyboard[row+3][col] = 'W'
                            pikachu_successors.append(copyboard)
                        # Taking black pieces v2
                        if board[row+1][col] in ('b','B') and board[row+2][col] == '.' and board[row+3][col] == '.':
                            copyboard = copy.deepcopy(board)
                            copyboard[row][col] = '.'
                            copyboard[row + 1][col] = '.'
                            copyboard[row + 2][col] = '.'
                            # also getting a raichu while taking
                            if row + 3 == len(board) - 1:
                                copyboard[row + 3][col] = '@'
                            else:
                                copyboard[row + 3][col] = 'W'
                            pikachu_successors.append(copyboard)

                    # 2 step forward jump when taking opponents piece
                    if row < len(board) - 2:
                        # Taking black pieces
                        if board[row+1][col] in ('b','B') and board[row+2][col] == '.':
                            copyboard = copy.deepcopy(board)
                            copyboard[row][col] = '.'
                            copyboard[row+1][col] = '.'
                            if row+2 == len(board) - 1:
                                copyboard[row+2][col] = '@'
                            else:
                                copyboard[row+2][col] = 'W'
                            pikachu_successors.append(copyboard)

                        # Normal 2 step forward move with raichu possibility
                        if board[row+1][col] == '.' and board[row+2][col] == '.':
                            copyboard = copy.deepcopy(board)
                            copyboard[row][col] = '.'
                            copyboard[row+1][col] = '.'
                            if row+2 == len(board) - 1:
                                copyboard[row+2][col] = '@'
                            else:
                                copyboard[row+2][col] = 'W'
                            pikachu_successors.append(copyboard)

                    # 1 step forward normal
                    if row < len(board) - 1:
                        if board[row+1][col] == '.':
                            copyboard = copy.deepcopy(board)
                            copyboard[row][col] = '.'
                            if row+1 == len(board) - 1:
                                copyboard[row+1][col] = '@'
                            else:
                                copyboard[row+1][col] = 'W'
                            pikachu_successors.append(copyboard)

                    # Left Movement

                    # 3 steps left jump when taking opponent piece
                    if col > 2:
                        # Taking black pieces v1
                        if board[row][col-1] == '.' and board[row][col-2] in ('b', 'B') and board[row][col-3] == '.':
                            copyboard = copy.deepcopy(board)
                            copyboard[row][col] = '.'
                            copyboard[row][col-1] = '.'
                            copyboard[row][col-2] = '.'
                            copyboard[row][col-3] = 'W'
                            pikachu_successors.append(copyboard)
                        # Taking black pieces v2
                        if board[row][col-1] in ('b', 'B') and board[row][col-2] == '.' and board[row][
                            col-3] == '.':
                            copyboard = copy.deepcopy(board)
                            copyboard[row][col] = '.'
                            copyboard[row][col-1] = '.'
                            copyboard[row][col-2] = '.'
                            copyboard[row][col-3] = 'W'
                            pikachu_successors.append(copyboard)

                    # 2 step left jump when taking opponents piece
                    if col > 1:
                        # Taking black pieces
                        if board[row][col-1] in ('b', 'B') and board[row][col-2] == '.':
                            copyboard = copy.deepcopy(board)
                            copyboard[row][col] = '.'
                            copyboard[row][col-1] = '.'
                            copyboard[row][col-2] = 'W'
                            pikachu_successors.append(copyboard)

                        # Normal 2 step left move
                        if board[row][col-1] == '.' and board[row][col-2] == '.':
                            copyboard = copy.deepcopy(board)
                            copyboard[row][col] = '.'
                            copyboard[row][col-1] = '.'
                            copyboard[row][col-2] = 'W'
                            pikachu_successors.append(copyboard)

                    # 1 step left normal
                    if col > 0:
                        if board[row][col-1] == '.':
                            copyboard = copy.deepcopy(board)
                            copyboard[row][col] = '.'
                            copyboard[row][col-1] = 'W'
                            pikachu_successors.append(copyboard)

                    # Right Movement

                    # 3 steps right jump when taking opponent piece
                    if col < len(board) - 3:
                        # Taking black pieces v1
                        if board[row][col + 1] == '.' and board[row][col + 2] in ('b', 'B') and board[row][
                            col + 3] == '.':
                            copyboard = copy.deepcopy(board)
                            copyboard[row][col] = '.'
                            copyboard[row][col + 1] = '.'
                            copyboard[row][col + 2] = '.'
                            copyboard[row][col + 3] = 'W'
                            pikachu_successors.append(copyboard)
                        # Taking black pieces v2
                        if board[row][col + 1] in ('b', 'B') and board[row][col + 2] == '.' and board[row][
                            col + 3] == '.':
                            copyboard = copy.deepcopy(board)
                            copyboard[row][col] = '.'
                            copyboard[row][col + 1] = '.'
                            copyboard[row][col + 2] = '.'
                            copyboard[row][col + 3] = 'W'
                            pikachu_successors.append(copyboard)

                    # 2 step right jump when taking opponents piece
                    if col < len(board) - 2:
                        # Taking black pieces
                        if board[row][col + 1] in ('b', 'B') and board[row][col + 2] == '.':
                            copyboard = copy.deepcopy(board)
                            copyboard[row][col] = '.'
                            copyboard[row][col + 1] = '.'
                            copyboard[row][col + 2] = 'W'
                            pikachu_successors.append(copyboard)

                        # Normal 2 step right move
                        if board[row][col + 1] == '.' and board[row][col + 2] == '.':
                            copyboard = copy.deepcopy(board)
                            copyboard[row][col] = '.'
                            copyboard[row][col + 1] = '.'
                            copyboard[row][col + 2] = 'W'
                            pikachu_successors.append(copyboard)

                    # 1 step right normal
                    if col < len(board) - 1:
                        if board[row][col + 1] == '.':
                            copyboard = copy.deepcopy(board)
                            copyboard[row][col] = '.'
                            copyboard[row][col + 1] = 'W'
                            pikachu_successors.append(copyboard)

    # Other player

    else:
        for row in range(len(board)):
            for col in range(len(board)):
                # if its a pikachu
                if board[row][col] == 'B':
                    # 3 steps forward jump when taking opponent piece
                    if row > 2:
                        # Taking white pieces v1
                        if board[row -1][col] == '.' and board[row - 2][col] in ('w', 'W') and \
                                board[row - 3][col] == '.':
                            copyboard = copy.deepcopy(board)
                            copyboard[row][col] = '.'
                            copyboard[row - 1][col] = '.'
                            copyboard[row - 2][col] = '.'
                            # also getting a raichu while taking
                            if row - 3 == 0:
                                copyboard[row - 3][col] = '$'
                            else:
                                copyboard[row - 3][col] = 'B'
                            pikachu_successors.append(copyboard)
                        # Taking white pieces v2
                        if board[row - 1][col] in ('w', 'W') and board[row - 2][col] == '.' and \
                                board[row - 3][col] == '.':
                            copyboard = copy.deepcopy(board)
                            copyboard[row][col] = '.'
                            copyboard[row - 1][col] = '.'
                            copyboard[row - 2][col] = '.'
                            # also getting a raichu while taking
                            if row - 3 == 0:
                                copyboard[row - 3][col] = '$'
                            else:
                                copyboard[row - 3][col] = 'B'
                            pikachu_successors.append(copyboard)

                    # 2 step forward jump when taking opponents piece
                    if row > 1:
                        # Taking white pieces
                        if board[row - 1][col] in ('w', 'W') and board[row - 2][col] == '.':
                            copyboard = copy.deepcopy(board)
                            copyboard[row][col] = '.'
                            copyboard[row - 1][col] = '.'
                            if row - 2 == 0:
                                copyboard[row - 2][col] = '$'
                            else:
                                copyboard[row - 2][col] = 'B'
                            pikachu_successors.append(copyboard)

                        # Normal 2 step forward move with raichu possibility
                        if board[row - 1][col] == '.' and board[row - 2][col] == '.':
                            copyboard = copy.deepcopy(board)
                            copyboard[row][col] = '.'
                            copyboard[row - 1][col] = '.'
                            if row - 2 == 0:
                                copyboard[row - 2][col] = '$'
                            else:
                                copyboard[row - 2][col] = 'B'
                            pikachu_successors.append(copyboard)

                    # 1 step forward normal
                    if row > 0:
                        if board[row - 1][col] == '.':
                            copyboard = copy.deepcopy(board)
                            copyboard[row][col] = '.'
                            if row - 1 == 0:
                                copyboard[row - 1][col] = '$'
                            else:
                                copyboard[row - 1][col] = 'B'
                            pikachu_successors.append(copyboard)

                    # Left Movement

                    # 3 steps left jump when taking opponent piece
                    if col > 2:
                        # Taking white pieces v1
                        if board[row][col - 1] == '.' and board[row][col - 2] in ('w', 'W') and \
                                board[row][col - 3] == '.':
                            copyboard = copy.deepcopy(board)
                            copyboard[row][col] = '.'
                            copyboard[row][col - 1] = '.'
                            copyboard[row][col - 2] = '.'
                            copyboard[row][col - 3] = 'B'
                            pikachu_successors.append(copyboard)
                        # Taking white pieces v2
                        if board[row][col - 1] in ('w', 'W') and board[row][col - 2] == '.' and \
                                board[row][
                                    col - 3] == '.':
                            copyboard = copy.deepcopy(board)
                            copyboard[row][col] = '.'
                            copyboard[row][col - 1] = '.'
                            copyboard[row][col - 2] = '.'
                            copyboard[row][col - 3] = 'B'
                            pikachu_successors.append(copyboard)

                    # 2 step left jump when taking opponents piece
                    if col > 1:
                        # Taking white pieces
                        if board[row][col - 1] in ('w', 'W') and board[row][col - 2] == '.':
                            copyboard = copy.deepcopy(board)
                            copyboard[row][col] = '.'
                            copyboard[row][col - 1] = '.'
                            copyboard[row][col - 2] = 'B'
                            pikachu_successors.append(copyboard)

                        # Normal 2 step left move
                        if board[row][col - 1] == '.' and board[row][col - 2] == '.':
                            copyboard = copy.deepcopy(board)
                            copyboard[row][col] = '.'
                            copyboard[row][col - 1] = '.'
                            copyboard[row][col - 2] = 'B'
                            pikachu_successors.append(copyboard)

                    # 1 step left normal
                    if col > 0:
                        if board[row][col - 1] == '.':
                            copyboard = copy.deepcopy(board)
                            copyboard[row][col] = '.'
                            copyboard[row][col - 1] = 'B'
                            pikachu_successors.append(copyboard)

                    # Right Movement

                    # 3 steps right jump when taking opponent piece
                    if col < len(board) - 3:
                        # Taking white pieces v1
                        if board[row][col + 1] == '.' and board[row][col + 2] in ('w', 'W') and \
                                board[row][
                                    col + 3] == '.':
                            copyboard = copy.deepcopy(board)
                            copyboard[row][col] = '.'
                            copyboard[row][col + 1] = '.'
                            copyboard[row][col + 2] = '.'
                            copyboard[row][col + 3] = 'B'
                            pikachu_successors.append(copyboard)
                        # Taking white pieces v2
                        if board[row][col + 1] in ('w', 'W') and board[row][col + 2] == '.' and \
                                board[row][
                                    col + 3] == '.':
                            copyboard = copy.deepcopy(board)
                            copyboard[row][col] = '.'
                            copyboard[row][col + 1] = '.'
                            copyboard[row][col + 2] = '.'
                            copyboard[row][col + 3] = 'B'
                            pikachu_successors.append(copyboard)

                    # 2 step right jump when taking opponents piece
                    if col < len(board) - 2:
                        # Taking white pieces
                        if board[row][col + 1] in ('w', 'W') and board[row][col + 2] == '.':
                            copyboard = copy.deepcopy(board)
                            copyboard[row][col] = '.'
                            copyboard[row][col + 1] = '.'
                            copyboard[row][col + 2] = 'B'
                            pikachu_successors.append(copyboard)

                        # Normal 2 step right move
                        if board[row][col + 1] == '.' and board[row][col + 2] == '.':
                            copyboard = copy.deepcopy(board)
                            copyboard[row][col] = '.'
                            copyboard[row][col + 1] = '.'
                            copyboard[row][col + 2] = 'B'
                            pikachu_successors.append(copyboard)

                    # 1 step right normal
                    if col < len(board) - 1:
                        if board[row][col + 1] == '.':
                            copyboard = copy.deepcopy(board)
                            copyboard[row][col] = '.'
                            copyboard[row][col + 1] = 'B'
                            pikachu_successors.append(copyboard)

    return pikachu_successors


# All successors for Raichu moves
def raichu(board,player):
    raichu_successors = []
    if player == 'w':
        for row in range(len(board)):
            for col in range(len(board)):
                # if its a raichu
                if board[row][col] == '@':
                    # Move backward (down the board)
                    for i in range(row+1,len(board)):
                        copyboard = copy.deepcopy(board)
                        if copyboard[i][col] in ('w','W','@'):
                            break
                        if copyboard[i][col] in ('b','B','$') and i < len(board) -1:
                            if copyboard[i+1][col] == '.':
                                copyboard[row][col] = '.'
                                copyboard[i][col] = '.'
                                copyboard[i+1][col] = '@'
                                raichu_successors.append(copyboard)
                                for x in range(i+2,len(board)):
                                    copyboard2 = copy.deepcopy(copyboard)
                                    if copyboard2[x][col] == '.':
                                        copyboard2[i+1][col] = '.'
                                        copyboard2[x][col] = '@'
                                        raichu_successors.append(copyboard2)
                                    else:
                                        break
                            else:
                                break
                            break
                        if copyboard[i][col] == '.':
                            copyboard[i][col] = '@'
                            copyboard[row][col] = '.'
                            raichu_successors.append(copyboard)

                    # Move forward (up the board)
                    for i in range(row-1,-1,-1):
                        copyboard = copy.deepcopy(board)
                        if copyboard[i][col] in ('w','W','@'):
                            break
                        if copyboard[i][col] in ('b', 'B', '$') and i > 0:
                            if copyboard[i - 1][col] == '.':
                                copyboard[row][col] = '.'
                                copyboard[i][col] = '.'
                                copyboard[i - 1][col] = '@'
                                raichu_successors.append(copyboard)
                                for x in range(i - 2, -1,-1):
                                    copyboard2 = copy.deepcopy(copyboard)
                                    if copyboard2[x][col] == '.':
                                        copyboard2[i - 1][col] = '.'
                                        copyboard2[x][col] = '@'
                                        raichu_successors.append(copyboard2)
                                    else:
                                        break
                            else:
                                break
                            break
                        if copyboard[i][col] == '.':
                            copyboard[i][col] = '@'
                            copyboard[row][col] = '.'
                            raichu_successors.append(copyboard)


                    # Move left
                    for i in range(col - 1, -1, -1):
                        copyboard = copy.deepcopy(board)
                        if copyboard[row][i] in ('w', 'W','@'):
                            break
                        if copyboard[row][i] in ('b', 'B', '$') and i > 0:
                            if copyboard[row][i-1] == '.':
                                copyboard[row][col] = '.'
                                copyboard[row][i] = '.'
                                copyboard[row][i-1] = '@'
                                raichu_successors.append(copyboard)
                                for x in range(i - 2, -1, -1):
                                    copyboard2 = copy.deepcopy(copyboard)
                                    if copyboard2[row][x] == '.':
                                        copyboard2[row][i-1] = '.'
                                        copyboard2[row][x] = '@'
                                        raichu_successors.append(copyboard2)
                                    else:
                                        break
                            else:
                                break
                            break
                        if copyboard[row][i] == '.':
                            copyboard[row][i] = '@'
                            copyboard[row][col] = '.'
                            raichu_successors.append(copyboard)

                    # Move right
                    for i in range(col + 1,len(board)):
                        copyboard = copy.deepcopy(board)
                        if copyboard[row][i] in ('w', 'W','@'):
                            break
                        if copyboard[row][i] in ('b', 'B', '$') and i < len(board)-1:
                            if copyboard[row][i + 1] == '.':
                                copyboard[row][col] = '.'
                                copyboard[row][i] = '.'
                                copyboard[row][i + 1] = '@'
                                raichu_successors.append(copyboard)
                                for x in range(i + 2,len(board)):
                                    copyboard2 = copy.deepcopy(copyboard)
                                    if copyboard2[row][x] == '.':
                                        copyboard2[row][i + 1] = '.'
                                        copyboard2[row][x] = '@'
                                        raichu_successors.append(copyboard2)
                                    else:
                                        break
                            else:
                                break
                            break
                        if copyboard[row][i] == '.':
                            copyboard[row][i] = '@'
                            copyboard[row][col] = '.'
                            raichu_successors.append(copyboard)


                    # Move backwards and diagonal right (down the board and diagonal right)
                    if col >= 0 and col < len(board) - 1 and row < len(board) - 1:
                        for r,c in zip(range(row+1,len(board)),range(col + 1, len(board))):
                            copyboard = copy.deepcopy(board)
                            if copyboard[r][c] in ('w', 'W', '@'):
                                break
                            if copyboard[r][c] in ('b', 'B', '$') and c < len(board) - 1 and r < len(board) - 1:
                                if copyboard[r+1][c + 1] == '.':
                                    copyboard[row][col] = '.'
                                    copyboard[r][c] = '.'
                                    copyboard[r+1][c + 1] = '@'
                                    raichu_successors.append(copyboard)
                                    for x,y in zip(range(r+2,len(board)),range(c + 2, len(board))):
                                        copyboard2 = copy.deepcopy(copyboard)
                                        if copyboard2[x][y] == '.':
                                            copyboard2[r+1][c + 1] = '.'
                                            copyboard2[x][y] = '@'
                                            raichu_successors.append(copyboard2)
                                        else:
                                            break
                                else:
                                    break
                                break
                            if copyboard[r][c] == '.':
                                copyboard[r][c] = '@'
                                copyboard[row][col] = '.'
                                raichu_successors.append(copyboard)


                    # Move backwards and diagonal left (down the board and diagonal left)
                    if col > 0 and col <= len(board) - 1 and row < len(board)-1:
                        for r, c in zip(range(row + 1, len(board)), range(col - 1, -1,-1)):
                            copyboard = copy.deepcopy(board)
                            if copyboard[r][c] in ('w', 'W', '@'):
                                break
                            if copyboard[r][c] in ('b', 'B', '$') and c > 0 and r < len(board)-1:
                                if copyboard[r + 1][c - 1] == '.':
                                    copyboard[row][col] = '.'
                                    copyboard[r][c] = '.'
                                    copyboard[r + 1][c - 1] = '@'
                                    raichu_successors.append(copyboard)
                                    for x, y in zip(range(r + 2, len(board)), range(c - 2, -1,-1)):
                                        copyboard2 = copy.deepcopy(copyboard)
                                        if copyboard2[x][y] == '.':
                                            copyboard2[r + 1][c - 1] = '.'
                                            copyboard2[x][y] = '@'
                                            raichu_successors.append(copyboard2)
                                        else:
                                            break
                                else:
                                    break
                                break
                            if copyboard[r][c] == '.':
                                copyboard[r][c] = '@'
                                copyboard[row][col] = '.'
                                raichu_successors.append(copyboard)


                    # Move forward and diagonal right (up the board and diagonal right)
                    if col >= 0 and col < len(board) - 1 and row > 0:
                        for r, c in zip(range(row - 1, -1,-1), range(col + 1,len(board))):
                            copyboard = copy.deepcopy(board)
                            if copyboard[r][c] in ('w', 'W', '@'):
                                break
                            if copyboard[r][c] in ('b', 'B', '$') and c < len(board) - 1 and r > 0:
                                if copyboard[r - 1][c + 1] == '.':
                                    copyboard[row][col] = '.'
                                    copyboard[r][c] = '.'
                                    copyboard[r - 1][c + 1] = '@'
                                    raichu_successors.append(copyboard)
                                    for x, y in zip(range(r - 2, -1,-1), range(c + 2, len(board))):
                                        copyboard2 = copy.deepcopy(copyboard)
                                        if copyboard2[x][y] == '.':
                                            copyboard2[r - 1][c + 1] = '.'
                                            copyboard2[x][y] = '@'
                                            raichu_successors.append(copyboard2)
                                        else:
                                            break
                                else:
                                    break
                                break
                            if copyboard[r][c] == '.':
                                copyboard[r][c] = '@'
                                copyboard[row][col] = '.'
                                raichu_successors.append(copyboard)

                    # Move forward and diagonal left (up the board and diagonal left)
                    if col > 0 and col <= len(board) - 1 and row > 0:
                        for r, c in zip(range(row - 1, -1, -1), range(col - 1, -1,-1)):
                            copyboard = copy.deepcopy(board)
                            if copyboard[r][c] in ('w', 'W', '@'):
                                break
                            if copyboard[r][c] in ('b', 'B', '$') and c > 0 and r < len(board)-1:
                                if copyboard[r - 1][c - 1] == '.':
                                    copyboard[row][col] = '.'
                                    copyboard[r][c] = '.'
                                    copyboard[r - 1][c - 1] = '@'
                                    raichu_successors.append(copyboard)
                                    for x, y in zip(range(r - 2, -1,-1), range(c - 2, -1,-1)):
                                        copyboard2 = copy.deepcopy(copyboard)
                                        if copyboard2[x][y] == '.':
                                            copyboard2[r - 1][c - 1] = '.'
                                            copyboard2[x][y] = '@'
                                            raichu_successors.append(copyboard2)
                                        else:
                                            break
                                else:
                                    break
                                break
                            if copyboard[r][c] == '.':
                                copyboard[r][c] = '@'
                                copyboard[row][col] = '.'
                                raichu_successors.append(copyboard)


    else:
        for row in range(len(board)):
            for col in range(len(board)):
                # if its a raichu
                if board[row][col] == '$':
                    # Move backward (down the board)
                    for i in range(row+1,len(board)):
                        copyboard = copy.deepcopy(board)
                        if copyboard[i][col] in ('b','B','$'):
                            break
                        if copyboard[i][col] in ('w','W','@') and i < len(board) -1:
                            if copyboard[i+1][col] == '.':
                                copyboard[row][col] = '.'
                                copyboard[i][col] = '.'
                                copyboard[i+1][col] = '$'
                                raichu_successors.append(copyboard)
                                for x in range(i+2,len(board)):
                                    copyboard2 = copy.deepcopy(copyboard)
                                    if copyboard2[x][col] == '.':
                                        copyboard2[i+1][col] = '.'
                                        copyboard2[x][col] = '$'
                                        raichu_successors.append(copyboard2)
                                    else:
                                        break
                            else:
                                break
                            break
                        if copyboard[i][col] == '.':
                            copyboard[i][col] = '$'
                            copyboard[row][col] = '.'
                            raichu_successors.append(copyboard)

                    # Move forward (up the board)
                    for i in range(row-1,-1,-1):
                        copyboard = copy.deepcopy(board)
                        if copyboard[i][col] in ('b','B','$'):
                            break
                        if copyboard[i][col] in ('w', 'W', '@') and i > 0:
                            if copyboard[i - 1][col] == '.':
                                copyboard[row][col] = '.'
                                copyboard[i][col] = '.'
                                copyboard[i - 1][col] = '$'
                                raichu_successors.append(copyboard)
                                for x in range(i - 2, -1,-1):
                                    copyboard2 = copy.deepcopy(copyboard)
                                    if copyboard2[x][col] == '.':
                                        copyboard2[i - 1][col] = '.'
                                        copyboard2[x][col] = '$'
                                        raichu_successors.append(copyboard2)
                                    else:
                                        break
                            else:
                                break
                            break
                        if copyboard[i][col] == '.':
                            copyboard[i][col] = '$'
                            copyboard[row][col] = '.'
                            raichu_successors.append(copyboard)


                    # Move left
                    for i in range(col - 1, -1, -1):
                        copyboard = copy.deepcopy(board)
                        if copyboard[row][i] in ('b', 'B','$'):
                            break
                        if copyboard[row][i] in ('w', 'W', '@') and i > 0:
                            if copyboard[row][i-1] == '.':
                                copyboard[row][col] = '.'
                                copyboard[row][i] = '.'
                                copyboard[row][i-1] = '$'
                                raichu_successors.append(copyboard)
                                for x in range(i - 2, -1, -1):
                                    copyboard2 = copy.deepcopy(copyboard)
                                    if copyboard2[row][x] == '.':
                                        copyboard2[row][i-1] = '.'
                                        copyboard2[row][x] = '$'
                                        raichu_successors.append(copyboard2)
                                    else:
                                        break
                            else:
                                break
                            break
                        if copyboard[row][i] == '.':
                            copyboard[row][i] = '$'
                            copyboard[row][col] = '.'
                            raichu_successors.append(copyboard)

                    # Move right
                    for i in range(col + 1,len(board)):
                        copyboard = copy.deepcopy(board)
                        if copyboard[row][i] in ('b', 'B','$'):
                            break
                        if copyboard[row][i] in ('w', 'W', '@') and i < len(board)-1:
                            if copyboard[row][i + 1] == '.':
                                copyboard[row][col] = '.'
                                copyboard[row][i] = '.'
                                copyboard[row][i + 1] = '$'
                                raichu_successors.append(copyboard)
                                for x in range(i + 2,len(board)):
                                    copyboard2 = copy.deepcopy(copyboard)
                                    if copyboard2[row][x] == '.':
                                        copyboard2[row][i + 1] = '.'
                                        copyboard2[row][x] = '$'
                                        raichu_successors.append(copyboard2)
                                    else:
                                        break
                            else:
                                break
                            break
                        if copyboard[row][i] == '.':
                            copyboard[row][i] = '$'
                            copyboard[row][col] = '.'
                            raichu_successors.append(copyboard)


                    # Move backwards and diagonal right (down the board and diagonal right)
                    if col >= 0 and col < len(board) - 1 and row < len(board)-1:
                        for r,c in zip(range(row+1,len(board)),range(col + 1, len(board))):
                            copyboard = copy.deepcopy(board)
                            if copyboard[r][c] in ('b', 'B', '$'):
                                break
                            if copyboard[r][c] in ('w', 'W', '@') and c < len(board) - 1 and r < len(board) - 1:
                                if copyboard[r+1][c + 1] == '.':
                                    copyboard[row][col] = '.'
                                    copyboard[r][c] = '.'
                                    copyboard[r+1][c + 1] = '$'
                                    raichu_successors.append(copyboard)
                                    for x,y in zip(range(r+2,len(board)),range(c + 2, len(board))):
                                        copyboard2 = copy.deepcopy(copyboard)
                                        if copyboard2[x][y] == '.':
                                            copyboard2[r+1][c + 1] = '.'
                                            copyboard2[x][y] = '$'
                                            raichu_successors.append(copyboard2)
                                        else:
                                            break
                                else:
                                    break
                                break
                            if copyboard[r][c] == '.':
                                copyboard[r][c] = '$'
                                copyboard[row][col] = '.'
                                raichu_successors.append(copyboard)


                    # Move backwards and diagonal left (down the board and diagonal left)
                    if col > 0 and col <= len(board) - 1 and row < len(board) - 1:
                        for r, c in zip(range(row + 1, len(board)), range(col - 1, -1,-1)):
                            copyboard = copy.deepcopy(board)
                            if copyboard[r][c] in ('b', 'B', '$'):
                                break
                            if copyboard[r][c] in ('w', 'W', '@') and c > 0 and r < len(board)-1:
                                if copyboard[r + 1][c - 1] == '.':
                                    copyboard[row][col] = '.'
                                    copyboard[r][c] = '.'
                                    copyboard[r + 1][c - 1] = '$'
                                    raichu_successors.append(copyboard)
                                    for x, y in zip(range(r + 2, len(board)), range(c - 2, -1,-1)):
                                        copyboard2 = copy.deepcopy(copyboard)
                                        if copyboard2[x][y] == '.':
                                            copyboard2[r + 1][c - 1] = '.'
                                            copyboard2[x][y] = '$'
                                            raichu_successors.append(copyboard2)
                                        else:
                                            break
                                else:
                                    break
                                break
                            if copyboard[r][c] == '.':
                                copyboard[r][c] = '$'
                                copyboard[row][col] = '.'
                                raichu_successors.append(copyboard)


                    # Move forward and diagonal right (up the board and diagonal right)
                    if col >= 0 and col < len(board) - 1 and row > 0:
                        for r, c in zip(range(row - 1, -1,-1), range(col + 1,len(board))):
                            copyboard = copy.deepcopy(board)
                            if copyboard[r][c] in ('b', 'B', '$'):
                                break
                            if copyboard[r][c] in ('w', 'W', '@') and c < len(board) - 1 and r > 0:
                                if copyboard[r - 1][c + 1] == '.':
                                    copyboard[row][col] = '.'
                                    copyboard[r][c] = '.'
                                    copyboard[r - 1][c + 1] = '$'
                                    raichu_successors.append(copyboard)
                                    for x, y in zip(range(r - 2, -1,-1), range(c + 2, len(board))):
                                        copyboard2 = copy.deepcopy(copyboard)
                                        if copyboard2[x][y] == '.':
                                            copyboard2[r - 1][c + 1] = '.'
                                            copyboard2[x][y] = '$'
                                            raichu_successors.append(copyboard2)
                                        else:
                                            break
                                else:
                                    break
                                break
                            if copyboard[r][c] == '.':
                                copyboard[r][c] = '$'
                                copyboard[row][col] = '.'
                                raichu_successors.append(copyboard)

                    # Move forward and diagonal left (up the board and diagonal left)
                    if col > 0 and col <= len(board) - 1 and row > 0:
                        for r, c in zip(range(row - 1, -1, -1), range(col - 1, -1, -1)):
                            copyboard = copy.deepcopy(board)
                            if copyboard[r][c] in ('b', 'B', '$'):
                                break
                            if copyboard[r][c] in ('w', 'W', '@') and c > 0 and r < len(board)-1:
                                if copyboard[r - 1][c - 1] == '.':
                                    copyboard[row][col] = '.'
                                    copyboard[r][c] = '.'
                                    copyboard[r - 1][c - 1] = '$'
                                    raichu_successors.append(copyboard)
                                    for x, y in zip(range(r - 2, -1,-1), range(c - 2, -1,-1)):
                                        copyboard2 = copy.deepcopy(copyboard)
                                        if copyboard2[x][y] == '.':
                                            copyboard2[r - 1][c - 1] = '.'
                                            copyboard2[x][y] = '$'
                                            raichu_successors.append(copyboard2)
                                        else:
                                            break
                                else:
                                    break
                                break
                            if copyboard[r][c] == '.':
                                copyboard[r][c] = '$'
                                copyboard[row][col] = '.'
                                raichu_successors.append(copyboard)


    return raichu_successors


# Combine all successors
def successors(board,player):
    return pichu(board, player) + pikachu(board, player) + raichu(board,player)


# Create heuristic evaluation function
def eval(board):
    # Count number of pieces for each player
    w_pichu = 0
    w_pikachu = 0
    w_raichu = 0
    b_pichu = 0
    b_pikachu = 0
    b_raichu = 0

    for row in board:
        for piece in row:
            if piece == 'w':
                w_pichu += 1
            if piece == 'W':
                w_pikachu += 1
            if piece == '@':
                w_raichu += 1
            if piece == 'b':
                b_pichu += 1
            if piece == 'B':
                b_pikachu += 1
            if piece == '$':
                b_raichu += 1

    # Evaluation function - 1 multiplier for pichu pieces, 5 multiplier for pikachu pieces,
    # 15 multiplier for raichu pieces, 0.1 multiplier for total # of possible next moves
    # total # of possible moves causes runtime issues with boards that are heavily populated with raichus (due to successor counts)
    if player == 'w':
        #if 1*(w_pichu - b_pichu) + 5*(w_pikachu - b_pikachu) + 15*(w_raichu - b_raichu) > 0:
        return 1*(w_pichu - b_pichu) + 5*(w_pikachu - b_pikachu) + 15*(w_raichu - b_raichu) + .1* (len(successors(board,'w')) - len(successors(board,'b')))
        #else:
        #    return 1*(w_pichu - b_pichu) + 5*(w_pikachu - b_pikachu) + 15*(w_raichu - b_raichu) + .1* (len(successors(board,'w')) - len(successors(board,'b')))
    else:
        #if 1 * (b_pichu - w_pichu) + 5 * (b_pikachu - w_pikachu) + 15 * (b_raichu - w_raichu) < 0:
        return 1 * (b_pichu - w_pichu) + 5 * (b_pikachu - w_pikachu) + 15 * (b_raichu - w_raichu) + .1 * (len(successors(board, 'b')) - len(successors(board, 'w')))
        #else:
        #    return 1 * (b_pichu - w_pichu) + 5 * (b_pikachu - w_pikachu) + 15 * (b_raichu - w_raichu) + .1 * (len(successors(board, 'b')) - len(successors(board, 'w')))

# Add evaluation function to successor states
def successors_with_eval(successors):
    successor_list = []
    for succ in successors:
        heuristic = eval(succ)
        successor_list.append([heuristic,heuristic,succ])

    return successor_list


# check if we're in a winning state
def goal(board):
    # Count number of pieces for each player
    w_pichu = 0
    w_pikachu = 0
    w_raichu = 0
    b_pichu = 0
    b_pikachu = 0
    b_raichu = 0

    for row in board:
        for piece in row:
            if piece == 'w':
                w_pichu += 1
            if piece == 'W':
                w_pikachu += 1
            if piece == '@':
                w_raichu += 1
            if piece == 'b':
                b_pichu += 1
            if piece == 'B':
                b_pikachu += 1
            if piece == '$':
                b_raichu += 1

    if player == 'w' and (b_pichu + b_pikachu + b_raichu == 0):
        return True
    if player == 'b' and (w_pichu + w_pikachu + w_raichu == 0):
        return True
    else:
        return False


# Max player
def max_value(board,depth,max_depth):
    depth = depth + 1
    if depth >= max_depth:
        return eval(board[2])
    succ = successors_with_eval(successors(board[2],player))
    for s in succ:
        board[0] = max(board[0],min_value(s,depth,max_depth))
        if board[0] >= board[1]:
            return board

    return board



# Min player
def min_value(board,depth,max_depth):
    depth = depth + 1
    if depth == max_depth:
        return eval(board[2])
    succ = successors_with_eval(successors(board[2],player))
    for s in succ:
        board[1] = min(board[1],max_value(s,depth+1,max_depth))
        if board[0] >= board[1]:
            return board

    return board


# alpha beta
def alpha_beta(initial_vals):
    succ = successors_with_eval(successors(initial_vals[2],player))
    vals = []
    for s in succ:
        vals.append(min_value(s,0,initial_vals[3]))

    # Sort values and return the maximum
    vals.sort()

    return vals[-1]



def find_best_move(board, N, player, timelimit):
    alpha = float(inf)
    beta = float(-inf)
    max_depth = 3
    board_init = board_to_list(board,N)
    initial_vals = [alpha, beta, board_init, max_depth]

    while True:
        solutions = alpha_beta(initial_vals)[2]
        delim = ''
        for board in solutions:
            delim = delim + ''.join(board)

        yield delim



if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise Exception("Usage: Raichu.py N player board timelimit")
        
    (_, N, player, board, timelimit) = sys.argv
    N=int(N)
    timelimit=int(timelimit)
    if player not in "wb":
        raise Exception("Invalid player.")

    if len(board) != N*N or 0 in [c in "wb.WB@$" for c in board]:
        raise Exception("Bad board string.")


    print("Searching for best move for " + player + " from board state: \n" + board_to_string(board, N))
    print("Here's what I decided:")
    for new_board in find_best_move(board, N, player, timelimit):
        print(new_board)
