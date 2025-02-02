from board import Board
from typing import List, Callable, Tuple, Optional
from helpers import get_opposite_color, Movement
from move import Move, MoveBlockVector
from math import gcd


class Engine:

  def __init__(self, board: Board) -> None:
    self.move_functions = {
      'P': self.generate_pawn_moves,
      'N': self.generate_knight_moves,
      'R': self.generate_rook_moves,
      'K': self.generate_king_moves,
      'Q': self.generate_queen_moves,
      'B': self.generate_bishop_moves,
    }

    self.board: Board = board

    self.in_check = False
    self.pins: List[MoveBlockVector] = []
    self.checks: List[MoveBlockVector] = []

    # Game state
    self.checkmate = False
    self.stalemate = False
    self.winner = None

    # Instead of calling generate_valid_moves in a bunch of places,
    # Reuse them when the game state has not been updated.
    self.white_moves: List[Move] = []
    self.black_moves: List[Move] = []

  @staticmethod
  def in_bounds(i: int, j: int) -> bool:
    return 0 <= i < 8 and 0 <= j < 8

  @staticmethod
  def infer_direction(move: Move) -> Tuple[int, int]:
    di = move.ni - move.i
    dj = move.nj - move.j

    # Normalize the direction by dividing by the GCD of di and dj.
    g = gcd(abs(di), abs(dj))
    return di // g, dj // g

  def return_valid_move(self, i, j, ni, nj) -> Optional[Move]:
    color = self.board.board[j][i][0]
    oppo = 'b' if color == 'w' else 'w'
    new_pos = self.board.board[nj][ni]
    if new_pos == '--':
      return Move(i, j, ni, nj, None)
    elif oppo == new_pos[0]:
      return Move(i, j, ni, nj, new_pos)
    else:
      return None

  def check_game_over(self) -> bool:
    return any([self.checkmate, self.stalemate])

  def refresh_moves_and_game_state(self, c: str):
    """
    Used to refresh the white moves given the game state.
    ALso refreshes the game state. A checkmate right after this call indicates a white win.
    """
    valid_moves = self.generate_valid_moves(c)

    if c == 'w':
      self.white_moves = valid_moves
    else:
      self.black_moves = valid_moves

  def find_pin(self, i, j, is_queen: bool) -> Optional[MoveBlockVector]:
    """
    Finds and returns (if applicable) the first pin for the position.
    NOTE: Will also remove the pin (assuming that the move generation will handle it).

    """
    pin: Optional[MoveBlockVector] = None

    for pinned_vector in self.pins[::-1]:
      if i == pinned_vector.i and j == pinned_vector.j:
        pin = pinned_vector
        # Since the queen calls both rook + bishop move generation functions, only allow the bishop move generator
        # to remove pins. This avoids situations where the engine believes the queen is no longer pinned, when it's not.
        if not is_queen:
          self.pins.remove(pinned_vector)
        break
    return pin

  def generate_valid_moves_for_piece(self, i, j, directions, is_queen: bool) -> List[Move]:
    pin: Optional[MoveBlockVector] = self.find_pin(i, j, is_queen)

    moves: List[Move] = []
    for direction in directions:
      moves.extend(self.generate_moves_in_direction(i, j, direction))

    if pin is None:
      return moves

    valid_moves: List[Move] = []
    for move in moves:
      move_d = self.infer_direction(move)

      if move_d == pin.d or tuple(d * -1 for d in pin.d) == move_d:
        valid_moves.append(move)

    return valid_moves

  def generate_moves_in_direction(self, i: int, j: int,
                                  direction: Callable[[int, int], Tuple[int, int]]) -> List[Move]:
    moves: List[Move] = []
    ni, nj = direction(i, j)
    while self.in_bounds(ni, nj):
      move_maybe = self.return_valid_move(i, j, ni, nj)
      if move_maybe is not None:
        moves.append(move_maybe)
        if move_maybe.captured_piece:
          break
      else:
        break
      ni, nj = direction(ni, nj)
    return moves

  def generate_moves_for_direction(self, i, j, d) -> List[Move]:
    moves: List[Move] = []

    for (di, dj) in d:
      ni = i + di
      nj = j + dj
      if self.in_bounds(ni, nj):
        move_maybe = self.return_valid_move(i, j, ni, nj)
        if move_maybe is not None:
          moves.append(move_maybe)

    return moves

  def generate_rook_moves(self, i, j) -> List[Move]:
    directions = [
      lambda x, y: (x - 1, y),  # Left
      lambda x, y: (x + 1, y),  # Right
      lambda x, y: (x, y - 1),  # Up
      lambda x, y: (x, y + 1)  # Down
    ]
    is_queen = self.board.board[j][i][1] == 'Q'

    return self.generate_valid_moves_for_piece(i, j, directions, is_queen)

  def generate_bishop_moves(self, i, j) -> List[Move]:
    directions = [
      lambda x, y: (x - 1, y - 1),  # Top left
      lambda x, y: (x + 1, y - 1),  # Top right
      lambda x, y: (x - 1, y + 1),  # Bottom left
      lambda x, y: (x + 1, y + 1)  # Bottom right
    ]

    return self.generate_valid_moves_for_piece(i, j, directions, False)

  def generate_queen_moves(self, i, j) -> List[Move]:
    return self.generate_rook_moves(i, j) + self.generate_bishop_moves(i, j)

  def generate_pawn_moves(self, i, j) -> List[Move]:
    moves: List[Move] = []
    pin: Optional[MoveBlockVector] = self.find_pin(i, j, False)

    color = self.board.board[j][i][0]
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

    if 0 <= nj < 8 and self.board.board[nj][i] == '--' and (pin is None or pin.d == (0, direction)):
      moves.append(Move(i, j, i, nj, None, nj == promotion_row))

      nj += direction
      if j == start_row and self.board.board[nj][i] == '--' and (pin is None or pin.d == (0, direction)):
        moves.append(Move(i, j, i, nj))  # Can't be promoted given starting position.

    for di in [-1, 1]:
      ni = i + di
      nj = j + direction

      if self.in_bounds(ni, nj):
        new_pos = self.board.board[nj][ni]
        if oppo == new_pos[0] and (pin is None or pin.d == (di, direction)):
          moves.append(Move(i, j, ni, nj, new_pos, nj == promotion_row))

    return moves

  def generate_knight_moves(self, i, j) -> List[Move]:
    is_pinned = False
    for pinned_vector in self.pins[::-1]:
      if i == pinned_vector.i and j == pinned_vector.j:
        is_pinned = True
        break

    if is_pinned:
      return []
    else:
      return self.generate_moves_for_direction(i, j, Movement.Knight)

  def generate_king_moves(self, i, j) -> List[Move]:
    c = self.board.board[j][i][0]

    moves: List[Move] = self.generate_moves_for_direction(i, j, Movement.King)
    valid_moves: List[Move] = []
    for move in moves:
      if c == 'w':
        self.board.wk_pos = (move.ni, move.nj)
      else:
        self.board.bk_pos = (move.ni, move.nj)

      in_check, _, _ = self.get_checks_and_pins(c)

      if not in_check:
        valid_moves.append(move)

    if c == 'w':
      self.board.wk_pos = (i, j)
    else:
      self.board.bk_pos = (i, j)

    return valid_moves

  def generate_valid_moves(self, c: str) -> List[Move]:
    """
    Returns all moves accounting for checks.
    """
    self.in_check, self.checks, self.pins = self.get_checks_and_pins(c)
    if c == 'w':
      k_pos = self.board.wk_pos
    else:
      k_pos = self.board.bk_pos

    if self.in_check:
      if len(self.checks) == 1:
        moves = self.generate_all_moves(c)
        check: MoveBlockVector = self.checks[0]
        piece_checking = self.board.board[check.j][check.i]
        valid_squares = []

        if piece_checking[1] == 'N':  # If knight is checking the king, the only valid move is to capture it/run away.
          valid_squares = [(check.i, check.j)]
        else:
          for i in range(1, 8):
            valid_square = (k_pos[0] + check.d[0] * i, k_pos[1] + check.d[1] * i)
            valid_squares.append(valid_square)
            if valid_square[0] == check.i and valid_square[1] == check.j:
              break

        # Remove moves that don't block the check or move the king.
        for move in moves[::-1]:
          if self.board.board[move.j][move.i][1] != 'K' and not (move.ni, move.nj) in valid_squares:
            moves.remove(move)
      else:  # Double check, can only move king.
        moves = self.generate_king_moves(k_pos[0], k_pos[1])
    else:  # Not in check, any move is fair game.
      moves = self.generate_all_moves(c)

    if len(moves) == 0:
      if self.in_check:
        self.checkmate = True
        self.winner = get_opposite_color(c)
      else:
        self.stalemate = True
    else:
      self.checkmate = False
      self.stalemate = False

    return moves

  def generate_all_moves(self, c: str) -> List[Move]:
    """
    Generates all possible moves without considering checks for a color.
    """
    moves: List[Move] = []

    for i in range(8):
      for j in range(8):
        piece = self.board.board[j][i]
        if piece[0] == c:
          moves.extend(self.move_functions[piece[1]](i, j))

    return moves

  def get_checks_and_pins(self, c: str) -> Tuple[bool, List[MoveBlockVector], List[MoveBlockVector]]:
    """
    Returns pins and checks of the board provided.
    :returns: (in_check, checks, pins)
    """
    pins: List[MoveBlockVector] = []
    checks: List[MoveBlockVector] = []
    in_check = False

    oppo = get_opposite_color(c)
    start_pos = self.board.wk_pos if c == 'w' else self.board.bk_pos

    for i in range(len(Movement.King)):
      d = Movement.King[i]
      possible_pin = None
      for mult in range(1, 8):
        ci = start_pos[0] + (d[0] * mult)
        cj = start_pos[1] + (d[1] * mult)
        if self.in_bounds(ci, cj):
          c_piece = self.board.board[cj][ci]
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
        else:
          break

    for move in Movement.Knight:
      ci, cj = start_pos[0] + move[0], start_pos[1] + move[1]
      if self.in_bounds(ci, cj):
        c_piece = self.board.board[cj][ci]
        if c_piece[0] == oppo and c_piece[1] == 'N':
          in_check = True
          checks.append(MoveBlockVector(ci, cj, move))

    return in_check, checks, pins
