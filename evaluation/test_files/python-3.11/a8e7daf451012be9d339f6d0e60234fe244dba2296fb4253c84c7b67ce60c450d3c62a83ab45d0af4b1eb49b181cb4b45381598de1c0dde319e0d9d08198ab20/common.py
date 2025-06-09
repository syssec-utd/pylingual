RED, BLACK = (1, 0)
BORDER, SPACE = (15, 56)
LOCAL, OTHER = (0, 1)
NETWORK, AI = (0, 1)
KING, ADVISOR, BISHOP, KNIGHT, ROOK, CANNON, PAWN, NONE = (0, 1, 2, 3, 4, 5, 6, -1)
AI_SEARCH_DEPTH = 5
init_fen = 'rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR r - - 0 1'
replace_dict = {'r': 'r', 'R': 'R', 'n': 'n', 'N': 'N', 'b': 'b', 'B': 'B', 'a': 'a', 'A': 'A', 's': 'k', 'S': 'K', 'p': 'p', 'P': 'P', 'c': 'c', 'C': 'C'}
state_to_board_dict = replace_dict
mov_dir = {'k': [(0, -1), (1, 0), (0, 1), (-1, 0)], 'K': [(0, -1), (1, 0), (0, 1), (-1, 0)], 'a': [(-1, -1), (1, -1), (-1, 1), (1, 1)], 'A': [(-1, -1), (1, -1), (-1, 1), (1, 1)], 'b': [(-2, -2), (2, -2), (2, 2), (-2, 2)], 'B': [(-2, -2), (2, -2), (2, 2), (-2, 2)], 'n': [(-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1)], 'N': [(-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1)], 'P': [(0, -1), (-1, 0), (1, 0)], 'p': [(0, 1), (-1, 0), (1, 0)]}
bishop_check = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
knight_check = [(0, -1), (0, -1), (1, 0), (1, 0), (0, 1), (0, 1), (-1, 0), (-1, 0)]

def get_kind(fen_ch):
    if fen_ch in ['k', 'K']:
        return KING
    elif fen_ch in ['a', 'A']:
        return ADVISOR
    elif fen_ch in ['b', 'B']:
        return BISHOP
    elif fen_ch in ['n', 'N']:
        return KNIGHT
    elif fen_ch in ['r', 'R']:
        return ROOK
    elif fen_ch in ['c', 'C']:
        return CANNON
    elif fen_ch in ['p', 'P']:
        return PAWN
    else:
        return NONE

def get_char(kind, color):
    if kind is KING:
        return ['K', 'k'][color]
    elif kind is ADVISOR:
        return ['A', 'a'][color]
    elif kind is BISHOP:
        return ['B', 'b'][color]
    elif kind is KNIGHT:
        return ['N', 'n'][color]
    elif kind is ROOK:
        return ['R', 'r'][color]
    elif kind is CANNON:
        return ['C', 'c'][color]
    elif kind is PAWN:
        return ['P', 'p'][color]
    else:
        return ''

def move_to_str(x, y, x_, y_):
    move_str = ''
    move_str += str(x)
    move_str += str(y)
    move_str += str(x_)
    move_str += str(y_)
    return move_str

def str_to_move(move_str):
    move_arr = [0] * 4
    move_arr[0] = int(move_str[0])
    move_arr[1] = int(move_str[1])
    move_arr[2] = int(move_str[2])
    move_arr[3] = int(move_str[3])
    return move_arr

class Move:

    def __init__(self, uci: str):
        s = str_to_move(uci)
        self.p = (s[0], s[1])
        self.n = (s[2], s[3])
        self.uci = uci

    @staticmethod
    def from_uci(uci):
        return Move(uci)