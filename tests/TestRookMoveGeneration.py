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


class TestRookMoveGeneration(unittest.TestCase):

  def setUp(self):
    self.board = Board(is_test_board=True)
    self.engine = Engine(self.board)

  def tearDown(self):
    self.board.clear_board()

  def test_rook_moves_from_center(self):
    self.board.board[3][3] = 'wR'
    actual_moves = self.engine.generate_rook_moves(3, 3)
    expected_moves = [
      Move(3, 3, 2, 3),
      Move(3, 3, 1, 3),
      Move(3, 3, 0, 3),
      Move(3, 3, 4, 3),
      Move(3, 3, 5, 3),
      Move(3, 3, 6, 3),
      Move(3, 3, 7, 3),
      Move(3, 3, 3, 2),
      Move(3, 3, 3, 1),
      Move(3, 3, 3, 0),
      Move(3, 3, 3, 4),
      Move(3, 3, 3, 5),
      Move(3, 3, 3, 6),
      Move(3, 3, 3, 7)
    ]

    self.assertEqual(sort_moves(actual_moves),
                     sort_moves(expected_moves))

  def test_rook_moves_with_friendly_pieces_blocking(self):
    self.board.board[3][3] = 'wR'
    self.board.board[3][5] = 'wP'  # Friendly piece blocking right.
    self.board.board[5][3] = 'wP'  # Friendly piece blocking down.

    expected_moves = [
      Move(3, 3, 2, 3), Move(3, 3, 1, 3), Move(3, 3, 0, 3),  # Left
      Move(3, 3, 3, 2), Move(3, 3, 3, 1), Move(3, 3, 3, 0),  # Up
      Move(3, 3, 4, 3),  # Right up to friendly piece
      Move(3, 3, 3, 4),  # Down up to friendly piece
    ]

    actual_moves = self.engine.generate_rook_moves(3, 3)
    self.assertEqual(sort_moves(actual_moves),
                     sort_moves(expected_moves))

  def test_rook_moves_with_enemy_pieces_blocking(self):
    self.board.board[3][3] = 'wR'
    self.board.board[3][5] = 'bP'  # Friendly piece blocking right.
    self.board.board[5][3] = 'bP'  # Friendly piece blocking down.

    expected_moves = [
      Move(3, 3, 2, 3), Move(3, 3, 1, 3), Move(3, 3, 0, 3),  # Left
      Move(3, 3, 3, 2), Move(3, 3, 3, 1), Move(3, 3, 3, 0),  # Up
      Move(3, 3, 4, 3),  Move(3, 3, 5, 3, True, SCORE_PIECE['P']),  # Right up to enemy piece.
      Move(3, 3, 3, 4),  Move(3, 3, 3, 5, True, SCORE_PIECE['P'])  # Down up to enemy piece.
    ]

    actual_moves = self.engine.generate_rook_moves(3, 3)
    self.assertEqual(sort_moves(actual_moves),
                     sort_moves(expected_moves))

  def test_rook_moves_from_edge(self):
    self.board.board[0][0] = 'wR'

    expected_moves = [
      Move(0, 0, 1, 0), Move(0, 0, 2, 0),
      Move(0, 0, 3, 0), Move(0, 0, 4, 0),
      Move(0, 0, 5, 0), Move(0, 0, 6, 0),
      Move(0, 0, 7, 0),  # Right
      Move(0, 0, 0, 1), Move(0, 0, 0, 2),
      Move(0, 0, 0, 3), Move(0, 0, 0, 4),
      Move(0, 0, 0, 5), Move(0, 0, 0, 6),
      Move(0, 0, 0, 7),  # Down
    ]

    actual_moves = self.engine.generate_rook_moves(0, 0)
    self.assertEqual(sort_moves(actual_moves),
                     sort_moves(expected_moves))

  def test_rook_capture_while_pinned(self):
   self.board.board[0][0] = 'wK'
   self.board.board[0][1] = 'wR'
   self.board.board[0][2] = 'bQ'
   self.engine.wk_pos = (0, 0)

   _, _, self.engine.pins = self.engine.get_checks_and_pins('w')
   # Pinned by queen on the right.
   self.assertEquals(len(self.engine.pins), 1)

   actual_moves = self.engine.generate_rook_moves(1, 0)
   self.assertEqual(len(actual_moves), 1)


if __name__ == '__main__':
  unittest.main()
