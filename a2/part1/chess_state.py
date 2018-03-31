# -*- coding: UTF-8 -*-
from collections import namedtuple as nt
from all_chess_moves import ALL_CHESS_MOVES as ACM
from all_chess_moves import PARAKEET

'''
CHESS PIECES UNICODE UTF-8
http://www.utf8-chartable.de/unicode-utf8-table.pl?start=9728&number=128&utf8=string-literal
'''
CHESS_PIECES = {
                  'R' : '♜',
                  'N' : '♞',
                  'B' : '♝',
                  'Q' : '♛',
                  'K' : '♚',
                  'P' : '♟',
                  'r' : '♖',
                  'n' : '♘',
                  'b' : '♗',
                  'q' : '♕',
                  'k' : '♔',
                  'p' : '♙',
                  '.' : '·'
               }

CHESS_PIECE_COUNT = {
                        'r' : 2,
                        'n' : 2,
                        'b' : 2,
                        'q' : 1,
                        'k' : 1,
                        'p' : 8
                    }

CHANGE_PLAYER = {
                    'b' : 'w',
                    'w' : 'b'
                }

ChessMove = nt('ChessMove', 'from_p to_p')

EMPTY_SPACE = '.'

class GameState():

    def __init__(self,
                 BOARD,
                 PLAYER=None,
                 FAST_MODE=False):

        self.BOARD = list(BOARD)
        self.updatePawns()
        self.PLAYER = PLAYER
        self.FAST_MODE = FAST_MODE
        self.WB_PIECES = {
                                'b' : {
                                        'r' : 0,
                                        'n' : 0,
                                        'b' : 0,
                                        'q' : 0,
                                        'k' : 0,
                                        'p' : 0,
                                        },
                                'w' : {
                                        'R' : 0,
                                        'N' : 0,
                                        'B' : 0,
                                        'Q' : 0,
                                        'K' : 0,
                                        'P' : 0
                                      }
                             }
        if not self.FAST_MODE:
            self.FEN = None
            self.inputStateToFen()

    def updatePawns(self):
        for index in xrange(0,8):
            # 'p'
            if self.BOARD[index] == PARAKEET[0]:
                self.BOARD[index] = 'q'

        for index in xrange(56, 64):
            # 'P'
            if self.BOARD[index] == PARAKEET[1]:
                self.BOARD[index] = 'Q'

    def makeBoard(self):
        '''
        Gets Info of the board
        '''
        for k in self.WB_PIECES:
            for p in self.WB_PIECES[k]:
                self.WB_PIECES[k][p] = 0

        for piece in self.BOARD:
            if piece == '.':
                continue

            if piece.islower():
                self.WB_PIECES['b'][piece] += 1
                continue

            self.WB_PIECES['w'][piece] += 1
        return self.WB_PIECES

    # TODO(gdhody) try optimize this
    def inputStateToFen(self):
        '''
        Convert this state
        rnbqkbnrpppppppp................................PPPPPPPPRNBQKBNR
        To FEN compact state
        rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
        '''

        self.FEN = ''
        for ind in xrange(8):
            count = 0
            for each in self.BOARD[ind * 8: (ind + 1) * 8]:
                if each == '.':
                    count += 1
                else:
                    if count:
                        self.FEN += str(count)
                        count = 0
                    self.FEN += each
            if count:
                self.FEN += str(count)
            self.FEN += '/'
        self.FEN = self.FEN[:-1]

    def printBoard(self):
        '''
        Prints a board on console for the following board state
        RNBQKBNRPPPPPPPP................................pppppppprnbqkbnr
        8 ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜
        7 ♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟
        6 · · · · · · · ·
        5 · · · · · · · ·
        4 · · · · · · · ·
        3 · · · · · · · ·
        2 ♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙
        1 ♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖
          a b c d e f g h
        '''

        if not self.FAST_MODE:
            for row_ind in xrange(8):
                print str(8 - row_ind) + \
                    ' ' + \
                    ' '.join(map(
                                    lambda x : CHESS_PIECES[x],
                                    self.BOARD[row_ind * 8 : (row_ind + 1) * 8]
                                ))
            print '  ' + ' '.join([chr(ord('a') + val) for val in xrange(8)])
        print "".join(self.BOARD)

    def isKingDead(self):
        if 'k' in self.BOARD and 'K' in self.BOARD:
            return False
        if 'k' in self.BOARD:
            return 'b'
        if 'K' in self.BOARD:
            return 'w'

    def returnPlayer(self):
        return self.PLAYER

    def returnBoard(self):
        return self.BOARD[:]

    def getPieceAtIndex(self, index):
        return self.BOARD[index]

    def getPieceInfoAtIndex(self, index):
        return self.getPieceInfo(self.getPieceAtIndex(index))

    def getPieceInfo(self, piece):
        if piece != '.':
            return 'w' if piece.isupper() else 'b'
        return False

    def convertCMToI2CC(self, move):
        return self.index2ChessCoord(move.from_p), self.index2ChessCoord(move.to_p)

    def index2ChessCoord(self, index):
        return str(chr(ord('a') + (index % 8))) + str(8 - int(index / 8))

    def findAllValidMoves(self, player=None):

        # Can be explicitly called for any player
        if not player:
            player = self.PLAYER

        # All possible valid moves on current board
        valid_moves = {}

        # Iterate over all positions on board
        for idx in xrange(64):

            # Only the player can make moves otherwise skip
            piece = self.BOARD[idx]
            piecePlayer = self.getPieceInfo(piece)
            if not piecePlayer or not piecePlayer == player:
                continue

            valid_moves[idx] = set([])

            # ACM contains piece info in lower case except for parakeet
            if piece not in PARAKEET:
                piece = piece.lower()

            # Go over all moves the piece can play
            for direction, direction_moves in ACM[piece][idx].items():

                # Go over each move in a given direction
                for piece_move in direction_moves:

                    #TODO(gdhody) Extra condition for parakeet

                    # Potential move, board position info
                    moveInfo = self.getPieceInfo(self.BOARD[piece_move])

                    # Moves for parakeet players are different as they have more
                    # restricted moves
                    if piece not in PARAKEET:

                        # The given move cannot land on the same player
                        if moveInfo == player:
                            break

                        valid_moves[idx].add(piece_move)

                        # The move knocked the opponent, clip movement
                        if moveInfo:
                            break

                    else:
                        # 0,p and 1,P
                        ind_p = PARAKEET.index(piece)

                        # Parakeet diagonal moves allowed if enemy player cut
                        if direction in [0 + (4 * ind_p), 2 + (4 * ind_p)]:
                            if moveInfo and moveInfo != player:
                                valid_moves[idx].add(piece_move)

                        # Parakeet player forward move if space open
                        elif direction == 1 + (4 * ind_p):
                            if not moveInfo:
                                valid_moves[idx].add(piece_move)

                                # Parakeet first move 2 jumps allowed only if
                                # the position is empty
                                if (idx / 8) == 6 - (5 * ind_p):
                                    para_2_new_pos = piece_move + \
                                                        (8 * (ind_p - 1)) + \
                                                        (8 * ind_p)
                                    para_2_move = self.getPieceInfo(
                                                    self.BOARD[para_2_new_pos])
                                    valid_moves[idx].add(para_2_new_pos)

        # Return moves in ChessMove named tuple
        if self.FAST_MODE:
            valid_moves = [
                            ChessMove(from_p=start, to_p=move)
                            for start, end in valid_moves.items()
                            for move in list(end)
                            if end
                          ]
            return (valid_moves,)
        valid_moves_pass = [
                                ChessMove(from_p=start, to_p=move)
                                for start, end in valid_moves.items()
                                for move in list(end)
                                if end
                           ]
        return (valid_moves_pass, [
                                [(
                                    self.index2ChessCoord(start),
                                    self.index2ChessCoord(move)
                                 ) for move in list(end)]
                                for start, end in valid_moves.items()
                            ])

    def makeAMove(self, move):
        # Make the move and return the new generated game state
        copy_of_board = self.BOARD[:]
        copy_of_board[move.to_p] = copy_of_board[move.from_p]
        copy_of_board[move.from_p] = EMPTY_SPACE
        return GameState(
                            "".join(copy_of_board),
                            CHANGE_PLAYER[self.PLAYER],
                            self.FAST_MODE
                        )

    def status(self):
        king = 'K'
        if self.PLAYER == 'b': king = 'k'
        king_position = self.BOARD.index(king)
        any_moves = len(self.findAllValidMoves()[0])
        king_danger_moves = [move for move in self.findAllValidMoves(CHANGE_PLAYER[self.PLAYER])[0]
                             if move.to_p == king_position]

        status_return = 0
        if king_danger_moves:
            status_return = 1
            if not any_moves: status_return = 2

        return status_return
