from board import Board
from move import Move
from typing import List


class Ai:

  def __init__(self):
    pass

  @staticmethod
  def find_optimal_move(valid_moves: List[Move], board: Board) -> Move:
    pass

  @staticmethod
  def find_alpha_beta_prune_move(valid_moves: List[Move], board: Board, depth: int, alpha: int, beta: int) -> Move:
    pass

