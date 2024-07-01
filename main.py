import pygame # type: ignore
from gui import Gui
from board import Board


if __name__ == '__main__':
  pygame.init()
  pygame.display.set_caption('Chess')

  board = Board()
  gui = Gui()

  print('Starting game.')

  running = True
  while running:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False

    gui.update_game_state(board = board)

  print('Ending game.')

  pygame.quit()