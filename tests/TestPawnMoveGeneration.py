import sys
import os
import unittest

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from board import Board
from engine import Engine
from move import Move, SCORE_PIECE


class TestPawnMoveGeneration(unittest.TestCase):

  def setUp(self):
    self.board = Board(is_test_board=True)
    self.engine = Engine(self.board)

  def tearDown(self):
    self.board.clear_board()

  def test_white_pawn_moves(self):
    self.board.board[6][1] = 'wP'

    expected_moves = [
      Move(1, 6, 1, 5),  # Single move forward.
      Move(1, 6, 1, 4)   # Double move forward from starting position.
    ]

    actual_moves = self.engine.generate_pawn_moves(1, 6)
    self.assertEqual(sorted(actual_moves, key=lambda m: (m.nj, m.ni)), sorted(expected_moves, key=lambda m: (m.nj, m.ni)))

  def test_black_pawn_moves(self):
    self.board.board[1][1] = 'bP'

    expected_moves = [
      Move(1, 1, 1, 2),  # Single move forward.
      Move(1, 1, 1, 3)   # Double move forward from starting position.
    ]

    actual_moves = self.engine.generate_pawn_moves(1, 1)
    self.assertEqual(sorted(actual_moves, key=lambda m: (m.nj, m.ni)), sorted(expected_moves, key=lambda m: (m.nj, m.ni)))


if __name__ == '__main__':
  unittest.main()
