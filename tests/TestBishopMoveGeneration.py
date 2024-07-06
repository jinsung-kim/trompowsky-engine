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


class TestBishopMoveGeneration(unittest.TestCase):

  def setUp(self):
    self.board = Board(is_test_board=True)
    self.engine = Engine()

  def tearDown(self):
    self.board.clear_board()

  def test_bishop_moves_from_center(self):
    self.board.board[3][3] = 'wB'

    expected_moves = [
      Move(3, 3, 2, 2), Move(3, 3, 1, 1), Move(3, 3, 0, 0),  # Top-left
      Move(3, 3, 4, 4), Move(3, 3, 5, 5), Move(3, 3, 6, 6),
      Move(3, 3, 7, 7),  # Bottom-right
      Move(3, 3, 2, 4), Move(3, 3, 1, 5), Move(3, 3, 0, 6),  # Bottom-left
      Move(3, 3, 4, 2), Move(3, 3, 5, 1), Move(3, 3, 6, 0),  # Top-right
    ]

    actual_moves = self.engine.generate_bishop_moves(3, 3, self.board)
    self.assertEqual(sort_moves(actual_moves),
                     sort_moves(expected_moves))

  def test_bishop_moves_with_friendly_pieces_blocking(self):
    self.board.board[3][3] = 'wB'
    self.board.board[2][2] = 'wP'  # Friendly piece blocking top-left diagonal.
    self.board.board[4][4] = 'wP'  # Friendly piece blocking bottom-right diagonal.

    expected_moves = [
      Move(3, 3, 0, 6),
      Move(3, 3, 1, 5),
      Move(3, 3, 2, 4),
      Move(3, 3, 4, 2),
      Move(3, 3, 5, 1),
      Move(3, 3, 6, 0)
    ]

    actual_moves = self.engine.generate_bishop_moves(3, 3, self.board)
    self.assertEqual(sort_moves(actual_moves),
                     sort_moves(expected_moves))

  def test_bishop_moves_with_opposing_pieces_blocking(self):
    self.board.board[3][3] = 'wB'
    self.board.board[2][2] = 'bP'  # Enemy piece blocking top-left diagonal.
    self.board.board[4][4] = 'bP'  # Enemy piece blocking bottom-right diagonal.

    expected_moves = [
      Move(3, 3, 0, 6),
      Move(3, 3, 1, 5),
      Move(3, 3, 2, 4),
      Move(3, 3, 4, 2),
      Move(3, 3, 5, 1),
      Move(3, 3, 6, 0),
      Move(3, 3, 2, 2, True, SCORE_PIECE['P']),
      Move(3, 3, 4, 4, True, SCORE_PIECE['P'])
    ]

    actual_moves = self.engine.generate_bishop_moves(3, 3, self.board)
    self.assertEqual(sort_moves(actual_moves),
                     sort_moves(expected_moves))

  def test_bishop_moves_from_edge(self):
    self.board.board[0][0] = 'wB'

    expected_moves = [
      Move(0, 0, 1, 1),
      Move(0, 0, 2, 2),
      Move(0, 0, 3, 3),
      Move(0, 0, 4, 4),
      Move(0, 0, 5, 5),
      Move(0, 0, 6, 6),
      Move(0, 0, 7, 7),
    ]

    actual_moves = self.engine.generate_bishop_moves(0, 0, self.board)
    self.assertEqual(sort_moves(actual_moves),
                     sort_moves(expected_moves))


if __name__ == '__main__':
  unittest.main()
