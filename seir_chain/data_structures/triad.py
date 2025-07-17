import time
import json
from seir_chain.crypto.hashing import sha256_hash, merkle_root
from .transaction import Transaction

class Triad:
    """
    Represents a Triad, the fundamental block-like structure in SeirChain.
    A Triad contains transactions and references to its parent and children.
    """
    def __init__(self, parent_hash: bytes, miner_address: str, height: int, difficulty: int):
        self.parent_hash = parent_hash
        self.height = height
        self.timestamp = int(time.time())
        self.nonce = 0
        self.miner_address = miner_address
        self.difficulty = difficulty

        self.transactions: list[Transaction] = []
        self.tx_merkle_root: bytes = b''

        # In the fractal model, a Triad can have multiple children.
        # These would be the hashes of the children Triads.
        self.child_hashes: list[bytes] = []

        # HRC / Consensus related fields
        self.aggregated_proof: bytes = b'' # e.g., aggregated BLS signature
        self.committee_pub_key: bytes = b'' # e.g., aggregated BLS public key

    def to_dict(self, for_hashing=True) -> dict:
        """Returns a dictionary representation of the Triad header."""
        data = {
            "parent_hash": self.parent_hash.hex(),
            "height": self.height,
            "timestamp": self.timestamp,
            "nonce": self.nonce,
            "miner_address": self.miner_address,
            "difficulty": self.difficulty,
            "tx_merkle_root": self.tx_merkle_root.hex()
        }
        if not for_hashing:
            data["child_hashes"] = [h.hex() for h in self.child_hashes]
            data["aggregated_proof"] = self.aggregated_proof.hex()
            data["committee_pub_key"] = self.committee_pub_key.hex()
            data["transactions"] = [tx.to_dict() for tx in self.transactions]
        return data

    def calculate_merkle_root(self):
        """Calculates and sets the Merkle root of the transactions."""
        if not self.transactions:
            self.tx_merkle_root = sha256_hash(b'')
        else:
            tx_hashes = [tx.get_hash() for tx in self.transactions]
            self.tx_merkle_root = merkle_root(tx_hashes)

    def get_header_hash(self) -> bytes:
        """
        Calculates the hash of the Triad's header.
        This is the hash that will be used for PoW.
        """
        # Ensure merkle root is calculated before hashing
        self.calculate_merkle_root()
        header_str = json.dumps(self.to_dict(for_hashing=True), sort_keys=True)
        return sha256_hash(header_str.encode('utf-8'))

    def add_transaction(self, transaction: Transaction):
        """Adds a valid transaction to the Triad."""
        # In a real system, we'd have a mempool and more complex validation.
        if transaction.is_valid():
            self.transactions.append(transaction)
        else:
            raise ValueError("Cannot add invalid transaction to Triad.")

    def __repr__(self):
        return f"<Triad h={self.height} txns={len(self.transactions)} hash={self.get_header_hash().hex()[:8]}>"
