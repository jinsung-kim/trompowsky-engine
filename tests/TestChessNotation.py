import sys
import os
import unittest

from helpers import glue_notation

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from board import Board
from move import Move


class TestChessNotation(unittest.TestCase):
  def setUp(self):
    self.board = Board(is_test_board=False)

  def test_file_rank_notation(self):
    n1 = self.board.to_chess_notation(0, 0)
    self.assertEqual(glue_notation(n1), 'a8')
    n2 = self.board.to_chess_notation(2, 2)
    self.assertEqual(glue_notation(n2), 'c6')
    n3 = self.board.to_chess_notation(4, 2)
    self.assertEqual(glue_notation(n3), 'e6')
    n4 = self.board.to_chess_notation(3, 6)
    self.assertEqual(glue_notation(n4), 'd2')
    n5 = self.board.to_chess_notation(7, 3)
    self.assertEqual(glue_notation(n5), 'h5')
    n6 = self.board.to_chess_notation(2, 1)
    self.assertEqual(glue_notation(n6), 'c7')

  def test_promotion_notation(self):
    self.board.board[0][0] = 'wQ'
    move = Move(0, 1, 0, 0, None, True)
    self.assertEqual(self.board.log_move(move), 'a8=Q')

  def test_capture_promotion_notation(self):
    self.board.board[0][2] = 'wQ'
    move = Move(0, 1, 2, 0, 'bP', True)
    self.assertEqual(self.board.log_move(move), 'axc8=Q')

  def test_pawn_notation(self):
    self.board.board[5][0] = 'wP'
    move = Move(0, 6, 0, 5)
    self.assertEqual(self.board.log_move(move), 'a3')
    self.board.clear_board()
    self.board.board[4][0] = 'wP'
    move = Move(0, 6, 0, 4)
    self.assertEqual(self.board.log_move(move), 'a4')

  def test_standard_notation(self):
    self.board.board[4][0] = 'wR'
    move = Move(0, 0, 0, 4)
    self.assertEqual(self.board.log_move(move), 'Ra4')
    self.board.clear_board()
    self.board.board[3][3] = 'wB'
    move = Move(1, 1, 3, 3)
    self.assertEqual(self.board.log_move(move), 'Bd5')

  def test_standard_notation_with_capture(self):
    self.board.board[5][5] = 'wQ'
    move = Move(0, 0, 5, 5, 'bR')
    self.assertEqual(self.board.log_move(move), 'Qxf3')
    self.board.clear_board()
    self.board.board[4][4] = 'wR'
    move = Move(4, 0, 4, 4, 'bP')
    self.assertEqual(self.board.log_move(move), 'Rxe4')


if __name__ == '__main__':
  unittest.main()
