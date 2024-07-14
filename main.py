import pygame  # type: ignore

from engine import Engine
from gui import Gui
from board import Board
from ai import Ai
from move import Move
from random import choice

MAX_FPS = 30

if __name__ == '__main__':
  pygame.init()
  pygame.display.set_caption('Chess')

  board = Board()
  engine = Engine(board)
  gui = Gui()
  ai = Ai(depth=3)

  clock = pygame.time.Clock()
  clock.tick(MAX_FPS)

  def process_move(move: Move):
    board.make_move(move)
    board.log_move(move)

    valid_ai_moves = engine.generate_valid_moves('b')
    if engine.checkmate:
      print('White wins. Black was checkmated.')
      return False
    elif engine.stalemate:
      print('Tie. Stalemate.')
      return False

    optimal_move = ai.find_optimal_move(valid_ai_moves, engine)

    # FIXME: Prevent the AI from actually capturing the king.
    if optimal_move is None:
      random_move = choice(valid_ai_moves)
      board.make_move(random_move)
      board.log_move(random_move)
    else:
      board.make_move(optimal_move)
      board.log_move(optimal_move)

    _ = engine.generate_valid_moves('w')
    if engine.checkmate:
      print('Black wins. White was checkmated.')
      return False
    elif engine.stalemate:
      print('Tie. Stalemate.')
      return False

    return True

  running = True
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
      elif event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:  # Left mouse button.
          mouse_cor = pygame.mouse.get_pos()
          mouse_x_cor = mouse_cor[0]
          mouse_y_cor = mouse_cor[1]
          i, j = gui.round_coords(mouse_x_cor, mouse_y_cor)
          gui.register_click(i, j, board)
          if gui.last_selected is not None and gui.last_selected != (i, j):
            (pi, pj) = gui.last_selected
            valid_moves = engine.generate_valid_moves('w')
            current_move = Move(pi, pj, i, j)
            if current_move in valid_moves:
              running = process_move(current_move)

      gui.update_game_state(engine)

  board.log_game()

  while True:
    continue

  # pygame.quit()
