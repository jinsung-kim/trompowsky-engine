import sys
import os
import unittest

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from board import Board
from engine import Engine
from move import Move


class TestKnightMoveGeneration(unittest.TestCase):

  def setUp(self):
    self.board = Board(is_test_board=True)
    self.engine = Engine(self.board)

  def tearDown(self):
    self.board.clear_board()

  def test_knight_center_moves(self):
    self.board.board[3][3] = 'wN'

    expected_moves = [
      Move(3, 3, 1, 2),  # Up-left
      Move(3, 3, 1, 4),  # Up-right
      Move(3, 3, 2, 1),  # Left-up
      Move(3, 3, 2, 5),  # Right-up
      Move(3, 3, 4, 1),  # Left-down
      Move(3, 3, 4, 5),  # Right-down
      Move(3, 3, 5, 2),  # Down-left
      Move(3, 3, 5, 4)   # Down-right
    ]

    actual_moves = self.engine.generate_knight_moves(3, 3)
    self.assertEqual(sorted(actual_moves, key=lambda m: (m.ni, m.nj)),
                     sorted(expected_moves, key=lambda m: (m.ni, m.nj)))

  def test_knight_corner_moves(self):
    self.board.board[0][0] = 'wN'

    expected_moves = [
      Move(0, 0, 2, 1),
      Move(0, 0, 1, 2),
    ]

    actual_moves = self.engine.generate_knight_moves(0, 0)
    self.assertEqual(sorted(actual_moves, key=lambda m: (m.ni, m.nj)),
                     sorted(expected_moves, key=lambda m: (m.ni, m.nj)))


if __name__ == '__main__':
  unittest.main()
