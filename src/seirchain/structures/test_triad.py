import unittest
from seirchain.structures.triad import Triad, compute_merkle_root

class TestTriad(unittest.TestCase):

    def test_merkle_root(self):
        transactions = ["tx1", "tx2", "tx3", "tx4"]
        merkle_root = compute_merkle_root(transactions)
        self.assertIsInstance(merkle_root, str)
        self.assertEqual(len(merkle_root), 64)

    def test_triad_creation(self):
        transactions = ["tx1", "tx2", "tx3"]
        triad = Triad(transactions, "parent_hash", "pof_data")
        self.assertEqual(triad.transactions, transactions)
        self.assertEqual(triad.parent_hash, "parent_hash")
        self.assertEqual(triad.pof_data, "pof_data")
        self.assertIsNotNone(triad.merkle_root)
