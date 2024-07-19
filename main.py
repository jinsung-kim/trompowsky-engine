import pygame  # type: ignore

from engine import Engine
from gui import Gui
from board import Board
from ai import Ai
from move import Move

if __name__ == '__main__':
  pygame.init()
  pygame.display.set_caption('Chess')

  board = Board()
  engine = Engine(board)
  gui = Gui()
  ai = Ai(depth=3)

  def process_move(move: Move):
    board.make_move(move)
    board.log_move(move)

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

  board.log_game()

  pygame.quit()
