import time
from seirchain.core.crypto import hash_data

class Transaction:
    def __init__(self, from_address, to_address, amount, signature=None):
        self.from_address = from_address
        self.to_address = to_address
        self.amount = amount
        self.timestamp = time.time()
        self.signature = signature

    def __repr__(self):
        return f"Transaction(from={self.from_address}, to={self.to_address}, amount={self.amount})"

    def calculate_hash(self):
        """Calculates the hash of the transaction."""
        transaction_data = f"{self.from_address}{self.to_address}{self.amount}{self.timestamp}"
        return hash_data(transaction_data)

    def sign(self, private_key):
        """Signs the transaction with the given private key."""
        self.signature = private_key.sign(self.calculate_hash().encode('utf-8'))

    def is_valid(self):
        """Validates the transaction."""
        if self.from_address == "0":  # Genesis block transaction
            return True
        if not self.signature:
            return False
        # The public key needs to be passed in to verify the signature
        # This will be handled by the node that receives the transaction
        return True
