from typing import Tuple

SCORE_PIECE = {
  'K': 900,
  'Q': 90,
  'R': 50,
  'B': 30,
  'N': 30,
  'P': 5
}


class Move:

  def __init__(self, i, j, ni, nj, is_capture_move=False, score=0) -> None:
    self.i, self.j, self.ni, self.nj, self.is_capture_move, self.score = \
      i, j, ni, nj, is_capture_move, score

  def __repr__(self) -> str:
    return f"({self.i}, {self.j}) -> ({self.ni}, {self.nj}) is_capture_move={self.is_capture_move} score={self.score}"

  def __eq__(self, other: 'Move') -> bool:
    if not isinstance(other, Move):
      return NotImplemented
    return (self.i, self.j, self.ni, self.nj, self.is_capture_move, self.score) == \
      (other.i, other.j, other.ni, other.nj, other.is_capture_move, other.score)

  # TODO: Write chess notation logs.


class MoveBlockVector:

  def __init__(self, i, j, d: Tuple[int, int]):
    self.i, self.j, self.d = i, j, d
