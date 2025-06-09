def reset(self):
    """Restores the starting position."""
    self.piece_bb = [BB_VOID, BB_RANK_C | BB_RANK_G, BB_A1 | BB_I1 | BB_A9 | BB_I9, BB_A2 | BB_A8 | BB_I2 | BB_I8, BB_A3 | BB_A7 | BB_I3 | BB_I7, BB_A4 | BB_A6 | BB_I4 | BB_I6, BB_B2 | BB_H8, BB_B8 | BB_H2, BB_A5 | BB_I5, BB_VOID, BB_VOID, BB_VOID, BB_VOID, BB_VOID, BB_VOID]
    self.pieces_in_hand = [collections.Counter(), collections.Counter()]
    self.occupied = Occupied(BB_RANK_G | BB_H2 | BB_H8 | BB_RANK_I, BB_RANK_A | BB_B2 | BB_B8 | BB_RANK_C)
    self.king_squares = [I5, A5]
    self.pieces = [NONE for i in SQUARES]
    for i in SQUARES:
        mask = BB_SQUARES[i]
        for piece_type in PIECE_TYPES:
            if mask & self.piece_bb[piece_type]:
                self.pieces[i] = piece_type
    self.turn = BLACK
    self.move_number = 1
    self.captured_piece_stack = collections.deque()
    self.move_stack = collections.deque()
    self.incremental_zobrist_hash = self.board_zobrist_hash(DEFAULT_RANDOM_ARRAY)
    self.transpositions = collections.Counter((self.zobrist_hash(),))