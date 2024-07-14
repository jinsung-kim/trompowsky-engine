from engine import Engine
from move import Move
from typing import List, Optional
from random import shuffle


class Ai:

  def __init__(self, depth=3):
    # The depth determines the difficulty of the AI.
    # Note that moves will take longer to generate the higher this is set.
    self.depth = depth
    self.next_move: Optional[Move] = None

  def find_optimal_move(self, valid_moves: List[Move], engine: Engine) -> Optional[Move]:
    self.next_move = None
    shuffle(valid_moves)
    self.find_alpha_beta_prune_move(valid_moves, engine, self.depth, -10000, 10000, -1)
    return self.next_move

  def find_alpha_beta_prune_move(self, valid_moves: List[Move], engine: Engine, depth: int,
                                 alpha: int, beta: int, turn_multiplier: int) -> int:
    if depth == 0:
      return turn_multiplier * engine.board.score_board()

    max_score = -10000

    for move in valid_moves:
      engine.board.make_move(move)
      valid_opposing_moves = engine.generate_valid_moves('w' if turn_multiplier == -1 else 'b')
      score = -self.find_alpha_beta_prune_move(valid_opposing_moves, engine, depth - 1, -beta, -alpha, -turn_multiplier)

      if score > max_score:
        max_score = score
        # Best move for the provided board.
        if depth == self.depth:
          self.next_move = move

      engine.board.undo_move(move)
      if max_score > alpha:
        alpha = max_score
      if alpha >= beta:
        break

    return max_score
