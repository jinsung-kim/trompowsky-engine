from board import Board
from typing import List, Callable, Tuple
from move import Move, SCORE_PIECE


class Engine:

  def __init__(self, board: Board) -> None:
    self.ai_move = False
    self.board = board

  @staticmethod
  def in_bounds(i: int, j: int) -> bool:
    return 0 <= i < 8 and 0 <= j < 8

  def generate_moves_in_direction(self, i: int, j: int, direction: Callable[[int, int], Tuple[int, int]]) -> List[Move]:
    moves: List[Move] = []
    ni, nj = direction(i, j)
    while self.in_bounds(ni, nj):
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
      lambda x, y: (x, y + 1)  # Down
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
      lambda x, y: (x + 1, y + 1)  # Bottom right
    ]

    moves: List[Move] = []
    for direction in directions:
      moves.extend(self.generate_moves_in_direction(i, j, direction))
    return moves

  def generate_queen_moves(self, i, j) -> List[Move]:
    return self.generate_rook_moves(i, j) + self.generate_bishop_moves(i, j)

  def generate_pawn_moves(self, i, j) -> List[Move]:
    moves: List[Move] = []

    color = self.board.board[j][i][0]

    if color == 'w':
      direction = -1
      start_row = 6
      promotion_row = 0
      oppo = 'b'
    else:
      direction = 1
      start_row = 1
      promotion_row = 7
      oppo = 'w'

    # Pawns can move up/down two squares if they are on the starting row.
    nj = j + direction

    if 0 <= nj < 8 and self.board.board[nj][i] == '--':
      moves.append(Move(i, j, i, nj))

      nj += direction
      if j == start_row and self.board.board[nj][i] == '--':
        moves.append(Move(i, j, i, nj))

    # Check for valid diagonal attacks.
    for di in [-1, 1]:
      ni = i + di
      nj = j + direction

      if self.in_bounds(ni, nj) and oppo == self.board.board[nj][ni][0]:
        score: int = SCORE_PIECE[self.board.board[nj][ni][1]]
        moves.append(Move(i, j, ni, nj, True, score))

    # Check for promotion to re-evaluate scores. Automatically promote to queen.
    for move in moves:
      if move.nj == promotion_row:
        # TODO: Make this support the others.
        promotion_score = SCORE_PIECE['Q'] - SCORE_PIECE['P']
        move.score += promotion_score

    return moves

  def generate_knight_moves(self, i, j) -> List[Move]:
    pass

  def generate_king_moves(self, i, j) -> List[Move]:
    pass
