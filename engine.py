from board import Board
from typing import List, Callable, Tuple, Optional
from helpers import get_opposite_color, Movement
from move import Move, SCORE_PIECE, MoveBlockVector
from math import gcd


class Engine:

  def __init__(self) -> None:
    self.move_functions = {
      'P': self.generate_pawn_moves,
      'N': self.generate_knight_moves,
      'R': self.generate_rook_moves,
      'K': self.generate_king_moves,
      'Q': self.generate_queen_moves,
      'B': self.generate_bishop_moves,
    }

    # Location Format: (i, j).
    # Must be up-to-date.
    self.wk_pos = (4, 7)
    self.bk_pos = (4, 0)

    self.in_check = False
    self.pins: List[MoveBlockVector] = []
    self.checks: List[MoveBlockVector] = []

  @staticmethod
  def in_bounds(i: int, j: int) -> bool:
    return 0 <= i < 8 and 0 <= j < 8

  @staticmethod
  def return_valid_move(i, j, ni, nj, board: Board) -> Optional[Move]:
    # TODO: Should this function handle pawn promotion?
    color = board.board[j][i][0]
    oppo = 'b' if color == 'w' else 'w'
    new_pos = board.board[nj][ni]
    promotion_score = 0
    if new_pos == '--':
      return Move(i, j, ni, nj, False, promotion_score)
    elif oppo == new_pos[0]:
      return Move(i, j, ni, nj, True, promotion_score + SCORE_PIECE[new_pos[1]])
    else:
      return None

  @staticmethod
  def infer_direction(move: Move) -> Tuple[int, int]:
    di = move.ni - move.i
    dj = move.nj - move.j

    # Normalize the direction by dividing by the GCD of di and dj.
    g = gcd(abs(di), abs(dj))
    return di // g, dj // g

  def generate_valid_moves_for_piece(self, i, j, board: Board, directions, is_queen: bool) -> List[Move]:
    pin: Optional[MoveBlockVector] = None

    for pinned_vector in self.pins[::-1]:
      if i == pinned_vector.i and j == pinned_vector.j:
        pin = pinned_vector
        # Since the queen calls both rook + bishop move generation functions, only allow the bishop move generator
        # to remove pins. This avoids situations where the engine believes the queen is no longer pinned, when it's not.
        if not is_queen:
          self.pins.remove(pinned_vector)
        break

    moves: List[Move] = []
    for direction in directions:
      moves.extend(self.generate_moves_in_direction(i, j, direction, board))

    if pin is None:
      return moves

    valid_moves: List[Move] = []
    for move in moves:
      move_d = self.infer_direction(move)

      if move_d == pin.d or tuple(d * -1 for d in pin.d) == move_d:
        valid_moves.append(move)

    return valid_moves

  def generate_moves_in_direction(self, i: int, j: int,
                                  direction: Callable[[int, int], Tuple[int, int]], board: Board) -> List[Move]:
    moves: List[Move] = []
    ni, nj = direction(i, j)
    while self.in_bounds(ni, nj):
      move_maybe = self.return_valid_move(i, j, ni, nj, board)
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
        move_maybe = self.return_valid_move(i, j, ni, nj, board)
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
    is_queen = board.board[j][i][1] == 'Q'

    return self.generate_valid_moves_for_piece(i, j, board, directions, is_queen)

  def generate_bishop_moves(self, i, j, board: Board) -> List[Move]:
    directions = [
      lambda x, y: (x - 1, y - 1),  # Top left
      lambda x, y: (x + 1, y - 1),  # Top right
      lambda x, y: (x - 1, y + 1),  # Bottom left
      lambda x, y: (x + 1, y + 1)  # Bottom right
    ]

    return self.generate_valid_moves_for_piece(i, j, board, directions, False)

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
    moves: List[Move] = self.generate_moves_for_direction(i, j, Movement.Knight, board)
    return moves

  def generate_king_moves(self, i, j, board: Board) -> List[Move]:
    c = board.board[j][i][0]

    moves: List[Move] = self.generate_moves_for_direction(i, j, Movement.King, board)
    valid_moves: List[Move] = []
    for move in moves:
      if c == 'w':
        self.wk_pos = (move.ni, move.nj)
      else:
        self.bk_pos = (move.ni, move.nj)

      in_check, _, _ = self.get_checks_and_pins(board, c)

      if not in_check:
        valid_moves.append(move)

      if c == 'w':
        self.wk_pos = (move.i, move.j)
      else:
        self.bk_pos = (move.i, move.j)

    return valid_moves

  def generate_all_moves(self, board: Board, c: str) -> List[Move]:
    """
    Generates all possible moves without considering checks for a color.
    """
    moves: List[Move] = []

    for i in range(8):
      for j in range(8):
        piece = board.board[j][i]
        if piece[0] == c:
          moves.extend(self.move_functions[piece[1]](i, j, board))

    return moves

  def generate_valid_moves(self, board: Board, c: str) -> List[Move]:
    pass

  def get_checks_and_pins(self, board: Board, c: str) -> Tuple[bool, List[MoveBlockVector], List[MoveBlockVector]]:
    """
    Returns pins and checks of the board provided.
    :returns: (in_check, checks, pins)
    """
    pins: List[MoveBlockVector] = []
    checks: List[MoveBlockVector] = []
    in_check = False

    oppo = get_opposite_color(c)
    start_pos = self.wk_pos if c == 'w' else self.bk_pos
    for i in range(len(Movement.King)):
      d = Movement.King[i]
      possible_pin = None
      for mult in range(1, 8):
        ci = start_pos[0] + d[0] * mult
        cj = start_pos[1] + d[1] * mult
        if self.in_bounds(ci, cj):
          c_piece = board.board[cj][ci]
          if c_piece[0] == c and c_piece[1] != 'K':
            if possible_pin is None:
              possible_pin = MoveBlockVector(ci, cj, d)
            else:
              break
          elif c_piece[0] == oppo:
            enemy_piece_type = c_piece[1]
            enemy_piece_color = c_piece[0]
            is_rook_check = (0 <= i <= 3 and enemy_piece_type == 'R')
            is_bishop_check = (4 <= i <= 7 and enemy_piece_type == 'B')
            is_pawn_check = (mult == 1 and enemy_piece_type == 'P' and (
              (enemy_piece_color == 'w' and 6 <= i <= 7) or (enemy_piece_color == 'b' and 4 <= i <= 5)
            ))
            is_queen_check = enemy_piece_type == 'Q'
            is_king_check = (enemy_piece_type == 'K' and mult == 1)

            if any([is_rook_check, is_queen_check, is_bishop_check, is_pawn_check, is_king_check]):
              if possible_pin is None:
                in_check = True
                checks.append(MoveBlockVector(ci, cj, d))
                # No need to check further from this direction.
                break
              else:
                pins.append(possible_pin)
                break
            # Enemy is not applying checks.
            else:
              break
        # Off the board.
        else:
          break

    for move in Movement.Knight:
      ci, cj = start_pos[0] + move[0], start_pos[1] + move[1]
      if self.in_bounds(ci, cj):
        c_piece = board.board[cj][ci]
        if c_piece[0] == oppo and c_piece[1] == 'N':
          in_check = True
          checks.append(MoveBlockVector(ci, cj, move))

    return in_check, checks, pins
