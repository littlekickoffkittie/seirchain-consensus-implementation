import time
from seirchain.core.crypto import hash_data

class Triad:
    def __init__(self, timestamp, transactions, previous_hash=''):
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.vdf_output = None
        self.vdf_proof = None
        self.nonce = 0
        self.hash = self.calculate_hash()

    def __repr__(self):
        return f"Triad(timestamp={self.timestamp}, transactions={len(self.transactions)}, hash={self.hash})"

    def calculate_hash(self):
        """Calculates the hash of the Triad."""
        triad_data = f"{self.timestamp}{self.transactions}{self.previous_hash}{self.vdf_output}{self.nonce}"
        return hash_data(triad_data)

    def mine_triad(self, difficulty):
        """Mines the Triad by finding a hash that starts with a certain number of zeros."""
        while self.hash[:difficulty] != "0" * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()
