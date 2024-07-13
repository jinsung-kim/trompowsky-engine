from move import Move, SCORE_PIECE
from copy import deepcopy

EMPTY_BOARD = [
  ['--', '--', '--', '--', '--', '--', '--', '--'],
  ['--', '--', '--', '--', '--', '--', '--', '--'],
  ['--', '--', '--', '--', '--', '--', '--', '--'],
  ['--', '--', '--', '--', '--', '--', '--', '--'],
  ['--', '--', '--', '--', '--', '--', '--', '--'],
  ['--', '--', '--', '--', '--', '--', '--', '--'],
  ['--', '--', '--', '--', '--', '--', '--', '--'],
  ['--', '--', '--', '--', '--', '--', '--', '--']
]

START_BOARD = [
  ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
  ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
  ["--", "--", "--", "--", "--", "--", "--", "--"],
  ["--", "--", "--", "--", "--", "--", "--", "--"],
  ["--", "--", "--", "--", "--", "--", "--", "--"],
  ["--", "--", "--", "--", "--", "--", "--", "--"],
  ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
  ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
]


# Maintains game state.
class Board:

  def __init__(self, is_test_board: bool = False):
    if is_test_board:
      self.board = deepcopy(EMPTY_BOARD)
    else:
      self.board = deepcopy(START_BOARD)

    # TODO: Track all of the game moves.
    self.game_log = []

  def __repr__(self) -> str:
    return '\n' + '\n'.join([' '.join(row) for row in self.board]) + '\n'

  def clear_board(self):
    self.board = deepcopy(EMPTY_BOARD)

  def make_move(self, move: Move):
    """
    Moves a piece from (i, j) to (ni, nj).
    Handles promotions, piece capturing, etc.

    args:
      move (Move): The current position of the piece and the desired place of the piece.
    """
    piece = self.board[move.j][move.i]
    self.board[move.nj][move.ni] = piece
    self.board[move.j][move.i] = '--'

    p_color, p_type = piece[0], piece[1]

    if p_type == 'K':
      if p_color == 'b':
        engine.bk_pos = (move.ni, move.nj)
      else:
        engine.wk_pos = (move.ni, move.nj)

    # Consider promotion.
    if p_type == 'P':
      if p_color == 'w':
        promotion_row = 0
      else:
        promotion_row = 7

      if move.nj == promotion_row:
        self.board[move.nj][move.ni] = p_color + 'Q'

  def undo_move(self, move: Move):
    """
    Undo a move from (ni, nj) to (i, j).
    Undoes promotions, king movement, captured pieces.
    """
    pass

  def score_board(self) -> int:
    """
    Score the current board, user pieces are scored positively, AI pieces are scored negatively.
    """
    score = 0
    for i in range(8):
      for j in range(8):
        piece = self.board[j][i]
        if piece != '--':
          score += SCORE_PIECE[piece[1]] if piece[0] == 'w' else -SCORE_PIECE[piece[1]]
    return score

  # TODO: Write this.
  def log_move(self, move: Move):
    pass
