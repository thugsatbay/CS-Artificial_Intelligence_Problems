class heuristicAI():
    def __init__(self, board_state, main_player):
        self.board_state = board_state
        self.current_player = self.board_state.returnPlayer()
        self.possible_moves = self.board_state.findAllValidMoves()[0]
        self.main_player = main_player

    def changeBoard(self, board_state):
        self.board_state = board_state
        self.current_player = self.board_state.returnPlayer()
        self.possible_moves = self.board_state.findAllValidMoves()[0]

    def material(self, weight):
        '''
            Checks the material balance at a given board state

            Reference: https://chessprogramming.wikispaces.com/Material

            According to traditional chess, the piece values of each player is
            as follows:
            Pawn (Parakeet) = 1
            Bishop (Blue Jay) = 3
            Rook (Robin) = 3
            Knight (Nighthawk) = 5
            Queen (Quetzal) = 9
            King (Kingfisher) = 0

            Reference: https://chessprogramming.wikispaces.com/Point+Value as proposed by Claude Shannon

            We calcuate the material value of the given board with respect to the maximizing player
        '''
        points = 0
        board_status = self.board_state.makeBoard()
        player = self.main_player

        black_point_multiplier = -1
        white_point_multiplier = -1
        if player == 'b':
            black_point_multiplier = 1
        else:
            white_point_multiplier = 1

        piece_values = {'p': 1, 'r': 3, 'b': 3, 'n': 5, 'q': 9, 'k': 0}
        # If computer is black or white, gets +ve score accordingly

        for piece in piece_values:
            points += white_point_multiplier * \
                    board_status['w'][piece.upper()] * \
                    piece_values[piece]
            points += black_point_multiplier * \
                    board_status['b'][piece] * \
                    piece_values[piece]
        return points * weight


    def piece_placement(self, weight):
        '''
            This heuristic function checks for the Centrality of the board.
            Central Region: (18,19,20,21,26,27,28,29,34,35,36,37,42,43,44,45)

            0  1  2  3  4  5  6  7
            8  9 10 11 12 13 14 15
           16 17 18 19 20 21 22 23
           24 25 26 27 28 29 30 31
           32 33 34 35 36 37 38 39
           40 41 42 43 44 45 46 47
           48 49 50 51 52 53 54 55
           56 57 58 59 60 61 62 63

           If the maximizing player has more number of player in the central
           board then the player gets positive points else the maximizing player
           points are adversely affected.

           Reference: https://en.wikipedia.org/wiki/Chess_strategy "Control Of Center" section

        '''


        points = 0
        square_center_values = {
                                    27: 1,
                                    28: 1,
                                    35: 1,
                                    36: 1,
                                    18: 0.5,
                                    19: 0.5,
                                    20: 0.5,
                                    21: 0.5,
                                    42: 0.5,
                                    43: 0.5,
                                    44: 0.5,
                                    45: 0.5,
                                    26: 0.5,
                                    34: 0.5,
                                    29: 0.5,
                                    37: 0.5
                                }

        for move in self.possible_moves:
            if self.current_player == self.main_player:
                if move.to_p in square_center_values:
                    points += square_center_values[move.to_p]
            else:
                if move.to_p in square_center_values:
                    points -= square_center_values[move.to_p]

        return points


    def depth_possible_moves_score(self, weight):

        '''

        This evaluation function calculates the Mobililty of a player based
        on the number of moves the player can make froma cell

         0  1  2  3  4  5  6  7
         8  9 10 11 12 13 14 15
        16 17 18 19 20 21 22 23
        24 25 26 27 28 29 30 31
        32 33 34 35 36 37 38 39
        40 41 42 43 44 45 46 47
        48 49 50 51 52 53 54 55
        56 57 58 59 60 61 62 63

        Reference: https://en.wikibooks.org/wiki/Chess_Strategy/Mobility

        '''



        points = 0
        piece_values =  {
                            'p': 1,
                            'b': 3,
                            'n': 5,
                            'r': 3,
                            'q': 9,
                            'k': 0
                        }

        for move in self.possible_moves:
            piece_info_from = self.board_state.getPieceInfoAtIndex(move.from_p)
            if self.current_player == self.main_player and self.current_player ==  piece_info_from:
                points += piece_values[self.board_state.getPieceAtIndex(move.from_p).lower()]
            elif self.current_player != self.main_player and self.current_player ==  piece_info_from:
                points -= piece_values[self.board_state.getPieceAtIndex(move.from_p).lower()]
        return points * weight

    def pawn_structure(self, weight):
        points = 0
        board = self.board_state.returnBoard()

        orientation_multiplier = 1
        pawn = "P"
        if self.main_player == 'b':
            pawn = "p"
            orientation_multiplier = -1

        '''
        0 1  2  3  4  5  6  7
        8 9 10 11 12 13 14 15
        Diagonal Connected Pawn Structure advantage
        Determine pawn to search for based on whose turn it is
        '''
        # black_points, white_points = 0, 0
        for row in xrange(8):
            for col in xrange(8):
                position = row * 8 + col
                if board[position] == pawn:
                    left_position = position - (7 * orientation_multiplier)
                    right_position = position - (9 * orientation_multiplier)
                    if left_position < 64 and board[left_position] == pawn:
                        points += 1
                    if right_position < 64 and board[right_position] == pawn:
                        points += 1
        return points * weight


    def check(self, weight):
        '''

        This evaluation function checks for the Kigfisher safety

        Reference: https://chessprogramming.wikispaces.com/King+Safety

        '''
        points = 0

        current_status = self.board_state.status()

        # Check or Checkmate situations
        if self.current_player != self.main_player:
            if current_status == 1:
                points += 1 * weight
            elif current_status == 2:
                points += float("inf")
        elif self.current_player == self.main_player:
            if current_status == 1:
                points -= 1 * weight
            elif current_status == 2:
                points += float("-inf")
        return points
