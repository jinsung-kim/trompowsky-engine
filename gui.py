from typing import Optional

import pygame  # type: ignore
from board import Board
from engine import Engine
from helpers import truncate
from move import Move

DISPLAY_HEIGHT = 400
DISPLAY_WIDTH = 400
SQUARE_SIDE = 50

RED_CHECK = (240, 150, 150)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE_LIGHT = (140, 184, 219)
BLUE_DARK = (91, 131, 159)
GRAY_LIGHT = (240, 240, 240)
GRAY_DARK = (200, 200, 200)
BROWN = (160, 82, 45)

bB = pygame.image.load("assets/bB.png")
bK = pygame.image.load("assets/bK.png")
bN = pygame.image.load("assets/bN.png")
bP = pygame.image.load("assets/bP.png")
bQ = pygame.image.load("assets/bQ.png")
bR = pygame.image.load("assets/bR.png")

wB = pygame.image.load("assets/wB.png")
wK = pygame.image.load("assets/wK.png")
wN = pygame.image.load("assets/wN.png")
wP = pygame.image.load("assets/wP.png")
wQ = pygame.image.load("assets/wQ.png")
wR = pygame.image.load("assets/wR.png")

image_dict = {
  "bB": bB,
  "bK": bK,
  "bN": bN,
  "bP": bP,
  "bQ": bQ,
  "bR": bR,
  "wB": wB,
  "wK": wK,
  "wN": wN,
  "wP": wP,
  "wQ": wQ,
  "wR": wR
}


class Gui:

  def __init__(self):
    self.game_display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    self.last_selected: Optional[tuple[int, int]] = None
    self.exit: bool = False

  @staticmethod
  def round_coords(x, y) -> tuple[int, int]:
    """
    Takes the raw (x,y) coordinates and converts them into what the board is compatible with.
    :return: (i, j) coords.
    """
    i = int(truncate(x / 50, 0))
    j = int(truncate(y / 50, 0))
    return i, j

  def register_click(self, i, j, engine: Engine) -> bool:
    """
    Register the click.
    :return: Whether the input has led to a valid move.
    """
    # Deselect current selection.
    if self.last_selected is not None and self.last_selected == (i, j):
      self.last_selected = None
      return False
    # Trying to initiate a move.
    if 'w' in engine.board.board[j][i]:
      self.last_selected = (i, j)
      return False
    # Potentially capturing another piece.
    elif self.last_selected is not None:
      for potential_move in engine.white_moves:
        if potential_move == Move(self.last_selected[0], self.last_selected[1], i, j):
          return True
      # An invalid move was selected.
      self.last_selected = None
      return False

  def draw_board(self):
    self.game_display.fill(GRAY_DARK)
    for i in range(4):
      for j in range(4):
        ci, cj = i * 100, j * 100
        self.draw_square(ci, cj, WHITE)
        self.draw_square(ci + SQUARE_SIDE, cj + SQUARE_SIDE, WHITE)

  def draw_square(self, i, j, color):
    pygame.draw.rect(self.game_display, color,
                     pygame.Rect(i, j, SQUARE_SIDE, SQUARE_SIDE))

  def draw_circle(self, i, j, color, radius=5):
    pygame.draw.circle(self.game_display, color, (i, j), radius)

  def draw_pieces(self, board: Board):
    for i in range(8):
      for j in range(8):
        if board.board[j][i] != "--":
          self.game_display.blit(image_dict[board.board[j][i]], ((i * 50) - 5, (j * 50) - 5))

  def highlight_moves(self, engine: Engine):
    if self.last_selected is not None:
      i, j = self.last_selected
      if engine.board.board[j][i] == '--':
        return
      self.draw_square(i * 50, j * 50, BLUE_DARK)

      valid_moves = engine.generate_valid_moves('w')
      for move in valid_moves:
        if move.i == i and move.j == j:
          if move.captured_piece is None:
            ci, cj = move.ni * 50 + 25, move.nj * 50 + 25
            self.draw_circle(ci, cj, BLUE_LIGHT)
          else:
            ci, cj = move.ni * 50, move.nj * 50
            self.draw_square(ci, cj, YELLOW)

  def update_game_state(self, engine):
    self.draw_board()
    self.highlight_moves(engine)
    self.draw_pieces(engine.board)
    pygame.display.update()
