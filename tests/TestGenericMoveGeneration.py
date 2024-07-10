import sys
import os
import unittest
from typing import List

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from board import Board
from engine import Engine
from move import Move


class TestGenericMoveGeneration(unittest.TestCase):
  def setUp(self):
    self.board = Board(is_test_board=False)
    self.engine = Engine(self.board)

  def test_initial_move_generation(self):
    moves: List[Move] = self.engine.generate_all_moves('w')

    # Only twenty ways to begin a match.
    self.assertEqual(len(moves), 20)

  def test_infer_direction(self):
    test_cases = [
      (Move(3, 3, 6, 6), (1, 1)),      # Diagonal move down-right.
      (Move(3, 3, 0, 0), (-1, -1)),    # Diagonal move up-left.
      (Move(1, 1, 1, 5), (0, 1)),      # Vertical move down.
      (Move(4, 4, 4, 0), (0, -1)),     # Vertical move up.
      (Move(2, 2, 6, 2), (1, 0)),      # Horizontal move right.
      (Move(7, 7, 3, 7), (-1, 0)),     # Horizontal move left.
      (Move(5, 5, 1, 9), (-1, 1)),     # Diagonal move down-left.
      (Move(2, 2, 6, 6), (1, 1)),      # Diagonal move down-right.
    ]

    for move, expected in test_cases:
      self.assertEqual(self.engine.infer_direction(move), expected)

  def test_valid_move_generation(self):
    moves: List[Move] = self.engine.generate_valid_moves('w')

    # Should be twenty valid ways to begin a match.
    self.assertEqual(len(moves), 20)

  def test_checkmate_status(self):
    self.board.clear_board()
    self.board.board[0][0] = 'wK'
    self.board.board[0][4] = 'bR'
    self.board.board[1][3] = 'bR'
    self.engine.wk_pos = (0, 0)

    actual_moves = self.engine.generate_valid_moves('w')
    self.assertEqual(self.engine.in_check, True)
    self.assertEqual(self.engine.checkmate, True)
    self.assertEqual(len(actual_moves), 0)

  def test_stalemate_status(self):
    self.board.clear_board()
    self.board.board[0][0] = 'wK'
    self.board.board[0][1] = 'wB'
    self.board.board[0][4] = 'bR'
    self.board.board[1][3] = 'bR'
    self.engine.wk_pos = (0, 0)

    actual_moves = self.engine.generate_valid_moves('w')
    self.assertEqual(self.engine.in_check, False)
    self.assertEqual(self.engine.checkmate, False)
    self.assertEqual(len(actual_moves), 0)


if __name__ == '__main__':
  unittest.main()
