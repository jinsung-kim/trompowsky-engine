from move import Move
from typing import Optional
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

  def make_move(self, move: Move) -> bool:
    """
    Moves a piece from (i, j) to (ni, nj). Moves will be pre-vetted so
    once this function is handed the move - it is assumed that it is valid.

    args:
      move (Move): The current position of the piece and the desired place of the piece.
    """
    pass

  def return_valid_move(self, i, j, ni, nj) -> Optional[Move]:
    color = self.board[j][i][0]
    oppo = 'b' if color == 'w' else 'w'
    if self.board[nj][ni] == '--':
      return Move(i, j, ni, nj, False)
    elif oppo == self.board[nj][ni][0]:
      return Move(i, j, ni, nj, True)
    else:
      return None
