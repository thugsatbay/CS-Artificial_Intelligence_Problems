#!/usr/bin/env python
# Larry Gates
# Gurleen Dhody
# 15/Sept/2017

import copy
import sys
import Queue as Q

initial_board = []
# Needs to have 2 arguments.
if not len(sys.argv) == 2:
    print("Not enough arguments provided")
    exit()
fileName = sys.argv[1]

# Handles opening the file and filling the board
with open(fileName) as f:
    for line in f:
        initial_board.append(map(int, line.strip().split(' ')))

# Determine the n x n size board
n = int(len(initial_board))
# Generates the goal state board
goal_state = [[row*4 + (col+1) for col in xrange(n)] for row in xrange(n)]
goal_state[n-1][n-1] = 0

# Heuristic function
def heuristic(board, divisor=1.00):
    "Heuristic Function that best estimates the number of moves to the goal state. "
    cost = 0
    for row in xrange(n):
        for col in xrange(n):
            value = board[row][col]
            if value:
                goal_value_row = int(value / n) - 1
                if value % n:
                    goal_value_row = int(value / n)
                goal_value_col = (value - 1) % n
                cost += abs(goal_value_row - row) + abs(goal_value_col - col)
    return cost

# Generate Successor
def generateS(boardS):
    "Optimized successor generator for possible moves"
    board, moves, cost = boardS
    new_states_len = (n*2) - 2
    new_states = []
    cost_in = 1
    for row in xrange(n):
        for col in xrange(n):
            if not board[row][col]:
                for index in xrange(n):
                    if col != index:
                        new_states.append( [cost + cost_in, [copy.deepcopy(board), "", cost + cost_in]] )
                        given_new_state = new_states[-1][-1][0]
                        given_new_state_row = given_new_state[row]
                        del given_new_state_row[col]
                        given_new_state_row.insert(index, 0)
                        new_states[-1][0] += heuristic(given_new_state) / 3.0
                        left_or_right = "L"
                        if index < col:
                            left_or_right = "R"
                        new_states[-1][-1][1] = moves + "," + left_or_right + str(abs(index - col)) + str(row + 1)
                for index in xrange(n):
                    if row != index:
                        new_states.append( [cost + cost_in, [copy.deepcopy(board), "", cost + cost_in]] )
                        given_new_state = new_states[-1][-1][0]
                        for till_zero in xrange(row, index, -1):
                            given_new_state[till_zero][col] = given_new_state[till_zero - 1][col]
                        for after_zero in xrange(row, index, 1):
                            given_new_state[after_zero][col] = given_new_state[after_zero + 1][col]
                        given_new_state[index][col] = 0
                        new_states[-1][0] += heuristic(given_new_state) / 3.0
                        up_or_down = "U"
                        if index < row:
                            up_or_down = "D"
                        new_states[-1][-1][1] = moves + "," + up_or_down + str(abs(index - row)) + str(col + 1)

    return new_states

# Changes list to tuple
def makeListToTuple(array):
    "Converts list into a tuple"
    return tuple([tuple(row) for row in array])

# Check if boards are equivalent
def checkTwoBoardsAreSame(board1, board2=goal_state):
    "Checks if the given boards look the same"
    for row in xrange(n):
        for col in xrange(n):
            if board1[row][col] != board2[row][col]:
                return False
    return True

# Board Output
def printBoards(boards):
    "Prints the board into a human readible output"
    for board in boards:
        print board[1][2], '+', board[0] - board[1][2], '=', board[0]
        print board[1][1]
        for row in xrange(n):
            print board[1][0][row]
        print '--------------'

# Main search function. 
def runAStar():
    """
    A* Search\n
    Use Best First Search (Algorithm 2)\n
    f(s) = g(s) + h(s)\n
        \t- g(s) = cost of best path found so far to s
        \t- h(s) = admissible heuristic function
    \n\nBest First Search:\n
    if GOAL?(initial-state) then return initial-state\n
    INSERT(initial-node, FRINGE)\n
    REPEAT:\n
        \tif empty(FRINGE) the return failure\n
        \ts <- REMOVE(FRINGE)\n
        \tif GOAL?(s) the return s and/or path\n
        \tfor every state s' in SUCC(s):\n
            \t\tINSERT(s', FRINGE)\n
    Use priority queue to sort most promising results for the 
    successors. \n
    Evaluation function f(s) >= 0 that estimates the "cost" from 
    initial state, through s, to a goal state.
    """
    states = Q.PriorityQueue()
    states.put( (0, [initial_board, "", 0]) )
    visited, elements_in_state_space = {}, {}
    while not states.empty():
        current_node = states.get()
        # printBoards([current_node])
        current_node = current_node[1]
        if checkTwoBoardsAreSame(board1=current_node[0]):
            print current_node[1].replace(",", " ").strip()
            return 
        
        visited[makeListToTuple(current_node[0])] = current_node[2]
        for each_new_state in generateS(current_node):
            if makeListToTuple(each_new_state[-1][0]) in visited:
                continue

            states.put(tuple(each_new_state))
        #raw_input()

runAStar()
