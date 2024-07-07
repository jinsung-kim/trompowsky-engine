import sys
import os
import unittest
from typing import List

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from board import Board, EMPTY_BOARD
from engine import Engine
from move import Move


class TestBoardMethods(unittest.TestCase):
  def setUp(self):
   self.board = Board(is_test_board=False)
   self.engine = Engine()

  def test_board_clear(self):
    self.board.board[3][3] = 'wQ'
    found_wq = any('wQ' in row for row in self.board.board)
    self.assertEqual(found_wq, True)  # flatten board and check that wQ is there.

    self.board.clear_board()

    self.assertEqual(self.board.board, EMPTY_BOARD)

  def test_initial_move_generation(self):
    moves: List[Move] = []

    for i in range(8):
      for j in range(8):
        if self.board.board[j][i][0] == 'w':
          moves.extend(self.engine.generate_potential_moves(i, j, self.board))
          
    # Only twenty ways to begin a match.
    self.assertEqual(len(moves), 20)


if __name__ == '__main__':
  unittest.main()
