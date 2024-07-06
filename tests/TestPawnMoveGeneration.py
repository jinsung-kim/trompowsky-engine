import sys
import os
import unittest

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from board import Board
from engine import Engine
from move import Move, SCORE_PIECE
from helpers import sort_moves


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
    self.assertEqual(sort_moves(actual_moves),
                     sort_moves(expected_moves))

  def test_white_pawn_blocked(self):
    self.board.board[6][1] = 'wP'
    self.board.board[5][1] = 'bP'

    actual_moves = self.engine.generate_pawn_moves(1, 6)
    self.assertEqual(0, len(actual_moves))

  def test_black_pawn_blocked(self):
    self.board.board[1][1] = 'bP'
    self.board.board[2][1] = 'wP'

    actual_moves = self.engine.generate_pawn_moves(1, 1)
    self.assertEqual(0, len(actual_moves))

  def test_black_pawn_moves(self):
    self.board.board[1][1] = 'bP'

    expected_moves = [
      Move(1, 1, 1, 2),  # Single move forward.
      Move(1, 1, 1, 3)   # Double move forward from starting position.
    ]

    actual_moves = self.engine.generate_pawn_moves(1, 1)
    self.assertEqual(sort_moves(actual_moves),
                     sort_moves(expected_moves))

  def test_white_pawn_diagonal_moves(self):
    self.board.board[6][1] = 'wP'
    self.board.board[5][2] = 'bP'

    expected_moves = [
      Move(1, 6, 1, 5),
      Move(1, 6, 1, 4),
      Move(1, 6, 2, 5, True, SCORE_PIECE['P']),
    ]

    actual_moves = self.engine.generate_pawn_moves(1, 6)
    self.assertEqual(sort_moves(actual_moves),
                     sort_moves(expected_moves))

  def test_black_pawn_diagonal_moves(self):
    self.board.board[1][1] = 'bP'
    self.board.board[2][0] = 'wP'

    expected_moves = [
      Move(1, 1, 1, 2),
      Move(1, 1, 1, 3),
      Move(1, 1, 0, 2, True, SCORE_PIECE['P']),
    ]

    actual_moves = self.engine.generate_pawn_moves(1, 1)
    self.assertEqual(sort_moves(actual_moves),
                     sort_moves(expected_moves))

  def test_white_pawn_promotion_moves(self):
    self.board.board[1][1] = 'wP'
    self.board.board[0][0] = 'bP'
    self.board.board[0][1] = 'bP'

    expected_moves = [
      Move(1, 1, 0, 0, True, SCORE_PIECE['Q'] + SCORE_PIECE['P'])
    ]

    actual_moves = self.engine.generate_pawn_moves(1, 1)
    self.assertEqual(sort_moves(actual_moves),
                     sort_moves(expected_moves))

  def test_black_pawn_promotion_moves(self):
    self.board.board[6][1] = 'bP'
    self.board.board[7][1] = 'wP'
    self.board.board[7][2] = 'wP'

    expected_moves = [
      Move(1, 6, 2, 7, True, SCORE_PIECE['Q'] + SCORE_PIECE['P'])
    ]

    actual_moves = self.engine.generate_pawn_moves(1, 6)
    self.assertEqual(sort_moves(actual_moves),
                     sort_moves(expected_moves))


if __name__ == '__main__':
  unittest.main()
