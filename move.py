

class Move:

  def __init__(self, i, j, ni, nj, is_capture_move = False) -> None:
    self.i, self.j, self.ni, self.nj, self.is_capture_move = \
      i, j, ni, nj, is_capture_move

  def __repr__(self) -> str:
    return f"({self.i}, {self.j}) -> ({self.ni}, {self.nj}) is_capture_move={self.is_capture_move}"

  def __eq__(self, other: 'Move') -> bool:
    if not isinstance(other, Move):
      return NotImplemented
    return (self.i, self.j, self.ni, self.nj, self.is_capture_move) == \
      (other.i, other.j, other.ni, other.nj, other.is_capture_move)
