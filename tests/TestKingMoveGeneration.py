import sys
import os
import unittest

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from board import Board
from engine import Engine
from move import Move
from helpers import sort_moves


class TestKingMoveGeneration(unittest.TestCase):

  def setUp(self):
    self.board = Board(is_test_board=True)
    self.engine = Engine(self.board)

  def tearDown(self):
    self.board.clear_board()

  def test_king_center_moves(self):
    self.board.board[3][3] = 'wK'

    expected_moves = [
      Move(3, 3, 2, 2),  # Top-left
      Move(3, 3, 2, 3),  # Top
      Move(3, 3, 2, 4),  # Top-right
      Move(3, 3, 3, 2),  # Left
      Move(3, 3, 3, 4),  # Right
      Move(3, 3, 4, 2),  # Bottom-left
      Move(3, 3, 4, 3),  # Bottom
      Move(3, 3, 4, 4)   # Bottom-right
    ]

    actual_moves = self.engine.generate_king_moves(3, 3)
    self.assertEqual(sort_moves(actual_moves),
                     sort_moves(expected_moves))

  def test_king_in_corner(self):
    self.board.board[0][0] = 'wK'

    expected_moves = [
      Move(0, 0, 1, 0),
      Move(0, 0, 0, 1),
      Move(0, 0, 1, 1)
    ]

    actual_moves = self.engine.generate_king_moves(0, 0)
    self.assertEqual(sort_moves(actual_moves),
                     sort_moves(expected_moves))

  def test_king_with_friendly_blocking(self):
    self.board.board[3][3] = 'wK'
    self.board.board[2][3] = 'wP'  # Friendly piece blocking top.
    self.board.board[4][4] = 'wP'  # Friendly piece blocking bottom-right.
    self.board.board[3][2] = 'wP'  # Friendly piece blocking left.

    expected_moves = [
      Move(3, 3, 2, 2),  # Top-left
      Move(3, 3, 2, 4),  # Top-right
      Move(3, 3, 3, 4),  # Right
      Move(3, 3, 4, 2),  # Bottom-left
      Move(3, 3, 4, 3)   # Bottom
    ]

    actual_moves = self.engine.generate_king_moves(3, 3)
    self.assertEqual(sort_moves(actual_moves),
                     sort_moves(expected_moves))


if __name__ == '__main__':
  unittest.main()