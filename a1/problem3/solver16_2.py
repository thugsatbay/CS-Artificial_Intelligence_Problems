#!/usr/bin/env python
import sys
import Queue 

"""
A* Search
Use Best First Search (Algorithm 2)
f(s) = g(s) + h(s)
    - g(s) = cost of best path found so far to s
    - h(s) = admissible heuristic function
Best First Search:
IF GOAL?(initial-state) then return initial-state
INSERT(initial-node, FRINGE)
REPEAT:
    if empty(FRINGE) the return failure
    s <- REMOVE(FRINGE)
    if GOAL?(s) the return s and/or path
    for every state s' in SUCC(s):
        INSERT(s', FRINGE)
Use priority queue to sort most promising results for the 
successors. 
Evaluation function f(s) >= 0 that estimates the "cost" from 
initial state, through s, to a goal state.
"""
def parseFile(file):
    " Takes a given file and makes a 2-D array representing a board"
    # Code in between (---) lines from following: 
    # https://stackoverflow.com/questions/19056125/reading-a-file-into-a-multidimensional-array-with-python
    # --------------------------
    textFile = open(file)
    lines = textFile.readlines()
    mainList = []
    for line in lines:
        line = line.replace("\n", "") # Besides this one, had to look in documentation
        line = line.split(" ")
    # --------------------------
        subList = []
        for l in line:
            subList.append(int(l))
        mainList.append(subList)
        # print(line)
    return mainList

def misplaceCount(board):
    "Heurisitic function: Number of misplaced tiles"
    counter = 1
    misplaced = 0
    for r in board:
        for c in r:
            if not c == counter:
                misplaced = misplaced + 1
            counter = counter + 1

    return misplaced

def totalDistanceManhattan(board):
    "Finds the total manhattan distance"
    # FIXME: We need to handle distance based off if all moves are 1, including moving all 3
    totalDistance = 0
    for row in range(len(board)):
        for col in range(len(board[row])):
            boardValue = board[row][col]
            if  boardValue == 0:
                continue
            if not boardValue == (row * 4 + col)+1:
                wrongR = (boardValue - 1)/4
                wrongC = (boardValue - 1)%4
                totalDistance += abs(wrongR - row) + abs(wrongC - col)
    return totalDistance


def heuristicFunction(board):
    "Calls the desired heuristic function and returns the value"
    # return misplaceCount(board)
    return totalDistanceManhattan(board)

def makeListCopy(l):
    "Was having reference issues even though I thought I had fixed them"
    newL = []
    for item in l:
        newL.append(item)
    return newL

def makeBoardCopy(b):
    "Handles copying the board to be a deep copy"
    newB = []
    for r in b:
        t = []
        for c in r:
            t.append(c)
        newB.append(t)
    return newB

def successors(path):
    "Returns potential successors for given board"
    board = path[0]
    route = path[1]
    succesorList = []
    # don't forget to add the cost overall as time goes on 
    # Return the heuristic (cost, (board, path))

    # Finding the location of the zero
    r0 = -1
    c0 = -1
    for r in range(len(board)):
        for c in range(len(board[r])):
            if board[r][c] == 0:
                r0 = r
                c0 = c
        if not r0 == -1:
            break
    
    # Move the row
    # Move in different counts
    if r0 == 3:
        tempR = r0
        # Handle moving just 1
        
        tempBoard = makeBoardCopy(board)
        tempPath = makeListCopy(route)
        tempBoard[tempR][c0] = tempBoard[tempR - 1][c0]
        tempBoard[tempR-1][c0] = 0
        tempStr = "D1"+str(r0+1)
        tempPath.append(tempStr)
        tB = tempBoard[:]
        succesorList.append([heuristicFunction(tempBoard), [tB, tempPath]])
        # Handle moving just 2

        tempBoard = makeBoardCopy(tempBoard)
        tempPath = makeListCopy(route)
        tempR = tempR - 1
        tempBoard[tempR][c0] = tempBoard[tempR - 1][c0]
        tempBoard[tempR-1][c0] = 0
        tempStr = "D2"+str(r0+1)
        tempPath.append(tempStr)
        succesorList.append([heuristicFunction(tempBoard), [tempBoard, tempPath]])


        # Handle moving all three
        tempBoard = makeBoardCopy(tempBoard)
        tempPath = makeListCopy(route)
        tempR = tempR - 1
        tempBoard[tempR][c0] = tempBoard[tempR - 1][c0]
        tempBoard[tempR-1][c0] = 0
        tempStr = "D3"+str(r0+1)
        tempPath.append(tempStr)
        succesorList.append([heuristicFunction(tempBoard), [tempBoard, tempPath]])

    elif r0 == 2:
        tempR = r0
        # Handle moving just 1
        
        tempBoard = makeBoardCopy(board)
        tempPath = makeListCopy(route)
        tempBoard[tempR][c0] = tempBoard[tempR - 1][c0]
        tempBoard[tempR-1][c0] = 0
        tempStr = "D1"+str(c0+1)
        tempPath.append(tempStr)
        tB = tempBoard[:]
        succesorList.append([heuristicFunction(tempBoard), [tB, tempPath]])
        # Handle moving just 2

        tempBoard = makeBoardCopy(tempBoard)
        tempPath = makeListCopy(route)
        tempR = tempR - 1
        tempBoard[tempR][c0] = tempBoard[tempR - 1][c0]
        tempBoard[tempR-1][c0] = 0
        tempStr = "D2"+str(c0+1)
        tempPath.append(tempStr)
        succesorList.append([heuristicFunction(tempBoard), [tempBoard, tempPath]])


        # Handle moving one down
        tempR = r0
        tempBoard = makeBoardCopy(board)
        tempPath = makeListCopy(route)
        tempBoard[tempR][c0] = tempBoard[tempR +1][c0]
        tempBoard[tempR+1][c0] = 0
        tempStr = "U1"+str(c0+1)
        tempPath.append(tempStr)
        succesorList.append([heuristicFunction(tempBoard), [tempBoard, tempPath]])
    elif r0 == 1:
        tempR = r0
        # Handle moving just 1
        
        tempBoard = makeBoardCopy(board)
        tempPath = makeListCopy(route)
        tempBoard[tempR][c0] = tempBoard[tempR - 1][c0]
        tempBoard[tempR-1][c0] = 0
        tempStr = "D1"+str(c0+1)
        tempPath.append(tempStr)
        tB = tempBoard[:]
        succesorList.append([heuristicFunction(tempBoard), [tB, tempPath]])
        # Handle moving one down

        tempBoard = makeBoardCopy(board)
        tempPath = makeListCopy(route)
        tempBoard[tempR][c0] = tempBoard[tempR + 1][c0]
        tempBoard[tempR + 1][c0] = 0
        tempStr = "U1"+str(c0+1)
        tempPath.append(tempStr)
        succesorList.append([heuristicFunction(tempBoard), [tempBoard, tempPath]])


        # Handle moving 2 down
        tempR = r0
        tempBoard = makeBoardCopy(tempBoard)
        tempPath = makeListCopy(route)
        tempR = tempR + 1
        tempBoard[tempR][c0] = tempBoard[tempR +1][c0]
        tempBoard[tempR+1][c0] = 0
        tempStr = "U2"+str(c0+1)
        tempPath.append(tempStr)
        succesorList.append([heuristicFunction(tempBoard), [tempBoard, tempPath]])
    elif r0 == 0:
        tempR = r0
        # Handle moving just 1
        
        tempBoard = makeBoardCopy(board)
        tempPath = makeListCopy(route)
        tempBoard[tempR][c0] = tempBoard[tempR + 1][c0]
        tempBoard[tempR + 1][c0] = 0
        tempStr = "U1"+str(c0+1)
        tempPath.append(tempStr)
        succesorList.append([heuristicFunction(tempBoard), [tempBoard, tempPath]])
        # Handle moving just 2

        tempBoard = makeBoardCopy(tempBoard)
        tempPath = makeListCopy(route)
        tempR = tempR + 1
        tempBoard[tempR][c0] = tempBoard[tempR + 1][c0]
        tempBoard[tempR + 1][c0] = 0
        tempStr = "U2"+str(c0+1)
        tempPath.append(tempStr)
        succesorList.append([heuristicFunction(tempBoard), [tempBoard, tempPath]])


        # Handle moving all three
        tempBoard = makeBoardCopy(tempBoard)
        tempPath = makeListCopy(route)
        tempR = tempR + 1
        tempBoard[tempR][c0] = tempBoard[tempR +1][c0]
        tempBoard[tempR+1][c0] = 0
        tempStr = "U3"+str(c0+1)
        tempPath.append(tempStr)
        succesorList.append([heuristicFunction(tempBoard), [tempBoard, tempPath]])
    else:
        print("ERROR")
        exit()

    # Move the column
    if c0 == 3:
        tempC = c0
        # Handle moving just 1
        
        tempBoard = makeBoardCopy(board)
        tempPath = makeListCopy(route)
        tempBoard[r0][tempC] = tempBoard[r0][tempC-1]
        tempBoard[r0][tempC-1] = 0
        tempStr = "R1"+str(c0+1)
        tempPath.append(tempStr)
        tB = tempBoard[:]
        succesorList.append([heuristicFunction(tempBoard), [tB, tempPath]])
        # Handle moving just 2

        tempBoard = makeBoardCopy(tempBoard)
        tempPath = makeListCopy(route)
        tempC = tempC - 1
        tempBoard[r0][tempC] = tempBoard[r0][tempC - 1]
        tempBoard[r0][tempC - 1] = 0
        tempStr = "R2"+str(r0+1)
        tempPath.append(tempStr)
        succesorList.append([heuristicFunction(tempBoard), [tempBoard, tempPath]])


        # Handle moving all three
        tempBoard = makeBoardCopy(tempBoard)
        tempPath = makeListCopy(route)
        tempC = tempC - 1
        tempBoard[r0][tempC] = tempBoard[r0][tempC - 1]
        tempBoard[r0][tempC - 1] = 0
        tempStr = "R3"+str(r0+1)
        tempPath.append(tempStr)
        succesorList.append([heuristicFunction(tempBoard), [tempBoard, tempPath]])

    elif c0 == 2:
        tempC = c0
        # Handle moving just 1
        
        tempBoard = makeBoardCopy(board)
        tempPath = makeListCopy(route)
        tempBoard[r0][tempC] = tempBoard[r0][tempC-1]
        tempBoard[r0][tempC-1] = 0
        tempStr = "R1"+str(r0+1)
        tempPath.append(tempStr)
        tB = tempBoard[:]
        succesorList.append([heuristicFunction(tempBoard), [tB, tempPath]])
        # Handle moving just 2

        tempBoard = makeBoardCopy(tempBoard)
        tempPath = makeListCopy(route)
        tempC = tempC - 1
        tempBoard[r0][tempC] = tempBoard[r0][tempC - 1]
        tempBoard[r0][tempC - 1] = 0
        tempStr = "R2"+str(r0+1)
        tempPath.append(tempStr)
        succesorList.append([heuristicFunction(tempBoard), [tempBoard, tempPath]])


        # Handle moving to the right
        tempBoard = makeBoardCopy(board)
        tempPath = makeListCopy(route)
        tempC = c0
        tempBoard[r0][tempC] = tempBoard[r0][tempC + 1]
        tempBoard[r0][tempC + 1] = 0
        tempStr = "L1"+str(r0+1)
        tempPath.append(tempStr)
        succesorList.append([heuristicFunction(tempBoard), [tempBoard, tempPath]])
    elif c0 == 1:
        tempC = c0
        # Handle moving just 1
        
        tempBoard = makeBoardCopy(board)
        tempPath = makeListCopy(route)
        tempBoard[r0][tempC] = tempBoard[r0][tempC-1]
        tempBoard[r0][tempC-1] = 0
        tempStr = "R1"+str(r0+1)
        tempPath.append(tempStr)
        tB = tempBoard[:]
        succesorList.append([heuristicFunction(tempBoard), [tB, tempPath]])


        # Handle moving to the right
        tempBoard = makeBoardCopy(board)
        tempPath = makeListCopy(route)
        tempC = c0
        tempBoard[r0][tempC] = tempBoard[r0][tempC + 1]
        tempBoard[r0][tempC + 1] = 0
        tempStr = "L1"+str(r0+1)
        tempPath.append(tempStr)
        succesorList.append([heuristicFunction(tempBoard), [tempBoard, tempPath]])

        # Handle moving just 2

        tempBoard = makeBoardCopy(tempBoard)
        tempPath = makeListCopy(route)
        tempC = tempC + 1
        tempBoard[r0][tempC] = tempBoard[r0][tempC + 1]
        tempBoard[r0][tempC + 1] = 0
        tempStr = "L2"+str(r0+1)
        tempPath.append(tempStr)
        succesorList.append([heuristicFunction(tempBoard), [tempBoard, tempPath]])
    elif c0 == 0:
        tempC = c0

        # Handle moving to the right
        tempBoard = makeBoardCopy(board)
        tempPath = makeListCopy(route)
        tempC = c0
        tempBoard[r0][tempC] = tempBoard[r0][tempC + 1]
        tempBoard[r0][tempC + 1] = 0
        tempStr = "L1"+str(r0+1)
        tempPath.append(tempStr)
        succesorList.append([heuristicFunction(tempBoard), [tempBoard, tempPath]])

        # Handle moving just 2

        tempBoard = makeBoardCopy(tempBoard)
        tempPath = makeListCopy(route)
        tempC = tempC + 1
        tempBoard[r0][tempC] = tempBoard[r0][tempC + 1]
        tempBoard[r0][tempC + 1] = 0
        tempStr = "L2"+str(r0+1)
        tempPath.append(tempStr)
        succesorList.append([heuristicFunction(tempBoard), [tempBoard, tempPath]])

        tempC = tempC + 1
        tempBoard = makeBoardCopy(tempBoard)
        tempPath = makeListCopy(route)
        tempBoard[r0][tempC] = tempBoard[r0][tempC+1]
        tempBoard[r0][tempC+1] = 0
        tempStr = "L3"+str(r0+1)
        tempPath.append(tempStr)
        tB = tempBoard[:]
        succesorList.append([heuristicFunction(tempBoard), [tB, tempPath]])
    else: 
        print("ERROR")
        exit()

    # print(succesorList)
    # print("----")
    return succesorList # TODO

def isGoalState(board):
    """Determines if board is:
     1  2  3  4 
     5  6  7  8
     9  10 11 12
     13 14 15 0
     Should shortcut
    """
    currentNumber = 1
    for r in board:
        for c in r:
            # print(c, currentNumber)
            if c == 0 and currentNumber == 16:
                continue
            if not c == currentNumber:
                return False
            currentNumber += 1
    return True



def aStar(path):
    "A* search of the given board. Should provide path to solution"
    if isGoalState(path[0]):
        return path
    counter = 0
    pq = Queue.PriorityQueue()
    pq.put((0, path))
    counter += 1
    visited = set()
    # print("Starting board")
    # print(path[0])
    # print("")
    while not pq.empty():
        # Gets item out of queue
        item = pq.get()

        # Assign variables 
        currentCost = item[0]
        boardRoute = item[1]
        board = boardRoute[0]

        # Handling visiting
        st = "".join(boardRoute[1])
        visited.add(st)
        
        # Checks if new board is goal state
        if isGoalState(board):
            return boardRoute
        # For each successor. In return, is a list of (expenseItself, (successorBoard, successorRoute)
        for s in successors(boardRoute):
            successorBoardRoute = s[1]
            # succesorBoard = successorBoardRoute[0]
            succesorCost = s[0]/float(3)
            if not "".join(successorBoardRoute[1]) in visited:
                # if len(successorBoardRoute[1]) > 1 and successorBoardRoute[1][0] == 'L13' and successorBoardRoute[1][1] == 'U12':
                #     print(successorBoardRoute[1])
                # Adds the cost to the value returned
                pq.put((succesorCost + len(successorBoardRoute[1]) + 1, successorBoardRoute))
                counter += 1 # Something for the priority queue
    return list()

def printPath(path):
    s = ""
    for p in path:
        s = s + str(p) + " "
    print(s)

def main():
    if not len(sys.argv) == 2:
        print("Not enough arguments")
        return
    fileName = sys.argv[1]
    board = parseFile(fileName)
    path = [board, []]
    result = aStar(path)
    printPath(result[1])


if __name__ == "__main__":
    main()



"""
Abstraction:
    - Set of states S
        * Any state that has all 16 pieces on the board
        * In any arrangement (only legal moves)
    - Initial State
        * Given board is the intitial state
    - Successor Function
        * Moving a piece(s) up, left, right, or down 
        * Also more than 1 piece can move at a time
    - Set of goal states
    - Cost function
    - Heuristic Function
"""