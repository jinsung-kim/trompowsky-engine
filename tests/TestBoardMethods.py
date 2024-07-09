import sys
import os
import unittest

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from board import Board, EMPTY_BOARD
from engine import Engine


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


if __name__ == '__main__':
  unittest.main()
