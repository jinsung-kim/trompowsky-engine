import pygame  # type: ignore
from board import Board
from engine import Engine

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

  # TODO: Take user input -> Generate valid moves for that piece -> Highlight them.
  def highlight_moves(self, engine: Engine, board: Board):
    pass

  def update_game_state(self, board):
    self.draw_board()
    self.draw_pieces(board)
    pygame.display.update()
