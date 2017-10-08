#!/usr/bin/env python
# Gurleen Singh Dhody

import sys

class ChessBoard:
    ''' ChessBoard class to store chess state space. '''
    def __init__(self, N):
        self.board  = [[0 for _ in range(N)] for _ in range(N)]
        self.black_node = "X"

    def getBoardPiece(self, row_index, col_index):
        return self.board[row_index][col_index]

    def setBoardPiece(self, row_index, col_index):
        self.board[row_index][col_index] = 1

    def removeBoardPiece(self, row_index, col_index):
        self.board[row_index][col_index] = 0

    def setBlackPiece(self, row_index, col_index):
        self.board[row_index][col_index] = -1

    def printBoard(self):
        print self.board

    def outputBoard(self):
        print "\n".join([" ".join([policy if cell == 1 else "X" if cell else "_" for cell in row]) for row in self.board])


def findNewUnplayableNodes(row, col):
    ''' Invalidate nodes after given move on chess board. '''
    if (row, col) in dic_inv_state_space:
        return dic_inv_state_space[(row,col)]
    # Optimization done by removing/calculating unplayable nodes of rows above current level as queen only inserted in lower levels.
    # All rows below with same column index become inaccessible.
    new_list = [(_,col) for _ in range(row, N)]
    # All diagonals below the given state become inaccessible.
    if policy == "Q":
        new_list += [(r,c) for r,c in zip(range(row + 1, N, 1), range(col + 1, N, 1))] + [(r,c) for r,c in zip(range(row + 1, N, 1), range(col - 1, -1, -1))]
    dic_inv_state_space[(row, col)] = new_list
    return dic_inv_state_space[(row, col)]

def createWorkingChessBoard(board, unplayable_nodes, layer):
    ''' Insert a queen on each row and exit when donne returning True else return False if no valid placement found. '''
    if layer == N:
        return True
    # Backtrack try inserting a value.
    for cell in range(0, N, 1):
        if (layer,cell) not in unplayable_nodes and board.getBoardPiece(layer,cell) == 0:
            board.setBoardPiece(layer, cell)
            if createWorkingChessBoard(board, unplayable_nodes + findNewUnplayableNodes(layer, cell), layer + 1):
                return True
            board.removeBoardPiece(layer, cell)
    return False

def solution(black_piece_row_index, black_piece_col_index):
    ''' Initialize and run the algorithm. '''
    play_board = ChessBoard(N)
    unplayable_nodes = []
    if black_piece_col_index >= 0 and black_piece_col_index < N and black_piece_row_index < N and black_piece_row_index >= 0:
        play_board.setBlackPiece(black_piece_row_index, black_piece_col_index)
        unplayable_nodes.append((black_piece_row_index, black_piece_col_index))
    if createWorkingChessBoard(play_board, unplayable_nodes, 0):
        play_board.outputBoard()
        return
    print "no solution"

# Dictonary to store invalid moves based on given state.
dic_inv_state_space = {}

# Rooks or queen.
piece = sys.argv[1]
policy = "Q"
if piece == "nrook":
    policy = "R"

# Board size.
N = int(sys.argv[2])

# Dead cell index.
black_row_cord = int(sys.argv[3]) - 1
black_col_cord = int(sys.argv[4]) - 1
solution(black_row_cord, black_col_cord)
