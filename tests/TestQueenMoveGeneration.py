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


class TestQueenMoveGeneration(unittest.TestCase):

  def setUp(self):
    self.board = Board(is_test_board=True)
    self.engine = Engine(self.board)

  def tearDown(self):
    self.board.clear_board()

  def test_queen_moves_from_center(self):
    self.board.board[3][3] = 'wQ'
    expected_moves = (self.engine.generate_rook_moves(3, 3) +
                      self.engine.generate_bishop_moves(3, 3))
    actual_moves = self.engine.generate_queen_moves(3, 3)
    # TODO: Write a proper sort.
    self.assertEqual(sort_moves(actual_moves),
                     sort_moves(expected_moves))

  def test_queen_moves_with_friendly_pieces_blocking(self):
    self.board.board[3][3] = 'wQ'
    self.board.board[3][5] = 'wP'  # Friendly piece blocking right.
    self.board.board[5][3] = 'wP'  # Friendly piece blocking down.

    expected_moves = [
      Move(3, 3, 2, 3), Move(3, 3, 1, 3), Move(3, 3, 0, 3),  # Left
      Move(3, 3, 3, 2), Move(3, 3, 3, 1), Move(3, 3, 3, 0),  # Up
      Move(3, 3, 4, 3),  # Right up to friendly piece
      Move(3, 3, 3, 4),  # Down up to friendly piece
      Move(3, 3, 2, 2), Move(3, 3, 1, 1), Move(3, 3, 0, 0),  # Top-left
      Move(3, 3, 4, 4), Move(3, 3, 5, 5),
      Move(3, 3, 6, 6), Move(3, 3, 7, 7),  # Bottom-right up to friendly piece
      Move(3, 3, 2, 4), Move(3, 3, 1, 5), Move(3, 3, 0, 6),  # Bottom-left
      Move(3, 3, 4, 2), Move(3, 3, 5, 1), Move(3, 3, 6, 0)  # Top-right
    ]

    actual_moves = self.engine.generate_queen_moves(3, 3)
    self.assertEqual(sort_moves(actual_moves),
                     sort_moves(expected_moves))

  def test_queen_moves_with_opposing_pieces_blocking(self):
    self.board.board[3][3] = 'wQ'
    self.board.board[3][5] = 'bP'  # Opposing piece blocking right.
    self.board.board[5][3] = 'bP'  # Opposing piece blocking down.
    expected_moves = [
      Move(3, 3, 2, 3), Move(3, 3, 1, 3), Move(3, 3, 0, 3),  # Left
      Move(3, 3, 3, 2), Move(3, 3, 3, 1), Move(3, 3, 3, 0),  # Up
      Move(3, 3, 4, 3), Move(3, 3, 5, 3, True, SCORE_PIECE['P']),  # Right up to enemy piece
      Move(3, 3, 3, 4), Move(3, 3, 3, 5, True, SCORE_PIECE['P']),  # Down up to enemy piece
      Move(3, 3, 2, 2), Move(3, 3, 1, 1), Move(3, 3, 0, 0),  # Top-left
      Move(3, 3, 4, 4), Move(3, 3, 5, 5),
      Move(3, 3, 6, 6), Move(3, 3, 7, 7),  # Bottom-right up to friendly piece
      Move(3, 3, 2, 4), Move(3, 3, 1, 5), Move(3, 3, 0, 6),  # Bottom-left
      Move(3, 3, 4, 2), Move(3, 3, 5, 1), Move(3, 3, 6, 0)  # Top-right
    ]

    actual_moves = self.engine.generate_queen_moves(3, 3)
    self.assertEqual(sort_moves(actual_moves),
                     sort_moves(expected_moves))

  def test_queen_moves_from_edge(self):
    self.board.board[0][0] = 'wQ'
    expected_moves = [
      Move(0, 0, 1, 0), Move(0, 0, 2, 0),
      Move(0, 0, 3, 0), Move(0, 0, 4, 0),
      Move(0, 0, 5, 0), Move(0, 0, 6, 0),
      Move(0, 0, 7, 0),  # Right
      Move(0, 0, 0, 1), Move(0, 0, 0, 2),
      Move(0, 0, 0, 3), Move(0, 0, 0, 4),
      Move(0, 0, 0, 5), Move(0, 0, 0, 6),
      Move(0, 0, 0, 7),  # Down
      Move(0, 0, 1, 1), Move(0, 0, 2, 2),
      Move(0, 0, 3, 3), Move(0, 0, 4, 4),
      Move(0, 0, 5, 5), Move(0, 0, 6, 6),
      Move(0, 0, 7, 7)  # Bottom-right
    ]

    actual_moves = self.engine.generate_queen_moves(0, 0)
    self.assertEqual(sort_moves(actual_moves),
                     sort_moves(expected_moves))

  def test_queen_pinned(self):
    self.board.board[0][0] = 'wK'
    self.board.board[0][1] = 'wQ'
    self.board.board[0][2] = 'bQ'
    self.engine.wk_pos = (0, 0)

    _, _, self.engine.pins = self.engine.get_checks_and_pins('w')
    # Pinned by queen on the right.
    self.assertEquals(len(self.engine.pins), 1)

    actual_moves = self.engine.generate_queen_moves(1, 0)
    self.assertEqual(len(actual_moves), 1)


if __name__ == '__main__':
  unittest.main()
