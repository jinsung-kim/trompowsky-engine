import unittest

from TestRookMoveGeneration import TestRookMoveGeneration
from TestBishopMoveGeneration import TestBishopMoveGeneration
from TestQueenMoveGeneration import TestQueenMoveGeneration
from TestBoardMethods import TestBoardMethods

if __name__ == '__main__':
  test_cases = [
    TestRookMoveGeneration,
    TestBishopMoveGeneration,
    TestQueenMoveGeneration,
    TestBoardMethods,
  ]

  test_suite = unittest.TestSuite()
  for test_case in test_cases:
    test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(test_case))

  unittest.TextTestRunner(verbosity=2).run(test_suite)
