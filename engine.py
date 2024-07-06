from copy import deepcopy

from board import Board
from typing import List, Callable, Tuple

from helpers import get_opposite_color
from move import Move, SCORE_PIECE


class Engine:

  def __init__(self) -> None:
    self.ai_move = False

  @staticmethod
  def in_bounds(i: int, j: int) -> bool:
    return 0 <= i < 8 and 0 <= j < 8

  def generate_moves_in_direction(self, i: int, j: int,
                                  direction: Callable[[int, int], Tuple[int, int]], board: Board) -> List[Move]:
    moves: List[Move] = []
    ni, nj = direction(i, j)
    while self.in_bounds(ni, nj):
      move_maybe = board.return_valid_move(i, j, ni, nj)
      if move_maybe is not None:
        moves.append(move_maybe)
        if move_maybe.is_capture_move:
          break
      else:
        break
      ni, nj = direction(ni, nj)
    return moves

  def generate_moves_for_direction(self, i, j, d, board: Board) -> List[Move]:
    moves: List[Move] = []

    for (di, dj) in d:
      ni = i + di
      nj = j + dj
      if self.in_bounds(ni, nj):
        move_maybe = board.return_valid_move(i, j, ni, nj)
        if move_maybe is not None:
          moves.append(move_maybe)

    return moves

  def generate_rook_moves(self, i, j, board: Board) -> List[Move]:
    directions = [
      lambda x, y: (x - 1, y),  # Left
      lambda x, y: (x + 1, y),  # Right
      lambda x, y: (x, y - 1),  # Up
      lambda x, y: (x, y + 1)  # Down
    ]

    moves: List[Move] = []
    for direction in directions:
      moves.extend(self.generate_moves_in_direction(i, j, direction, board))

    return moves

  def generate_bishop_moves(self, i, j, board: Board) -> List[Move]:
    directions = [
      lambda x, y: (x - 1, y - 1),  # Top left
      lambda x, y: (x + 1, y - 1),  # Top right
      lambda x, y: (x - 1, y + 1),  # Bottom left
      lambda x, y: (x + 1, y + 1)  # Bottom right
    ]

    moves: List[Move] = []
    for direction in directions:
      moves.extend(self.generate_moves_in_direction(i, j, direction, board))
    return moves

  def generate_queen_moves(self, i, j, board: Board) -> List[Move]:
    return self.generate_rook_moves(i, j, board) + self.generate_bishop_moves(i, j, board)

  def generate_pawn_moves(self, i, j, board: Board) -> List[Move]:
    moves: List[Move] = []

    color = board.board[j][i][0]
    oppo = get_opposite_color(color)

    if color == 'w':
      direction = -1
      start_row = 6
      promotion_row = 0
    else:
      direction = 1
      start_row = 1
      promotion_row = 7

    # Pawns can move up/down two squares if they are on the starting row.
    nj = j + direction

    if 0 <= nj < 8 and board.board[nj][i] == '--':
      moves.append(Move(i, j, i, nj))

      nj += direction
      if j == start_row and board.board[nj][i] == '--':
        moves.append(Move(i, j, i, nj))

    # Check for valid diagonal attacks.
    for di in [-1, 1]:
      ni = i + di
      nj = j + direction

      if self.in_bounds(ni, nj) and oppo == board.board[nj][ni][0]:
        score: int = SCORE_PIECE[board.board[nj][ni][1]]
        moves.append(Move(i, j, ni, nj, True, score))

    # Check for promotion to re-evaluate scores. Automatically promote to queen.
    for move in moves:
      if move.nj == promotion_row:
        # TODO: Make this support the others.
        promotion_score = move.score + SCORE_PIECE['Q'] - SCORE_PIECE['P']
        move.score += promotion_score

    return moves

  def generate_knight_moves(self, i, j, board: Board) -> List[Move]:
    d = [(-2, 1), (-2, -1),
         (-1, -2), (1, -2),
         (2, -1), (2, 1),
         (1, 2), (-1, 2)]

    moves: List[Move] = self.generate_moves_for_direction(i, j, d, board)
    return moves

  def generate_king_moves(self, i, j, board: Board) -> List[Move]:
    d = [(-1, 1), (1, -1), (1, 0), (0, 1),
         (-1, 0), (0, -1), (1, 1), (-1, -1)]
    color = board.board[j][i][0]
    oppo = get_opposite_color(color)

    moves: List[Move] = self.generate_moves_for_direction(i, j, d, board)

    # TODO: There's an infinite recursion loop here. Fix it.
    return [move for move in moves if not self.is_position_attacked(move, oppo, board)]

  def generate_ai_moves(self):
    pass

  def generate_potential_moves(self, i, j, board: Board) -> List[Move]:
    piece = board.board[j][i][1]
    if piece == 'P':
      return self.generate_pawn_moves(i, j, board)
    elif piece == 'R':
      return self.generate_rook_moves(i, j, board)
    elif piece == 'N':
      return self.generate_knight_moves(i, j, board)
    elif piece == 'B':
      return self.generate_bishop_moves(i, j, board)
    elif piece == 'Q':
      return self.generate_queen_moves(i, j, board)
    elif piece == 'K':
      return self.generate_king_moves(i, j, board)
    return []

  def is_position_attacked(self, move: Move, oppo: str, board: Board) -> bool:
    # TODO: Make sure each move does not jeopardize the king.
    # TODO: Optimize this so that we aren't generating the whole list of moves before checking.

    # The p_board is the potential board if the move passed in was executed.
    # TODO: A helper function for this swap below.
    p_board: Board = deepcopy(board)
    curr = board.board[move.j][move.i]
    p_board.board[move.j][move.i] = '--'
    p_board.board[move.nj][move.ni] = curr

    opposing_moves: List[Move] = []
    for ci in range(8):
      for cj in range(8):
        if p_board.board[cj][ci][0] == oppo:
          opposing_moves.extend(self.generate_potential_moves(ci, cj, p_board))

    for p_move in opposing_moves:
      if p_move.ni == move.ni and p_move.nj == move.nj:
        return True

    return False
