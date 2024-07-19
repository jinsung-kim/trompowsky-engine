from typing import Optional, List

import pygame  # type: ignore
from board import Board
from engine import Engine
from helpers import truncate

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
    self.clicks: List[tuple[int, int]] = []

  @staticmethod
  def round_coords(x, y) -> tuple[int, int]:
    """
    Takes the raw (x,y) coordinates and converts them into what the board is compatible with.
    :return: (i, j) coords.
    """
    i = int(truncate(x / 50, 0))
    j = int(truncate(y / 50, 0))
    return i, j

  def register_click(self, i, j, board: Board) -> bool:
    if self.last_selected is not None and self.last_selected == (i, j):
      self.clicks.clear()
      self.last_selected = None
    if 'w' in board.board[j][i]:
      self.last_selected = (i, j)
      self.clicks.append((i, j))
      return True
    else:
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

  def draw_pieces(self, board: Board):
    for i in range(8):
      for j in range(8):
        if board.board[j][i] != "--":
          self.game_display.blit(image_dict[board.board[j][i]], ((i * 50) - 5, (j * 50) - 5))

  def highlight_moves(self, engine: Engine):
    if self.last_selected is not None:
      i, j = self.last_selected
      piece = engine.board.board[j][i]
      if piece == '--':
        return

      self.draw_square(i * 50, j * 50, YELLOW)

      valid_moves = engine.generate_valid_moves('w')
      for move in valid_moves:
        if move.i == i and move.j == j:
          ci, cj = move.ni * 50, move.nj * 50
          self.draw_square(ci, cj, BLUE_LIGHT)

  def update_game_state(self, engine):
    self.draw_board()
    self.highlight_moves(engine)
    self.draw_pieces(engine.board)
    pygame.display.update()
