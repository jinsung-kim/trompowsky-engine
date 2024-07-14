from typing import Tuple

SCORE_PIECE = {
  'K': 90,
  'Q': 9,
  'R': 5,
  'B': 3,
  'N': 3,
  'P': 1,
}


class Move:

  def __init__(self, i, j, ni, nj, captured_piece=None, promote=False) -> None:
    self.i, self.j, self.ni, self.nj, self.captured_piece, self.promote = \
      i, j, ni, nj, captured_piece, promote

  def __repr__(self) -> str:
    return f"({self.i}, {self.j}) -> ({self.ni}, {self.nj}) captured_piece={self.captured_piece} promote={self.promote}"

  def __eq__(self, other: 'Move') -> bool:
    if not isinstance(other, Move):
      return NotImplemented
    # TODO: Should this include more than the positional fields?
    return (self.i, self.j, self.ni, self.nj) == \
      (other.i, other.j, other.ni, other.nj)

  # TODO: Write chess notation logs.


class MoveBlockVector:

  def __init__(self, i, j, d: Tuple[int, int]):
    self.i, self.j, self.d = i, j, d
