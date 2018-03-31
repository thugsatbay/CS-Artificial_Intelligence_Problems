#!/usr/bin/env python

import os
import sys

from chess_state import GameState
from pichuAI import pichuAI as PAI

def printLogo():
    if os.path.isfile('pichu.txt'):
        with open('pichu.txt', 'r') as f:
            for index, line in enumerate(f):
                if index:
                    print line
        print ''

'''
sys take input arguments,
let the time interval decide how much depth to go
FAST MODE = True
depth 4 = 1.5 secs
depth 5 = 12 secs
'''

if len(sys.argv) <= 3:
    print "Too few arguments"
else:
    FAST_MODE = True
    SEARCH_DEPTH = 4
    BOARD_STATE = str(sys.argv[2])
    PLAYER = str(sys.argv[1])
    TIME = int(sys.argv[3])
    if TIME >= 1 and TIME < 2:
        SEARCH_DEPTH = 3
    elif TIME >= 2 and TIME < 7:
        SEARCH_DEPTH = 4
    else:
        SEARCH_DEPTH = 5


    pichu = GameState(BOARD_STATE, PLAYER, FAST_MODE)
    pichu.printBoard()
    if not FAST_MODE:
        printLogo()
        pichu.printBoard()

    '''
    Depth = x, x-1 alternate chances explored,
    for x = 4, moves generated
        (1) max
        (2) min
        (3) max
        (4) heuristic calculated max, min returned based on above layer
    '''
    pichu_AI = PAI(
                    pichu,
                    PLAYER,
                    depth=SEARCH_DEPTH,
                    FAST_MODE=FAST_MODE
                )
    pichu_AI.findTheBestMove()
