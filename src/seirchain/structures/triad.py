"""
Triad Data Structure

This module defines the Triad data structure, the fundamental unit of the SeirChain ledger.
"""

import hashlib
import statistics
from typing import List, Any

def compute_merkle_root(transactions: List[str]) -> str:
    """
    Computes the Merkle root for a list of transactions.
    """
    if not transactions:
        return ""

    transaction_hashes = [hashlib.sha256(tx.encode()).hexdigest() for tx in transactions]

    while len(transaction_hashes) > 1:
        if len(transaction_hashes) % 2 != 0:
            transaction_hashes.append(transaction_hashes[-1])

        new_hashes = []
        for i in range(0, len(transaction_hashes), 2):
            combined_hash = hashlib.sha256(
                (transaction_hashes[i] + transaction_hashes[i+1]).encode()
            ).hexdigest()
            new_hashes.append(combined_hash)
        transaction_hashes = new_hashes

    return transaction_hashes[0]

def is_timestamp_valid(timestamp: int, parent_timestamps: List[int]) -> bool:
    """
    Validates the timestamp of the Triad.
    """
    if len(parent_timestamps) < 11:
        return True

    median_timestamp = statistics.median(parent_timestamps[-11:])
    return timestamp > median_timestamp

class Triad:
    """
    Represents a Triad in the SeirChain ledger.
    """

    def __init__(self, transactions: List[str], parent_hash: str, pof_data: Any, timestamp: int, parent_timestamps: List[int]):
        """
        Initializes a new Triad.

        Args:
            transactions: A list of transactions to be included in the Triad.
            parent_hash: The hash of the parent Triad.
            pof_data: The Proof-of-Fractal data for this Triad.
            timestamp: The timestamp of the Triad.
            parent_timestamps: A list of the timestamps of the parent Triads.
        """
        if not is_timestamp_valid(timestamp, parent_timestamps):
            raise ValueError("Invalid timestamp")

        self.transactions = transactions
        self.parent_hash = parent_hash
        self.pof_data = pof_data
        self.timestamp = timestamp
        self.parent_timestamps = parent_timestamps
        self.merkle_root = compute_merkle_root(self.transactions)
        self.child_references = []

    def __str__(self):
        return f"Triad(merkle_root='{self.merkle_root}', parent_hash='{self.parent_hash}')"
