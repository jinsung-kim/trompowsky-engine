

class Board:

  def __init__(self):
    self.board = [
      ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
      ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
      ["--", "--", "--", "--", "--", "--", "--", "--"],
      ["--", "--", "--", "--", "--", "--", "--", "--"],
      ["--", "--", "--", "--", "--", "--", "--", "--"],
      ["--", "--", "--", "--", "--", "--", "--", "--"],
      ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
      ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
    ]

    # TODO: Track all of the game moves.
    self.game_log = []

  def __repr__(self) -> str:
    return '\n'.join([' '.join(row) for row in self.board])

  def make_move(self, i, j, ni, nj) -> bool:
    '''
    Attempts to move a piece from (i, j) to (ni, nj).

    args:
      i (int): The row index of the piece to move.
      j (int): The column index of the piece to move.
      ni (int): The row index of the destination.
      nj (int): The column index of the destination.

    Returns:
      bool: True if the move is successful, False otherwise - in which case the
      board is reverted to its state.
    '''
    return False