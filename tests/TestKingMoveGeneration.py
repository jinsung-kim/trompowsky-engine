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

  def test_king_with_opposing_threat(self):
    self.board.board[0][0] = 'wK'
    self.board.board[1][1] = 'bR'
    self.engine.wk_pos = (0, 0)

    expected_moves = [
      Move(0, 0, 1, 1)
    ]

    actual_moves = self.engine.generate_king_moves(0, 0)
    self.assertEqual(sort_moves(actual_moves),
                     sort_moves(expected_moves))

  def test_king_with_opposing_pawn_threat(self):
    self.board.board[0][0] = 'bK'
    self.board.board[1][2] = 'wP'
    self.board.bk_pos = (0, 0)

    expected_moves = [
      Move(0, 0, 0, 1),
      Move(0, 0, 1, 1)
    ]
    actual_moves = self.engine.generate_king_moves(0, 0)
    self.assertEqual(sort_moves(actual_moves),
                     sort_moves(expected_moves))

  def test_king_with_opposing_pawn_threat_with_friendly_block(self):
    self.board.board[2][2] = 'wK'
    self.board.board[0][0] = 'bP'
    self.board.board[1][1] = 'bN'
    self.board.wk_pos = (2, 2)

    actual_moves = self.engine.generate_king_moves(2, 2)
    self.assertEqual(len(actual_moves), 5)

    in_check, _, pins = self.engine.get_checks_and_pins('w')
    self.assertEqual(in_check, False)
    self.assertEqual(len(pins), 0)

  def test_king_check(self):
    self.board.board[3][3] = 'wK'
    self.board.wk_pos = (3, 3)
    self.board.board[0][0] = 'bB'

    in_check, _, _ = self.engine.get_checks_and_pins('w')
    self.assertEqual(in_check, True)

  def test_king_double_check(self):
    self.board.board[3][3] = 'wK'
    self.board.board[0][0] = 'bB'
    self.board.board[3][0] = 'bR'
    self.board.wk_pos = (3, 3)

    in_check, checks, pins = self.engine.get_checks_and_pins('w')
    self.assertEqual(in_check, True)
    self.assertEqual(len(checks), 2)
    self.assertEqual(len(pins), 0)

  def test_king_stalemate(self):
    self.board.board[0][0] = 'bK'
    self.board.board[1][1] = 'wR'
    self.board.board[2][2] = 'wP'
    self.board.bk_pos = (0, 0)

    actual_moves = self.engine.generate_king_moves(0, 0)
    self.assertEqual(len(actual_moves), 0)

  def test_two_kings(self):
    self.board.board[0][0] = 'bK'
    self.board.board[3][3] = 'wK'

    self.board.bk_pos = (0, 0)
    self.board.wk_pos = (0, 0)

    actual_moves = self.engine.generate_king_moves(0, 0)
    self.assertEqual(len(actual_moves), 3)

  def test_two_kings_close(self):
    self.board.board[0][0] = 'bK'
    self.board.board[2][1] = 'wK'

    self.board.bk_pos = (0, 0)
    self.board.wk_pos = (1, 2)

    actual_moves = self.engine.generate_king_moves(0, 0)
    self.assertEqual(len(actual_moves), 1)


if __name__ == '__main__':
  unittest.main()
