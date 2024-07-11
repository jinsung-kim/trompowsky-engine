import math
from typing import List, Optional
from move import Move


class Movement:
  Knight = [(-2, 1), (-2, -1),
            (-1, -2), (1, -2),
            (2, -1), (2, 1),
            (1, 2), (-1, 2)]

  # Note: First four are orthogonal. Last four are diagonal. The order does matter.
  # This is critical to understand the pin/check logic function.
  King = [(1, 0), (0, 1),
          (-1, 0), (0, -1),
          (-1, -1), (-1, 1),
          (1, -1), (1, 1)]


def truncate(f, n):
  return math.floor(f * 10 ** n / 10 ** n)


def sort_moves(moves: List[Move]) -> List[Move]:
  return sorted(moves, key=lambda m: (m.ni, m.nj))


def get_opposite_color(color: str) -> str:
  return 'b' if color == 'w' else 'w'
