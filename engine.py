from board import Board
from typing import List, Callable, Tuple
from move import Move


class Engine:

  def __init__(self, board: Board) -> None:
    self.ai_move = False
    self.board = board

  def generate_user_moves(self, i, j, board: Board) -> List[Move]:
    """
    For any given piece, will return a list of moves that the user can make.
    TODO: Must always check that the king is not in danger through any move.

    Args:
      i (int): The row index of the piece to move.
      j (int): The column index of the piece to move.
      board (Board): The current state of the board.

    Returns:
      List[Move]: A list of possible moves for the piece located at (i, j).
    """
    pass

  def generate_moves_in_direction(self, i: int, j: int, direction: Callable[[int, int], Tuple[int, int]]) -> List[Move]:
    moves: List[Move] = []
    ni, nj = direction(i, j)
    while 0 <= ni < 8 and 0 <= nj < 8:
      move_maybe = self.board.return_valid_move(i, j, ni, nj)
      if move_maybe is not None:
        moves.append(move_maybe)
        if move_maybe.is_capture_move:
          break
      else:
        break
      ni, nj = direction(ni, nj)
    return moves

  def generate_rook_moves(self, i, j) -> List[Move]:
    directions = [
      lambda x, y: (x - 1, y),  # Left
      lambda x, y: (x + 1, y),  # Right
      lambda x, y: (x, y - 1),  # Up
      lambda x, y: (x, y + 1)   # Down
    ]

    moves: List[Move] = []
    for direction in directions:
      moves.extend(self.generate_moves_in_direction(i, j, direction))

    return moves

  def generate_bishop_moves(self, i, j) -> List[Move]:
    directions = [
      lambda x, y: (x - 1, y - 1),  # Top left
      lambda x, y: (x + 1, y - 1),  # Top right
      lambda x, y: (x - 1, y + 1),  # Bottom left
      lambda x, y: (x + 1, y + 1)   # Bottom right
    ]

    moves: List[Move] = []
    for direction in directions:
      moves.extend(self.generate_moves_in_direction(i, j, direction))
    return moves

  def generate_queen_moves(self, i, j) -> List[Move]:
    return self.generate_rook_moves(i, j) + self.generate_bishop_moves(i, j)

  def generate_pawn_moves(self, i, j) -> List[Move]:
    pass

  def generate_knight_moves(self, i, j) -> List[Move]:
    pass

  def generate_king_moves(self, i, j) -> List[Move]:
    pass
