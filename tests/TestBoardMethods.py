import sys
import os
import unittest

from move import Move

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from board import Board, EMPTY_BOARD
from engine import Engine


class TestBoardMethods(unittest.TestCase):
  def setUp(self):
   self.board = Board(is_test_board=False)
   self.engine = Engine(self.board)

  def test_board_clear(self):
    self.board.board[3][3] = 'wQ'
    found_wq = any('wQ' in row for row in self.board.board)
    self.assertEqual(found_wq, True)  # flatten board and check that wQ is there.

    self.board.clear_board()

    self.assertEqual(self.board.board, EMPTY_BOARD)

  def test_score_board(self):
    self.assertEqual(self.board.score_board(), 0)
    self.board.clear_board()
    self.assertEqual(self.board.score_board(), 0)

  def test_score_board_2(self):
    self.board.clear_board()
    self.board.board[0][0] = 'wQ'
    self.board.board[0][1] = 'wR'
    self.assertEqual(self.board.score_board(), 14)

  def test_move_undo_promotion(self):
    self.board.clear_board()
    self.board.board[1][0] = 'wP'

    move = Move(0, 1, 0, 0, None, True)

    self.board.make_move(move)
    self.assertEqual(self.board.score_board(), 9)

    self.board.undo_move(move)
    self.assertEqual(self.board.score_board(), 1)

  def test_move_undo_capture(self):
    self.board.clear_board()
    self.board.board[1][1] = 'wP'
    self.board.board[0][0] = 'bQ'

    move = Move(0, 0, 1, 1, 'wP', False)

    self.assertEqual(self.board.score_board(), -8)
    self.board.make_move(move)
    self.assertEqual(self.board.score_board(), -9)

    self.board.undo_move(move)
    self.assertEqual(self.board.score_board(), -8)


if __name__ == '__main__':
  unittest.main()
