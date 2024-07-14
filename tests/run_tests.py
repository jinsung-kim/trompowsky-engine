import unittest

from TestPawnMoveGeneration import TestPawnMoveGeneration
from TestRookMoveGeneration import TestRookMoveGeneration
from TestBishopMoveGeneration import TestBishopMoveGeneration
from TestQueenMoveGeneration import TestQueenMoveGeneration
from TestKingMoveGeneration import TestKingMoveGeneration
from TestKnightMoveGeneration import TestKnightMoveGeneration
from TestBoardMethods import TestBoardMethods
from TestChessNotation import TestChessNotation
from TestGenericMoveGeneration import TestGenericMoveGeneration

if __name__ == '__main__':
  test_cases = [
    TestKnightMoveGeneration,
    TestKingMoveGeneration,
    TestPawnMoveGeneration,
    TestRookMoveGeneration,
    TestBishopMoveGeneration,
    TestQueenMoveGeneration,
    TestGenericMoveGeneration,
    TestBoardMethods,
    TestChessNotation
  ]

  test_suite = unittest.TestSuite()
  for test_case in test_cases:
    test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(test_case))

  unittest.TextTestRunner(verbosity=2).run(test_suite)
