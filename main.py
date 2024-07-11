import pygame  # type: ignore

from engine import Engine
from gui import Gui
from board import Board
from move import Move

if __name__ == '__main__':
  pygame.init()
  pygame.display.set_caption('Chess')

  board = Board()
  engine = Engine(board)
  gui = Gui()

  print('Starting game.')

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
              board.make_move(current_move)

      gui.update_game_state(engine)

  print('Ending game.')

  pygame.quit()
