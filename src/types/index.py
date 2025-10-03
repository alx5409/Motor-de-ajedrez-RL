class PieceType:
    PAWN = 'pawn'
    KNIGHT = 'knight'
    BISHOP = 'bishop'
    ROOK = 'rook'
    QUEEN = 'queen'
    KING = 'king'

class GameState:
    IN_PROGRESS = 'in_progress'
    WHITE_WON = 'white_won'
    BLACK_WON = 'black_won'
    DRAW = 'draw'