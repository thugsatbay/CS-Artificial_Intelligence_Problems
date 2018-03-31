from heuristic import heuristicAI as HAI

class pichuAI():
    def __init__(self,
                 board,
                 player,
                 depth=2,
                 FAST_MODE=False):

        self.heuristicFunction = HAI(board, player)
        self.allowed_depth = depth
        self.board = board
        self.player = player
        self.node_count = 0
        self.FAST_MODE =FAST_MODE


    def findTheBestMove(self):
        board_moves = self.board.findAllValidMoves()[0]
        alpha, beta = float('-inf'), float('inf')
        best_move = board_moves[0]
        self.board.makeAMove(best_move).printBoard()
        for each_move in board_moves:
            board_cost = self.minmax(self.board.makeAMove(each_move),
                                     alpha,
                                     beta,
                                     1)
            #print "Move", self.board.convertCMToI2CC(each_move), "Board", board_cost
            if alpha < board_cost:
                best_move = each_move
                if not self.FAST_MODE:
                    print "Move", self.board.convertCMToI2CC(each_move), "Board", board_cost
                #else:
                    #print "Move", each_move, "Board", board_cost
                self.board.makeAMove(each_move).printBoard()
            alpha = max(alpha, board_cost)
        if not self.FAST_MODE:
            print "Total Nodes Explored", self.node_count

    def minmax(self, move_board, alpha, beta, current_depth=0):
        # Increase the current depth of the search tree
        current_depth += 1

        '''
        Returns False if both kings are alive
        Else returns player whose king is alive
        '''
        king_status = move_board.isKingDead()
        if king_status:
            if self.player == king_status:
                return float('inf')
            else:
                return float('-inf')


        if current_depth == self.allowed_depth:
            board_h_cost = self.pichu_heuristics(move_board)
            if not current_depth % 2:
                '''
                Return max since the above layer is max
                '''
                alpha = max(alpha, board_h_cost)
                self.node_count += 1
                return alpha
            else:
                '''
                Return min since the above even layer is min
                '''
                beta = min(beta, board_h_cost)
                self.node_count += 1
                return beta
        # min - even layer
        elif not current_depth % 2:
            min_moves = move_board.findAllValidMoves()[0]
            for each_move in min_moves:
                if alpha < beta:
                    board_min_cost = self.minmax(move_board.makeAMove(each_move),
                                                    alpha,
                                                    beta,
                                                    current_depth)
                    beta = min(beta, board_min_cost)
            return beta
        # max - odd layer
        else:
            max_moves = move_board.findAllValidMoves()[0]
            for each_move in max_moves:
                if alpha < beta:
                    board_max_cost = self.minmax(move_board.makeAMove(each_move),
                                                    alpha,
                                                    beta,
                                                    current_depth)
                    alpha = max(alpha, board_max_cost)
            return alpha

    def pichu_heuristics(self, move_board):
        total_h_cost = 0

        # Update the board to the heuristic functionalty
        self.heuristicFunction.changeBoard(move_board)

        # Calculate all the heuristics, sum to 100
        total_h_cost += self.heuristicFunction.material(40)
        # king check
        total_h_cost += self.heuristicFunction.check(15)
        # place pieces in center
        total_h_cost += self.heuristicFunction.piece_placement(1)
        # possible moves by another player at end of search
        total_h_cost += self.heuristicFunction.depth_possible_moves_score(10)
        # pawn shapes
        total_h_cost += self.heuristicFunction.pawn_structure(25)
        return total_h_cost
