from engine import Engine
from move import Move
from typing import List, Optional
from random import shuffle, choice


class Ai:

  def __init__(self, depth=3):
    # The depth determines the difficulty of the AI.
    # Note that moves will take longer to generate the higher this is set.
    self.depth = depth
    self.next_move: Optional[Move] = None

  def find_optimal_move(self, engine: Engine) -> Optional[Move]:
    self.next_move = None
    shuffle(engine.black_moves)
    self.find_alpha_beta_prune_move(engine.black_moves, engine, self.depth, -10000, 10000, -1)
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

  def make_optimal_move(self, engine: Engine) -> bool:
    """
    Makes the in most cases the optimal move, and then checks the game state.
    :return: Whether the game is over or not.
    """
    engine.refresh_moves_and_game_state('b')

    optimal_move_maybe = self.find_optimal_move(engine)

    if optimal_move_maybe is None:
      optimal_move_maybe = choice(engine.black_moves)

    engine.board.make_move(optimal_move_maybe)

    engine.refresh_moves_and_game_state('w')
    engine.board.log_move(optimal_move_maybe, engine.in_check, engine.checkmate)

    return engine.check_game_over()
