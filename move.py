from typing import Tuple

SCORE_PIECE = {
  'K': 900,
  'Q': 90,
  'R': 50,
  'B': 30,
  'N': 30,
  'P': 5,
}


class Move:

  def __init__(self, i, j, ni, nj, capture_piece=None) -> None:
    self.i, self.j, self.ni, self.nj, self.capture_piece = \
      i, j, ni, nj, capture_piece

  def __repr__(self) -> str:
    return f"({self.i}, {self.j}) -> ({self.ni}, {self.nj}) capture_piece={self.capture_piece}"

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
