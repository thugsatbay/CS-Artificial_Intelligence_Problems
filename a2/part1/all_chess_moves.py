from math import atan2
from copy import deepcopy

'''
MOVEMENT & MOVEMENT_ANGLES
store information regarding all possible movements by pieces and the angles 
made by them when making the moves
'''
MOVEMENT = [    
                (-1, -1), # dig up left
                (-1, 0), # up
                (-1, 1), # dig up right
                (0, 1), # right
                (1, 1), # dig down right
                (1, 0), # down
                (1, -1), # dig down left
                (0, -1), # left
                (-1, -2), # horse 1-2 up left
                (-1, 2), # horse 1-2 up right
                (1, 2), # horse 1-2 down right
                (1, -2), # horse 1-2 down left
                (-2, -1), # horse 2-1 up left
                (-2, 1), # horse 2-1 up right
                (2, 1), # horse 2-1 down right
                (2, -1) # horse 2-1 down left
           ]
MOVEMENT_ANGLES = [atan2(move[0], move[1]) for move in MOVEMENT]

def robinLegalMove(dr, dc, r):
    return not dr or not dc

def blueLegalMove(dr, dc, r):
    return abs(dr) == abs(dc)

def quetzalLegalMove(dr, dc, r):
    return blueLegalMove(dr, dc, r) or robinLegalMove(dr, dc, r)

def kingfisherLegalMove(dr, dc, r):
    return abs(dr) <= 1 and abs(dc) <= 1

def nightHawkLegalMove(dr, dc, r):
    return (abs(dr) == 1 and abs(dc) == 2) or (abs(dr) == 2 and abs(dc) == 1)

def parakeetWhiteLegalMove(dr, dc, r):
    return abs(dc) <= 1 and dr == 1 and r > 0

def parakeetBlackLegalMove(dr, dc, r):
    return abs(dc) <= 1 and dr == -1 and r < 7

'''
Function call for checking legal moves of all pieces
'''
LEGAL_MOVES_FOR_PIECES = {
                            'r' : robinLegalMove,
                            'b' : blueLegalMove,
                            'q' : quetzalLegalMove,
                            'k' : kingfisherLegalMove,
                            'n' : nightHawkLegalMove,
                            'P' : parakeetWhiteLegalMove,
                            'p' : parakeetBlackLegalMove
                         }

'''
DIRECTION_DIC 
X is the point where you are and 1,2 ... 8 represent all the directions in
which you can move from point X
Example:
0 1 2
7 X 3
6 5 4  
'''
DIRECTION_DIC = {
                    0 : [], 
                    1 : [],
                    2 : [],
                    3 : [],
                    4 : [],
                    5 : [],
                    6 : [],
                    7 : []
                }

PARAKEET = ['p', 'P']

ALL_CHESS_MOVES = {}

for piece, legal_function in LEGAL_MOVES_FOR_PIECES.items():
    
    # For a given piece
    ALL_CHESS_MOVES[piece] = {}
    
    for pos_index in xrange(64):
        
        # For a given piece and location on board
        ALL_CHESS_MOVES[piece][pos_index] = deepcopy(DIRECTION_DIC)

        original_r, original_c = int(pos_index / 8), pos_index % 8

        '''
        Store the moves in sorted order with respect to pos_index

        3 3 3 3 3 3
        2 2 2 2 2 3
        2 1 1 1 2 3
        2 1 X 1 2 3
        2 1 1 1 2 3
        2 2 2 2 2 3 
        3 3 3 3 3 3
        
        Where X is pos_index and the boundaries are the difference between that
        position(pos_relative_to_index) and pos_index

        Terminal Condition:
            -Your player knocks another player
            -Your player movement is impeded by some other piece that is yours
        
        This will allow to clip moves easily once a terminal condition is met
        '''
        for pos_relative_to_index in sorted(range(64), key=lambda k : abs(k - pos_index)):

            # No move can be played since same location as starting point
            if pos_relative_to_index == pos_index:
                continue

            new_r = int(pos_relative_to_index / 8)
            new_c = pos_relative_to_index % 8
            dr, dc = new_r - original_r, new_c - original_c

            # This does not seem to be a legal move of piece from pos_index
            if not LEGAL_MOVES_FOR_PIECES[piece](dr, dc, original_r):
                continue

            # The angle of the move should also match
            if atan2(dr, dc) in MOVEMENT_ANGLES:
                direction = MOVEMENT_ANGLES.index(atan2(dr, dc)) % 8
                ALL_CHESS_MOVES[piece][pos_index][direction].append(pos_relative_to_index)

'''
# This code has been patched in chess_state
for index, p in enumerate(PARAKEET):
    for all_pos in ALL_CHESS_MOVES[p]:
        if int(all_pos / 8) == 6 - (index * 5):
            value = ALL_CHESS_MOVES[p][all_pos][1 + (index * 4)][0]
            ALL_CHESS_MOVES[
                                p
                           ][
                                all_pos
                           ][
                                1 + (index * 4)
                            ].append(value + ((index - 1) * 8) + (index * 8))
'''

'''
# Test Code
print ALL_CHESS_MOVES['P'][9]
'''
