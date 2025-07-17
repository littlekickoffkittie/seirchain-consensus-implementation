import unittest
from seirchain.consensus.pof import ProofOfFractal

class TestProofOfFractal(unittest.TestCase):

    def test_pof(self):
        pof = ProofOfFractal(difficulty=4)
        puzzle = pof.create_puzzle("test data")
        nonce = pof.solve_puzzle(puzzle)
        self.assertTrue(pof.verify_solution(puzzle, nonce))
