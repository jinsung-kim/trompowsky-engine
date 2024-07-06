import math
from typing import List
from move import Move


def truncate(f, n):
  return math.floor(f * 10 ** n / 10 ** n)


def sort_moves(moves: List[Move]) -> List[Move]:
  return sorted(moves, key=lambda m: (m.ni, m.nj))
