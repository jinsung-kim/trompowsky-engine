from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame  # type: ignore

from engine import Engine
from gui import Gui
from board import Board
from ai import Ai
from move import Move

if __name__ == '__main__':
  pygame.init()
  pygame.display.set_caption('Chess')
  pygame.display.set_icon(pygame.image.load("assets/wK.png"))

  board = Board()
  engine = Engine(board)
  gui = Gui()
  # Recommend 3 for smooth instant move generation. TODO: Need to thread this somehow.
  ai = Ai(depth=4)

  def process_move(move: Move):
    board.make_move(move)
    # Since white went, we can assume that it would not put the king in check.
    gui.update_game_state(engine, skip_white_check=True)

    engine.refresh_moves_and_game_state('b')
    board.log_move(move, engine.in_check, engine.checkmate)

    if engine.check_game_over():
      return False
    ai.make_optimal_move(engine)

    gui.update_game_state(engine)
    return not engine.check_game_over()

  running = True

  gui.update_game_state(engine)
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
        gui.exit = True
      elif event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:  # Left mouse button.
          engine.refresh_moves_and_game_state('w')

          mouse_cor = pygame.mouse.get_pos()
          mouse_x_cor, mouse_y_cor = mouse_cor[0], mouse_cor[1]
          i, j = gui.round_coords(mouse_x_cor, mouse_y_cor)
          valid_move_click_registered = gui.register_click(i, j, engine)
          gui.update_game_state(engine)

          if valid_move_click_registered:
            (pi, pj) = gui.last_selected
            current_move = Move(pi, pj, i, j)
            running = process_move(current_move)

  while not gui.exit:
    for event in pygame.event.get():
      gui.exit = True

  board.log_game()

  pygame.quit()
