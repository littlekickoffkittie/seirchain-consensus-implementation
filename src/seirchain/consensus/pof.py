"""
Proof-of-Fractal (PoF) Consensus Algorithm

This module implements the Proof-of-Fractal (PoF) consensus algorithm,
a novel consensus mechanism designed for the SeirChain network.
"""

import hashlib
import random
import time
from typing import Dict, Any

class ProofOfFractal:
    """
    Implements the Proof-of-Fractal (PoF) puzzle and verification.
    """

    def __init__(self, difficulty: int = 4):
        """
        Initialize the PoF algorithm.

        Args:
            difficulty: The number of leading zeros required in the hash.
        """
        self.difficulty = difficulty

    def create_puzzle(self, transaction_data: str) -> Dict[str, Any]:
        """
        Creates a new PoF puzzle.

        Args:
            transaction_data: The data from the transactions to be included in the Triad.

        Returns:
            A dictionary representing the puzzle.
        """
        puzzle = {
            "transaction_data": transaction_data,
            "difficulty": self.difficulty,
            "timestamp": time.time(),
        }
        return puzzle

    def solve_puzzle(self, puzzle: Dict[str, Any]) -> int:
        """
        Solves a PoF puzzle.

        Args:
            puzzle: The puzzle to solve.

        Returns:
            The nonce that solves the puzzle.
        """
        puzzle_data = puzzle["transaction_data"] + str(puzzle["timestamp"])
        target = "0" * self.difficulty
        nonce = 0
        while True:
            hash_attempt = hashlib.sha256(
                (puzzle_data + str(nonce)).encode()
            ).hexdigest()
            if hash_attempt.startswith(target):
                return nonce
            nonce += 1

    def verify_solution(self, puzzle: Dict[str, Any], nonce: int) -> bool:
        """
        Verifies a PoF solution.

        Args:
            puzzle: The puzzle that was solved.
            nonce: The nonce that was found.

        Returns:
            True if the solution is valid, False otherwise.
        """
        puzzle_data = puzzle["transaction_data"] + str(puzzle["timestamp"])
        target = "0" * self.difficulty
        hash_attempt = hashlib.sha256(
            (puzzle_data + str(nonce)).encode()
        ).hexdigest()
        return hash_attempt.startswith(target)
